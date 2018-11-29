import socket
import sys
from _thread import *

def new_client(c, server_id, Servers_list):

    query = c.recv(1024).decode("utf-8")
    print(query)

    client_id = query.split(",")[0].strip()
    hostname = query.split(",")[1].strip()
    dns_type = query.split(",")[2].strip()

    domain = hostname.split(".")[-1].strip()

    if dns_type == 'I':
        if Servers_list.__contains__(domain):
            respond = '0x01, '+server_id+', '+Servers_list[domain]['ip']+', '+Servers_list[domain]['port']
            c.send(respond.encode("utf-8"))

        else:
            respond = '0xFF, '+client_id+', Server not found'
            c.send(respond.encode("utf-8"))

    elif dns_type == 'R':
        s = socket.socket()

        ip = Servers_list[domain]['ip']
        port = Servers_list[domain]['port']
        query = server_id+', '+hostname+', '+dns_type

        s.connect((ip, int(port)))

        print("Connecting to "+ip+":"+str(port)+"...")
        print(s.recv(1024).decode("utf-8"))
        print()
        print("Sending query: "+query)
        s.send(query.encode("utf-8"))

        respond = s.recv(1024).decode("utf-8")
        s.close()

        print("Receive respond from domain server: ")
        print(respond)
        
        c.send(respond.encode("utf-8"))


    c.close()



def root_server(server_id, server_port, servers_list):
    
    # Read all the lines into a dict
    Servers_list = {}
    f = open(servers_list, "r")
    for line in f:
        line = line.strip()

        domain = line.split(" ")[0]
        ip = line.split(" ")[1]
        port = line.split(" ")[2]

        server = {}
        server['ip'] = ip
        server['port'] = port

        Servers_list[domain] = server

    f.close()

    print("Server List:")
    print(Servers_list)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = '0.0.0.0'    #listen on this pc
    port = int(server_port)
    s.bind((host, port))
    print("socket binded to post", port) 


    s.listen(5)
    print("socket is listening") 

    while True:
        c, addr = s.accept()

        print('Got connection from', addr)
        c.send('Connection created. Welcome!'.encode("utf-8"))

        start_new_thread(new_client, (c, server_id, Servers_list)) 


if __name__ == '__main__':
    server_id = sys.argv[1]
    server_port = sys.argv[2]
    servers_list = sys.argv[3]
    root_server(server_id, server_port, servers_list)