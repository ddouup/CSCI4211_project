import socket
import sys
from _thread import *

def new_client(c, server_id, DNS_map):
	while True:
		try:
			output = c.recv(1024).decode("utf-8")
			if output == 'q':
				print("Client closing...")
				break

			log_file = open(server_id+'.log','a+')
			print(output)
			log_file.write(output+'\n')
			log_file.close()

			try:
				client_id = output.split(", ")[0]
				hostname = output.split(", ")[1]
				dns_type = output.split(", ")[2]
				
				if dns_type != 'I' and dns_type != 'R':
					raise e

				if DNS_map.__contains__(hostname):
					c.send(('0x00, '+server_id+', '+DNS_map[hostname]).encode("utf-8"))
				else:
					c.send(('0xFF, '+client_id+', Host not found').encode("utf-8"))

			except Exception as e:
				print(e)
				print("Invalid format")
				c.send(('0xEE, '+client_id+', Invalid format').encode("utf-8"))


		except KeyboardInterrupt:
			print()
			print("KeyboardInterrupt")
			c.send('q'.encode("utf-8"))
			c.close()
			sys.exit(0)

	c.send('Connection closed.'.encode("utf-8"))
	c.close()



def local_server(server_id, server_port, mapping_files, servers_list):
	
	# Read all the lines into a dict
	DNS_map = {}
	f = open(mapping_files, "r")
	for line in f:
		line = line.strip()
		domain = line.split(" ")[0]
		ip = line.split(" ")[1]
		DNS_map[domain] = ip
	f.close()
	print(DNS_map)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	host = '0.0.0.0'	#listen on this pc
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
	mapping_files = sys.argv[3] # (com.dat, gov.dat, or org.dat)
	servers_list = sys.argv[4]
	local_server(server_id, server_port, mapping_files, servers_list)