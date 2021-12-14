
def check_number_ips(filename):#считает количество ip в файле
    count=0
    file = open(filename,'r')
    while True:
        line = file.readline()
        if not line:
            break
        if "ips" in line and "#ips" not in line and "192.160" in line:
            count+=1
    return count


def correct_file(input_filename, output_filename, clients_dict):
    input_file = open(input_filename, "r")
    output_file = open(output_filename,"w")

    big_cliets_list=[]
    small_cliets_list=[]

    for addr in clients_dict.keys():
        if clients_dict[addr]["scaner_type"]=="Big":
            big_cliets_list.append(addr)
        elif clients_dict[addr]["scaner_type"]=="Small":
            small_cliets_list.append(addr)

    if len(clients_dict.keys())!=check_number_ips(input_filename):
        print("the number of ip addresses in the file and dictionary does not match")
        return "the number of ip addresses in the file and dictionary does not match"


    while True:
        line = input_file.readline()
        if not line:
            break

        if "BIG" in line:
            correct_ips(input_file, output_file, big_cliets_list)

        if "SMALL" in line:
            correct_ips(input_file, output_file, small_cliets_list)
    
    
    
    
def correct_ips(input_file, output_file, clients_list):   
    client_number=0
    while True:
        line = input_file.readline()
        if not line:
            break
        if "ips" in line and "#ips" not in line and "192.160" in line:
            position = line.find("192.160")
            if client_number > len(clients_list):
                print("there are more addresses written in one of the config sections than the program found")
                return "there are more addresses written in one of the config sections than the program found"
            while line[position] != line[position-1]: #удаляем старый ip
                line=line[:position]+line[position+1:]
            line = line[:position]+str(clients_list[client_number])+line[position:] #вставляем новый ip
            #client_number+=1

        
        #в любом случае записываем строку в исправаленный файл
        output_file.write(line)
 
clients_dict ={'192.168.31.88': {'scaner_name': 'scaner1', 'scaner_type': 'Big', 'mac_addr': 'd8:cb:8a:9c:c3:c9'}}
correct_file("c1.txt", "out", clients_dict)











