import socket, netifaces, ipaddress
import logging
import configparser
import pickle
import os
import argparse
import sys
import signal
import time

def guess_interface(): 
    '''this function guesses the interface'''
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


def signal_handler(signum, frame):
    '''this signal handler closes the socket when the program terminates on a signal'''
    print("Signal Exit")
    sock.close()
    sys.exit(0)



def client_func(config_file, target_interface = None):
    '''This function opens the port passed to it. 
    When someone connects to this port, it sends a message and waits for a message. 
    If the messages match, it prints that everything is fine
    after that, it sends the client data to the server'''
    
    #get values from config
    try:
        config = configparser.ConfigParser()
        #прописать проверку существования файла
        if not os.path.isfile(config_file):
            logging.error("No config file")
            return "NO_CONFIG_FILE"
        config.read(config_file)
        default_name_sourse = config.get("GENERAL","default_name_sourse") 
        if default_name_sourse == "host":
            scaner_name = socket.gethostname()
        elif default_name_sourse == "scannername": 
            scaner_name = config.get("GENERAL","Scannername")
        else:
            print("parsed incorrect default_name_sourse")
            sys.exit()
        print(scaner_name)
        scaner_type = config.get("GENERAL","Type")
        if target_interface == None:
            target_interface = guess_interface()
        port = config.get("GENERAL","Port")

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

    except Exception as err_msg:
        logging.error(f"!!! Error !!! when reading config file! Check {config_file} file, or get default one. More exact: {err_msg}.")
        print(f"!!! Error !!! when reading config file! Check {config_file} file, or get default one. More exact: {err_msg}.")
        sys.exit()




    interface_list=netifaces.interfaces() #получить список интерфейсов
    
    logging.debug(f"interface_list is {interface_list}")
    if target_interface not in interface_list:
        logging.error("You have entered the wrong target_interface")
        sys.exit()


    mac_addr = netifaces.ifaddresses(target_interface)[netifaces.AF_LINK][0]["addr"]
    client_data = {"scaner_name": scaner_name, "scaner_type": scaner_type, "mac_addr": mac_addr}
    logging.debug(f"client_data is {client_data}")
    

    addrs = netifaces.ifaddresses(target_interface)

    host=addrs[netifaces.AF_INET]

    logging.debug(f"Host is {host}")

    ipv4=host[0]['addr']
    mask=host[0]['netmask']

    logging.debug(f"my ip {ipv4}")  

    
    message = "Hi, glad to see u"
    global sock 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        sock.bind((ipv4, int(port)))
    except:
        try:
            time.sleep(200)
            sock.bind((ipv4, int(port)))
        except:
            print("Bind error - port is already occupied. Wait some time and restart")
            sys.exit()

        
    sock.listen(5)
    data=""
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        conn, addr = sock.accept()
        logging.debug(f'connected from the address {addr} on {time.strftime("%H:%M:%S", time.localtime())}')

        conn.send("Hi, glad to see u".encode('utf8'))
        data = conn.recv(1024)
        if (data.decode('utf8')) == message:
            #sending client data
            client_data_in_bytes=pickle.dumps(client_data)
            conn.send(client_data_in_bytes)
        
        conn.close()






if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Config')
    a = guess_interface()
    parser.add_argument(
        '--config',
        type=str,
        default="config.ini",
        help='enter config (default: config.ini)'
    )
    
    parser.add_argument(
        '--i',
        type=str,
        help='enter target interface'
    )
    args = parser.parse_args()

    #print(args.config, args.i)
    client_func(config_file = args.config)




