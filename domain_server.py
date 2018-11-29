import socket
import sys
from _thread import *

def new_client(c, server_id, DNS_map):

    query = c.recv(1024).decode("utf-8")
    print(query)

    client_id = query.split(",")[0].strip()
    hostname = query.split(",")[1].strip()
    dns_type = query.split(",")[2].strip()

    if DNS_map.__contains__(hostname.lower().replace("www.", "")):
        c.send(('0x00, '+server_id+', '+DNS_map[hostname]).encode("utf-8"))
    else:
        c.send(('0xFF, '+client_id+', Host not found').encode("utf-8"))

    c.close()

def domain_server(server_id, server_port, filename):
    print("This is "+server_id+" server.")
    # Read all the lines into a dict
    DNS_map = {}
    f = open(filename, "r")
    for line in f:
        line = line.strip()

        domain = line.split(" ")[0]
        domain = domain.replace("www.", "")

        ip = line.split(" ")[1]
        DNS_map[domain] = ip

    f.close()

    print(filename+": ")
    print(DNS_map)
    print()

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

        start_new_thread(new_client, (c, server_id, DNS_map)) 


if __name__ == '__main__':
    server_id = sys.argv[1]
    server_port = sys.argv[2]
    mapping_files = sys.argv[3]
    domain_server(server_id, server_port, mapping_files)