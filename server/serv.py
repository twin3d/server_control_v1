import socket, netifaces, ipaddress
from joblib import Parallel, delayed

def get_client_ips( target_interface="enp7s0", family='AF_INET', search_port = "51815" , debug = False):
    """ 1. What I do
        2. What I need 

    Args:
        target_interface (str, optional): [description]. Defaults to "enp7s0".
        family (str, optional): [description]. Defaults to 'AF_INET'.
        search_port (str, optional): [description]. Defaults to "51815".
        debug (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """

    clients = []

    interface_list=netifaces.interfaces() #получить список интерфейсов
    #print(interface_list)
    if target_interface not in interface_list:
        print("You have entered the wrong target_interface")
        return "NO_INTERFACE"

    addrs = netifaces.ifaddresses(target_interface)
    if debug == True:
        print(f"Addrs is {addrs}")
    host=addrs[netifaces.AF_INET]
    if debug == True:
        print(f"Host is {host}")
    ipv4=host[0]['addr']
    mask=host[0]['netmask']
    if debug == True:
        print(f"Iv4 is {ipv4}/{mask}")
    
    s=ipv4+"/"+mask
    net = ipaddress.IPv4Network(s, strict=False)
    if debug == True:
        print("my net is", net)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for addr in net:
        if debug == True:
            print(f"ip is {addr}")
        result = sock.connect_ex((str(addr),int(search_port)))
        if result == 0:
            print(f"Found client on {addr}")
            clients.append(addr)
    return clients

    '''
    for addr in net:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(100,300):
            result = sock.connect_ex((str(addr),port))
            if result == 0:
                print ("Port", port, "of", addr, "is open")
    '''       


if __name__=='__main__':
    get_client_ips("enp7s0",'AF_INET')
