# tcp server can be used when writing command shells or crafting a proxy

import socket
import threading

import shellcat2 
#IP = '192.168.105.131'
#PORT = 9998

class Cat:

	def __init__(self, args):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.args = args

	def tcp_server(self,IP, PORT):
		try:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind((IP, PORT))
			self.socket.listen(5)
			print(f'[*] Listening on {IP}:{PORT}')
			while True:
				client , address = self.socket.accept()
				print(f'[*] Accepted connection from {address[0]}:{address[1]}')
				client_handler = threading.Thread(target=self.handle_client, args=(client,))
				client_handler.start()
		except Exception as e:
			print(e)
			

	def handle_client(self, client_socket):
#		with client_socket as sock:
#			request = sock.recv(1024)
#			print(f'[*] Received: {request.decode("utf-8")}')
#			sock.send(b'ACK')
		if self.args.execute:
			output = execute(self.args.execute)
			client_socket.send(output.encode())
		elif self.args.upload:
			file_buffer = b''
			while True:
				data = client_socket.recv(4096)
				if data:
					file_buffer += data
				else:
					break
			with open(self.args.upload, 'wb') as f:
				f.write(file_buffer)
			message = f'Saved file {self.args.upload}'
			client_socket.send(message.encode())
		elif self.args.command:
			cmd_buffer = b''
			while True:
				try:
					client_socket.send(b'SCAT: #> ')
					while '\n' not in cmd_buffer.decode():
						cmd_buffer += client_socket.recv(64)
					response = execute(cmd_buffer.decode())
					if response:
						client_socket.send(response.encode())
					cmd_buffer = b''
				except Exception as e:
					print(f'server killed {e}')
					self.socket.close()
					sys.exit()




