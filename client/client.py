import socket, netifaces, ipaddress
import logging
import configparser

def client_func(target_interface="enp3s0",family='AF_INET', port = "51815", config_file = "config.ini"):
    '''This function opens the port passed to it. 
    When someone connects to this port, it sends a message and waits for a message. 
    If the messages match, it prints that everything is fine'''

    #get values from config
    config = configparser.ConfigParser()
    config.read(config_file)   
    scaner_name = config["DEFAULT"]["Scanername"]




    interface_list=netifaces.interfaces() #получить список интерфейсов
    
    logging.debug(interface_list)
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
        logging.debug("connected from the address", addr)
        conn.send("Hi, glad to see u".encode('utf8'))
        data = conn.recv(1024)
        logging.debug("got message ", data.decode("utf8"))
        if (data.decode('utf8')) == message:
            logging.debug("keys are equal")
        
        conn.close()


if __name__=='__main__':
    client_func("enp7s0")
