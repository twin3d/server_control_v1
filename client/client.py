import socket, netifaces, ipaddress

def client_func(target_interface="enp0s31f6",family='AF_INET', port = "51815",debug = True ):

    interface_list=netifaces.interfaces() #получить список интерфейсов
    if debug == True:
        print(interface_list)
    if target_interface not in interface_list:
        print("You have entered the wrong target_interface")


    addrs = netifaces.ifaddresses(target_interface)
    if debug == True:
        #print(f"Addrs is {addrs}")
        pass
    host=addrs[netifaces.AF_INET]
    if debug == True:
        print(f"Host is {host}")
    ipv4=host[0]['addr']
    mask=host[0]['netmask']

    if debug == True:
        print(f"my ip {ipv4}")  

    message = "Hi, glad to see u"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ipv4, int(port)))
    sock.listen(5)
    data=""
    while True:
        conn, addr = sock.accept()
        print("connect done")
        conn.send("Hi, glad to see u".encode('utf8'))
        data = conn.recv(1024)
        print(data.decode("utf8"))
        if (data.decode('utf8')) == message:
            print("he is a good boy!")
        
        conn.close()


if __name__=='__main__':
    client_func()
