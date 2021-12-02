import socket, netifaces, ipaddress
import logging
import configparser
import pickle
import os



def client_func(target_interface="enp3s0",family='AF_INET', port = "51815", config_file = "./client/config.ini"):
    '''This function opens the port passed to it. 
    When someone connects to this port, it sends a message and waits for a message. 
    If the messages match, it prints that everything is fine'''
    #get values from config
    config = configparser.ConfigParser()
    #прописать проверку существования файла
    if not os.path.isfile(config_file):
        logging.error("No config file")
        return "NO_CONFIG_FILE"
    config.read(config_file)   
    scaner_name = config.get("GENERAL","Scanername")
    client_data = {"scaner_name": scaner_name}
    logging.debug(f"client_data is {client_data}") #для каждого лога указать время сообщения
#погуглить про timestamp 

    interface_list=netifaces.interfaces() #получить список интерфейсов
    
    logging.debug(f"interface_list is {interface_list}")
    if target_interface not in interface_list:
        logging.error("You have entered the wrong target_interface")

    addrs = netifaces.ifaddresses(target_interface)

    host=addrs[netifaces.AF_INET]

    logging.debug(f"Host is {host}")

    ipv4=host[0]['addr']
    mask=host[0]['netmask']

    logging.debug(f"my ip {ipv4}")  

    message = "Hi, glad to see u"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ipv4, int(port)))
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


if __name__=='__main__':
    client_func("enp7s0")
