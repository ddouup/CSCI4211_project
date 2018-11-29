'''
Name of file: client.py
Short description of program: 

Name: DOU Daihui
ID: 5514178
Email: dou00005@umn.edu
'''

import socket
import sys

def writetoLog(filename, line):
    print("Write to: "+filename)
    print(line)
    print()
    with open(filename, 'a+') as log_file:
        log_file.write(line+'\n')

def client(client_id, server_ip, server_port):
    s = socket.socket()

    s.connect((server_ip, int(server_port)))

    print(s.recv(1024).decode("utf-8"))

    while True:
        try:
            
            query = input('Please input the DNS query in the following format: CLIENT_ID, HOSTNAME, I/R\nInput q to exit\n:')
            if query == 'q':
                s.send('q'.encode("utf-8"))
                break

            if query == '':
                print("Please input something")
                print()
                continue

            writetoLog(client_id+'.log', query)

            s.send(query.encode("utf-8"))

            respond = s.recv(1024).decode("utf-8")
            print(respond)
            print()

            if respond == 'q':
                print("Server closed exceptionally.")
                s.close()
                sys.exit(0)

            writetoLog(client_id+'.log', respond+"\n")

        except KeyboardInterrupt:
            print()
            print("KeyboardInterrupt")
            s.send('q'.encode("utf-8"))
            sys.exit(0)

    print(s.recv(1024).decode("utf-8"))
    print("Exit")
    s.close()

if __name__ == '__main__':
    client_id = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = sys.argv[3]
    client(client_id, server_ip, server_port)