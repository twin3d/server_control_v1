import socket, netifaces, ipaddress
import time
import threading 
import logging
import configparser
import pickle
import os
import sys
import argparse

message = "Hi, glad to see u"

def guess_interface(): 
    '''this function guesses the interface'''
    interface_list=netifaces.interfaces()
    for interface in interface_list:
        if interface[0]=="e" or interface[0]=="w":
            #print(interface)
            try:
                addrs = netifaces.ifaddresses(interface)
                host=addrs[netifaces.AF_INET]
                ipv4=host[0]['addr']
                #print(ipv4)
                if ipv4[:6]=="192.16" or ipv4[:3]=="10." or ipv4[:6]=="172.16":
                    return interface
            except:
                pass
    return "No interface"

def connect(addr, search_port, socket_timeout):
    '''this function tries to connect to the transmitted port.
     If the port is open, it sends a message to the server and also receives a message. 
     If the messages match, it prints that everything is fine
     after that, it receives the client's data'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(float(socket_timeout))
    #sock.settimeout(socket_timeout)
    #print(addr)
    #sock.settimeout()
    result = sock.connect_ex((str(addr),int(search_port)))
    if result == 0:
        logging.debug(f"Found client on {addr}")
        #logging.debug("connect done")
        data = sock.recv(1024)
        #logging.debug(f"got message  {data.decode('utf8')}")
        sock.send('Hi, glad to see u'.encode('utf8'))
        if str(data.decode('utf8')) == message:
            clients.append(addr)
            #logging.debug("keys are equal")
            #getting client data
            client_data_in_bytes = sock.recv(2048)
            client_data = pickle.loads(client_data_in_bytes)
            #logging.debug("got client data")
            #logging.debug(str(client_data))
            clients_dict[str(addr)] = client_data
            
    sock.close()



def get_client_ips( target_interface=None, search_port = "51815", mask = None, 
config_file = "config.ini", output_file = None, output_type = None, conf = None, 
net_str = None):
    '''This function scans the network and looks for open ports in it. 
    Returns a list of ip addresses that have the corresponding port open  '''

    global clients
    clients = []
    global clients_dict
    clients_dict = {}

    
    #get values from config
    try:
        config = configparser.ConfigParser()
        if not os.path.isfile(config_file):
            logging.error("No config file")
            return "NO_CONFIG_FILE"  
        config.read(config_file)  
        search_port = config.get("GENERAL","Port")

        socket_timeout = config.get("GENERAL","Timeout")

        if target_interface == None:
            target_interface = guess_interface()

        try:
            log_level = config.get("GENERAL","log_level")
        except Exception:
            log_level = "debug"

        
        
        logger = logging.getLogger()
        if log_level == "debug":
            logger.setLevel(logging.DEBUG)
        elif log_level == "warning":
            logger.setLevel(logging.ERROR)
        logger.debug(f"Debug level is {log_level}")
        
        logging.debug(f"search_port is {search_port}, socket_timeout is  {socket_timeout}")
    except Exception as err_msg:
        logging.error(f"!!! Error !!! when reading config file! Check {config_file} file, or get default one. More exact: {err_msg}.")
        #print(f"!!! Error !!! when reading config file! Check {config_file} file, or get default one. More exact: {err_msg}.")
        sys.exit()

    interface_list=netifaces.interfaces() #получить список интерфейсов
    logging.debug(f"interface_list is {interface_list}")

    if target_interface not in interface_list:
        logging.error("You have entered the wrong target_interface")
        return "NO_INTERFACE"

    addrs = netifaces.ifaddresses(target_interface)

    host=addrs[netifaces.AF_INET]
    #logging.debug(f"Host is {host}")

    ipv4=host[0]['addr']
    if mask == None:
        mask=host[0]['netmask']
    #mask='255.255.0.0' #checked what would happen with a smaller mask
    logging.debug(f"Iv4 is {ipv4}/{mask}")
    
    if net_str == None:
        net_str=ipv4+"/"+mask
    net = ipaddress.IPv4Network(net_str, strict=False)

    logging.debug(f"my net is {net}")
    logging.debug(f"search_port is {search_port}")  
    
    threads = []
    for addr in net:
        #connect(addr,search_port,socket_timeout)
        threads.append( threading.Thread(target = connect, args = (addr,search_port,socket_timeout)))
        threads[-1].start()


    for thread in threads:
        thread.join()

    # ВСЕГДА RETURN!!!
    return output(output_file, output_type, conf)


def output(output_file, output_type, conf):
    '''this function is based on output_type сalls a function of the form in the appropriate form'''
    if output_type == "python":
        logging.debug('Python output')
        return clients_dict

    elif output_type == "text":
        print_to_file(output_file)

    elif output_type == "config":
        correct_file(conf, output_file)

    else:
        print("problems with output type")




def print_to_file(filename):
    '''function of output of the program result to a text file'''
    try:
        file = open(filename, "w")
    except Exception as err_msg:
        logging.error("You entered wrong filename. Error is {err_msg}")
        #sys.exit()
        #вопрос что делать если не смог записать в файл - записать в дефолтный
    logging.debug("writing to file")
    #write big section
    file.write("Big\n")
    for ip in clients_dict.keys():
        if clients_dict[ip]["scaner_type"]=="Big":
            file.write(clients_dict[ip]["scaner_name"])
            file.write(" ")
            file.write(str(ip))
            file.write(" ")
            file.write(clients_dict[ip]["mac_addr"])
            file.write("\n")

    file.write("\n")

    #write small section
    file.write("Small\n")
    for ip in clients_dict.keys():
        if clients_dict[ip]["scaner_type"]=="Small":
            file.write(clients_dict[ip]["scaner_name"])
            file.write(" ")
            file.write(str(ip))
            file.write(" ")
            file.write(clients_dict[ip]["mac_addr"])
            file.write("\n")

    file.close()



def correct_file(input_filename, output_filename):
    '''this function replaces the ip addresses in 3d_automation/server_control/config.sh 
    and outputs to output_filename'''
    logging.debug("Correcting file")
    input_file = open(input_filename, "r")
    output_file = open(output_filename,"w")

    if os.path.isfile("../../3d_automation/server_control/config.sh"):
        os.system(f"cp ../../3d_automation/server_control/config.sh {input_filename}")
        logging.debug("copy config from 3d_automation")
    

    big_cliets_list=[]
    small_cliets_list=[]

    for addr in clients_dict.keys():
        if clients_dict[addr]["scaner_type"]=="Big":
            big_cliets_list.append(addr)
        elif clients_dict[addr]["scaner_type"]=="Small":
            small_cliets_list.append(addr)


    while True:
        line = input_file.readline()
        if not line:
            break
        output_file.write(line)
        if '$SCANNER == "BIG"' in line:
            for ip in big_cliets_list:
                output_file.write(f'  ips+=("{ip}")\n')
                output_file.write('  users+=("pi")')
            while True:
                line = input_file.readline()
                if not line:
                    break
                if "SCANNER_MQTT_IP" in line:
                    break


        if '$SCANNER == "SMALL"' in line:
            for ip in small_cliets_list:
                output_file.write(f'  ips+=("{ip}")\n')
                output_file.write('  users+=("pi")')
            while True:
                line = input_file.readline()
                if not line:
                    break
                if "SCANNER_MQTT_IP" in line:
                    break








if __name__=='__main__':
    start_time=time.time()
    
    parser = argparse.ArgumentParser(description='Config')

    parser.add_argument(
        '--config', '-c',
        type=str,
        default="config.ini",
        help='enter config (default: config.ini)'
    )
    parser.add_argument(
        '-i',
        type=str,
        help='enter target interface'
    )
    parser.add_argument(
        '--out', '-o',
        type=str,
        default="clients_list.out",
        help='enter output file (default: clients_list.out)'
    )

    parser.add_argument(
        '--type', '-t',
        type=str,
        default="text",
        help="enter the output type, it may be: python program will return a dictionary;\n text - the program will output as a text file\n; config - the program will add ip addresses to the transmitted config file  (default: text)"
    )


    parser.add_argument(
        '--config_sh', '-s',
        type=str,
        default="conf.sh",
        help="enter the config file to which you want to add ip addresses (default: conf.sh)"
    )

    parser.add_argument(
        '--net', '-n',
        type=str,
        help="enter net which you wanna scan"
    )

    args = parser.parse_args()
    output_types=["python", "text", "config"]
    if args.type not in output_types:
        print("entered incorrect output type")
        sys.exit()

    get_client_ips(config_file = args.config, output_file = args.out,
    output_type =args.type, conf = args.config_sh, net_str = args.net)
    logging.info(clients_dict)
    #logging.debug(f"program time is  {time.time() - start_time} seconds")

