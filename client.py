import socket
import sys

def client(client_id, server_ip, server_port):
	s = socket.socket()

	s.connect((server_ip, int(server_port)))

	print(s.recv(1024).decode("utf-8"))

	log_file = open(client_id+'.log','w')

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

			s.send(query.encode("utf-8"))

			output = s.recv(1024).decode("utf-8")
			print(output)

			if output == 'q':
				print("Server closed exceptionally.")
				s.close()
				sys.exit(0)

			log_file.write(output+'\n')

		except KeyboardInterrupt:
			print()
			print("KeyboardInterrupt")
			s.send('q'.encode("utf-8"))
			sys.exit(0)

	print(s.recv(1024).decode("utf-8"))
	print("Exit")
	log_file.close()
	s.close()

if __name__ == '__main__':
	client_id = sys.argv[1]
	server_ip = sys.argv[2]
	server_port = sys.argv[3]
	client(client_id, server_ip, server_port)