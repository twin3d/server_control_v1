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

    interface_list=netifaces.interfaces()
    for interface in interface_list:
        if interface[0]=="e":
            #print(interface)
            addrs = netifaces.ifaddresses(interface)
            host=addrs[netifaces.AF_INET]
            ipv4=host[0]['addr']
            #print(ipv4)
            if ipv4[:6]=="192.16" or ipv4[:3]=="10." or ipv4[:6]=="172.16":
                return interface
    return "No interface"

def connect(addr,search_port, socket_timeout):
    '''this function tries to connect to the transmitted port.
     If the port is open, it sends a message to the server and also receives a message. 
     If the messages match, it prints that everything is fine
     after that, it receives the client's data'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(float(socket_timeout))
    sock.settimeout(0.01)
    result = sock.connect_ex((str(addr),int(search_port)))
    if result == 0:
        logging.debug(f"Found client on {addr}")
        #global clients
        #global clients_dict
        logging.debug("connect done")
        data = sock.recv(1024)
        logging.debug(f"got message  {data.decode('utf8')}")
        sock.send('Hi, glad to see u'.encode('utf8'))
        if str(data.decode('utf8')) == message:
            clients.append(addr)
            logging.debug("keys are equal")
            #getting client data
            client_data_in_bytes = sock.recv(2048)
            client_data = pickle.loads(client_data_in_bytes)
            logging.debug("got client data")
            logging.debug(str(client_data))
            clients_dict[str(addr)] = client_data
            
    sock.close()



def get_client_ips( target_interface=None, search_port = "51815", mask = None, 
config_file = "config.ini", output_file = None):
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
        socket_timeout = config["GENERAL"]["Timeout"]
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
        print(f"!!! Error !!! when reading config file! Check {config_file} file, or get default one. More exact: {err_msg}.")
        sys.exit()

    interface_list=netifaces.interfaces() #получить список интерфейсов
    logging.debug(f"interface_list is {interface_list}")

    if target_interface not in interface_list:
        logging.error("You have entered the wrong target_interface")
        return "NO_INTERFACE"

    addrs = netifaces.ifaddresses(target_interface)

    host=addrs[netifaces.AF_INET]
    logging.debug(f"Host is {host}")

    ipv4=host[0]['addr']
    if mask == None:
        mask=host[0]['netmask']
    #mask='255.255.0.0' #checked what would happen with a smaller mask
    logging.debug(f"Iv4 is {ipv4}/{mask}")
    
    s=ipv4+"/"+mask
    net = ipaddress.IPv4Network(s, strict=False)

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
    return output(output_file)


def output(filename):
    '''output function'''
    if filename == None:
        logging.debug('Python output')
        return clients_dict

    else:
        return print_to_file(filename)




def print_to_file(filename):
    '''function of output of the program result to a file'''
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






if __name__=='__main__':
    start_time=time.time()
    
    parser = argparse.ArgumentParser(description='Config')

    parser.add_argument(
        '--config', '--c',
        type=str,
        default="config.ini",
        help='enter config (default: config.ini)'
    )
    '''#закомментировано, тк интерфейс угадывается автоматически
    parser.add_argument(
        '--i',
        type=str,
        help='enter target interface'
    )
    args = parser.parse_args()
    '''
    parser.add_argument(
        '--out', '--o',
        type=str,
        help='enter output file (default: output_file.txt)'
    )

    args = parser.parse_args()
    print(args)

    get_client_ips(config_file = args.config, output_file = args.out)
    logging.info(clients_dict)
    #logging.debug(f"program time is  {time.time() - start_time} seconds")

