import socket

def main():
	s = socket.socket() 
	host = socket.gethostname()
	port = 12345
	s.bind((host, port))

	s.listen(10)
	while True:
		c, addr = s.accept()
		c.send('Welcome')
		c.close()

if __name__ == '__main__':
	main()