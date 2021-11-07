import socket, netifaces, ipaddress
def handshake(input_interface, default_interface='lo', default_family='AF_INET'):
    flag=0
    interface_list=netifaces.interfaces()#получить список интерфейсов
    print(interface_list)
    for i in interface_list:
        if input_interface==i:
            flag=1
    interface=input_interface
    if flag==0:
        interface=default_interface

    addrs = netifaces.ifaddresses(interface)
    #print(addrs)
    host=addrs[netifaces.AF_INET]
    #print(host)
    ipv4=host[0]['addr']
    mask=host[0]['netmask']
    #print(ipv4, mask)
    
    s=ipv4+"/"+mask
    net = ipaddress.IPv4Network(s, strict=False)
    print("my net is", net)
    
    for addr in net:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(100,300):
            result = sock.connect_ex((str(addr),port))
            if result == 0:
                print ("Port", port, "of", addr, "is open")
            


    
handshake("enp7s0","lo",'AF_INET')
