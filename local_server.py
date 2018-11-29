'''
Name of file: local_server.py
Short description of program: 

Name: DOU Daihui
ID: 5514178
Email: dou00005@umn.edu
'''

import socket
import sys
import os
from _thread import *

ROOT_IP = '127.0.0.1'
ROOT_PORT = 5353

def readDNSMap(filename):
    DNS_map = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            domain = line.split(" ")[0].lower().replace("www.", "")

            ip = line.split(" ")[1]
            DNS_map[domain] = ip
    return  DNS_map

def writetoLog(filename, line):
    print("Write to: "+filename)
    print(line)
    print()
    with open(filename, 'a+') as log_file:
        log_file.write(line+'\n')



def Query(ip, port, query):
    s = socket.socket()
    s.connect((ip, int(port)))
    print("Connecting to "+ip+":"+str(port)+"...")
    print(s.recv(1024).decode("utf-8"))
    print()
    print("Sending query: "+query)
    print()
    s.send(query.encode("utf-8"))
    respond = s.recv(1024).decode("utf-8")
    s.close()
    
    return respond



def new_client(c, server_id, DNS_map, Domains):
    while True:
        try:
            query = c.recv(1024).decode("utf-8")
            if query == 'q':
                print("Client closing...")
                writetoLog(server_id+'.log', "")
                break

            print("Receive query from client")
            writetoLog(server_id+'.log', query)

            try:
                client_id = query.split(",")[0].strip()
                hostname = query.split(",")[1].strip()
                dns_type = query.split(",")[2].strip()
            except Exception as e:
                print(e)
                respond = '0xEE, '+server_id+', Invalid format'
                writetoLog(server_id+'.log', respond)

                print("Sending error to client")
                c.send(respond.encode("utf-8"))
                writetoLog(server_id+'.log', "")
                print("------------------------------------")  
                continue
            
            # Check the query format
            valid = True
            if dns_type != 'I' and dns_type != 'R':
                valid = False

            if not hostname.split(".")[-1].lower() in Domains:
                valid = False
                
            if valid == False:
                respond = '0xEE, '+server_id+', Invalid format'
                writetoLog(server_id+'.log', respond)

                print("Sending error to client")
                c.send(respond.encode("utf-8"))
                writetoLog(server_id+'.log', "")
                print("------------------------------------")  
                continue


            # Check cache first
            DNS_map_cache = {}
            if os.path.exists("mapping.log"):
                DNS_map_cache = readDNSMap("mapping.log")

            # Case insensitive & "www." not necessary
            h = hostname.lower().replace("www.", "")
            if h in DNS_map_cache or h in DNS_map:
                respond = '0x00, '+server_id+', '+DNS_map[h]
                writetoLog(server_id+'.log', respond+"\n")
                c.send(respond.encode("utf-8"))
                print("------------------------------------")  

            else:
                query = server_id+', '+hostname+', '+dns_type

                print("Sending query to root server")
                writetoLog(server_id+'.log', query)

                respond = Query(ROOT_IP, ROOT_PORT, query)

                print("Receive respond from root server")
                writetoLog(server_id+'.log', respond)

                if respond.split(",")[0].strip() == '0x01':
                    # Iterative query, forward to domain DNS server
                    
                    domain_ip = respond.split(",")[2].strip()
                    domain_port = respond.split(",")[3].strip()

                    print("Sending query to domain server")
                    writetoLog(server_id+'.log', query)

                    respond = Query(domain_ip, domain_port, query)

                    print("Receive respond to domain server")
                    writetoLog(server_id+'.log', respond)
                    
                    # Cache and espond to client
                    if respond.split(",")[0].strip() != "0xFF":
                        cache = hostname+" "+respond.split(",")[2].strip()
                        writetoLog("mapping.log", cache)

                    res = respond.split(",")[0].strip()+", "+server_id+", "+ respond.split(",")[2].strip()
                    print("Sending respond to client")
                    c.send(res.encode("utf-8"))
                    writetoLog(server_id+'.log', "")
                    print("------------------------------------")            
                    
                else:
                    # Recursive query, cache and respond to client
                    if respond.split(",")[0].strip() != "0xFF":
                        cache = hostname+" "+respond.split(",")[2].strip()
                        writetoLog("mapping.log", cache)

                    res = respond.split(",")[0].strip()+", "+server_id+", "+ respond.split(",")[2].strip()
                    print("Sending respond to client")
                    c.send(res.encode("utf-8"))
                    writetoLog(server_id+'.log', "")
                    print("------------------------------------")


        except KeyboardInterrupt:
            print()
            print("KeyboardInterrupt")
            print("Sending q to clients...")
            c.send('q'.encode("utf-8"))
            c.close()
            sys.exit(0)

    c.send('Connection closed.'.encode("utf-8"))
    c.close()



def local_server(server_id, server_port, filename):
    
    # Read all the lines into a dict
    DNS_map = readDNSMap(filename)

    print("Default DNS mappings:")
    print(DNS_map)

    Domains = ['com','gov','org']

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

        start_new_thread(new_client, (c, server_id, DNS_map, Domains)) 


if __name__ == '__main__':
    server_id = sys.argv[1]
    server_port = sys.argv[2]
    mapping_files = sys.argv[3]
    local_server(server_id, server_port, mapping_files)