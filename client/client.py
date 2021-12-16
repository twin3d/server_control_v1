import socket, netifaces, ipaddress
import logging
import configparser
import pickle
import os
import argparse
import sys


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
        scaner_name = config.get("GENERAL","Scanername")
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind((ipv4, int(port)))
    except:
        request = (f"sudo kill $(sudo lsof -t -i:{port})")
        code = os.system(request)
        try:
            sock.bind((ipv4, int(port)))
        except:
            print("Bind error - port is already occupied. Wait some time and restart")
            sys.exit()

        
    sock.listen(5)
    data=""
    while True:
        conn, addr = sock.accept()
        logging.debug(f"connected from the address {addr}")
        conn.send("Hi, glad to see u".encode('utf8'))
        data = conn.recv(1024)
        logging.debug(data.decode("utf8"))
        if (data.decode('utf8')) == message:
            logging.debug("keys are equal")
            #sending client data
            client_data_in_bytes=pickle.dumps(client_data)
            conn.send(client_data_in_bytes)
        
        conn.close()
        #break




if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Config')
    a = guess_interface()
    parser.add_argument(
        '--config',
        type=str,
        default="config.ini",
        help='enter config (default: config.ini)'
    )
    '''
    parser.add_argument(
        '--i',
        type=str,
        help='enter target interface'
    )'''
    args = parser.parse_args()

    #print(args.config, args.i)
    client_func(config_file = args.config)




