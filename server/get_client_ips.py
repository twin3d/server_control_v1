import socket, netifaces, ipaddress
import time
import threading 
import logging
import configparser
import pickle

message = "Hi, glad to see u"


def connect(addr,search_port, socket_timeout, client_data):
    '''this function tries to connect to the transmitted port.
     If the port is open, it sends a message to the server and also receives a message. 
     If the messages match, it prints that everything is fine'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(int(socket_timeout))
    result = sock.connect_ex((str(addr),int(search_port)))
    if result == 0:
        logging.debug(f"Found client on {addr}")
        global clients
        logging.debug("connect done")
        data = sock.recv(1024)
        logging.debug("got message ", data.decode('utf8'))
        sock.send('Hi, glad to see u'.encode('utf8'))
        if str(data.decode('utf8')) == message:
            clients.append(addr)
            logging.debug("keys are equal")

            client_data_in_bytes = sock.recv(1024)
            client_data = pickle.loads(client_data_in_bytes)




        sock.close()



def get_client_ips( target_interface="enp3s0", family='AF_INET',
 search_port = "51815", mask = None, config_file = "confug.ini"):
    '''This function scans the network and looks for open ports in it. 
    Returns a list of ip addresses that have the corresponding port open  '''

    global clients
    clients = []

    #get values from config
    config = configparser.ConfigParser()
    config.read(config_file)   
    search_port = config["DEFAULT"]["Port"]
    socket_timeout = config["DEFAULT"]["Timeout"]




    interface_list=netifaces.interfaces() #получить список интерфейсов
    logging.debug(interface_list)

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

    logging.debug("my net is", net)
    logging.debug("search_port is",search_port)  
    
    threads = []
    for addr in net:
        threads.append( threading.Thread(target = connect, args = (addr,search_port,socket_timeout)))
        threads[-1].start()
        
    for thread in threads:
        thread.join()

    return clients

def output_print(clients, output_type = "python"):
    if output_type == "python":
        output_dict = {}
        for client in clients:
            host = str(client)
            output_dict[host]=""

        return output_dict

    elif output_type == "output_file":
        pass
    else:
        logging.error("You enter wrong output_type")
        return "ERROR_OUTPUT"









if __name__=='__main__':
    start_time=time.time()
    clients=get_client_ips("enp7s0",'AF_INET')
    logging.info(clients)
    logging.debug(f"program time is  {time.time() - start_time} seconds")

