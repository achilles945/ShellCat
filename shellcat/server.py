# tcp server can be used when writing command shells or crafting a proxy

import socket
import threading

#IP = '192.168.105.131'
#PORT = 9998

class ShellCat:

	def __init__(self):
		pass

	def tcp_server(self,IP, PORT):
		try:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.bind((IP, PORT))
			server.listen(5)
			print(f'[*] Listening on {IP}:{PORT}')
			while True:
				client , address = server.accept()
				print(f'[*] Accepted connection from {address[0]}:{address[1]}')
				client_handler = threading.Thread(target=handle_client, args=(client,))
				client_handler.start()
		except Exception as e:
			print(e)
			
	def handle_client(client_socket):
		with client_socket as sock:
			request = sock.recv(1024)
			print(f'[*] Received: {request.decode("utf-8")}')
			sock.send(b'ACK')

#if __name__ == '__main__' :
#	tcp_server(IP, PORT) 

