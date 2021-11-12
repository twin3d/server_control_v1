import socket, netifaces, ipaddress
import time

def get_client_ips( target_interface="enp7s0", family='AF_INET', search_port = "51815" , debug = True):
    '''This function scans the network and looks for open ports in it. 
    Returns a list of ip addresses that have the corresponding port open  '''
    clients = []
    if debug==True:
        search_port=80

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
    mask=host[0]['netmask']
    mask='255.255.0.0' #checked what would happen with a smaller mask
    if debug == True:
        print(f"Iv4 is {ipv4}/{mask}")
    
    s=ipv4+"/"+mask
    net = ipaddress.IPv4Network(s, strict=False)
    if debug == True:
        print("my net is", net)  
    
    for addr in net:
        if debug == True:
            #print(f"ip is {addr}")
            pass
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.001)
        result = sock.connect_ex((str(addr),int(search_port)))
        sock.close()
        if result == 0:
            print(f"Found client on {addr}")
            clients.append(addr)       
    return clients


if __name__=='__main__':
    start_time=time.time()
    clients=get_client_ips("enp7s0",'AF_INET')
    print(clients)
    print (f"program time is  {time.time() - start_time} seconds")
