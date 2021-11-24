import socket, netifaces, ipaddress
import time
import threading 


message = "Hi, glad to see u"


def connect(addr,search_port):
    '''this function tries to connect to the transmitted port.
     If the port is open, it sends a message to the server and also receives a message. 
     If the messages match, it prints that everything is fine'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.001)
    result = sock.connect_ex((str(addr),int(search_port)))
    if result == 0:
        print(f"Found client on {addr}")
        global clients
        clients.append(addr)
        #sock.close() удалено за ненадобностью - жду подтверждения
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.connect((str(addr),int(search_port)))
        print("connect done")
        data = sock.recv(1024)
        print(data.decode('utf8'))
        sock.send('Hi, glad to see u'.encode('utf8'))
        if str(data.decode('utf8')) == message:
            print("he is a good boy!")
        sock.close()



def get_client_ips( target_interface="enp3s0", family='AF_INET', search_port = "51815" , debug = True , mask = None):
    '''This function scans the network and looks for open ports in it. 
    Returns a list of ip addresses that have the corresponding port open  '''

    #if debug==True:
    #    search_port=80
    global clients
    clients = []

    interface_list=netifaces.interfaces() #получить список интерфейсов
    if debug == True:
        print(interface_list)
    if target_interface not in interface_list:
        print("You have entered the wrong target_interface")
        return "NO_INTERFACE"

    addrs = netifaces.ifaddresses(target_interface)
    if debug == True:
        #print(f"Addrs is {addrs}")
        pass
    host=addrs[netifaces.AF_INET]
    if debug == True:
        print(f"Host is {host}")
    ipv4=host[0]['addr']
    if mask == None:
        mask=host[0]['netmask']
    #mask='255.255.0.0' #checked what would happen with a smaller mask
    if debug == True:
        print(f"Iv4 is {ipv4}/{mask}")
    
    s=ipv4+"/"+mask
    net = ipaddress.IPv4Network(s, strict=False)
    if debug == True:
        print("my net is", net)
        print("search_port is",search_port)  
    
    threads = []
    for addr in net:
        threads.append( threading.Thread(target = connect, args = (addr,search_port)) )
        threads[-1].start()
        
    for thread in threads:
        thread.join()
    return clients


    



if __name__=='__main__':
    start_time=time.time()
    clients=get_client_ips("enp7s0",'AF_INET')
    print(clients)
    print (f"program time is  {time.time() - start_time} seconds")

