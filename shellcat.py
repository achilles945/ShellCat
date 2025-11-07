#!/bin/python3

import argparse
import sys
import shellcat.client as client
import shellcat.server as server
import shellcat.udp_client as udpclient
import shellcat.udp_server as udpserver

class ShellCat:
	def __init__(self, args, target, port):
		self.args = args
		self.target = target
		self.port = port
		self.client = client.Cat()
		self.server = server.Cat()
		self.udpclient = udpclient.Cat()
		self.udpserver = udpserver.Cat()

	def run(self):
		if self.args.udp and self.args.listen:
			self.udp_listen()
		elif self.args.udp:
			self.upd_send()
		elif self.args.listen:
			self.listen()
		elif self.target and self.port:
			self.send()


	def send(self):
		try:
			self.client.tcp_client(self.target, self.port)
		except Exception as e:
			print(f"[!] TCP Send error: {e}")

	def listen(self):
		try:
			self.server.tcp_server(self.target, self.port)
		except Exception as e:
			print(f"[!] TCP Listen error: {e}")
	
	def upd_send(self):
		try:
			self.udpclient.udp_client_main(self.target, self.port)
		except Exception as e:
			print(f"[!] UDP Send Error: {e}")

	def udp_listen(self):
		try:
			self.udpserver.udp_server_run(self.target, self.port)
		except Exception as e:
			print(f"[!] UDP Listen error {e}")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='ShellCat Net Tool',
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-udp','--udp', action='store_true',help='Use UDP Protocol')
	parser.add_argument('-l','--listen', action='store_true', help='listen mode')
	parser.add_argument('-t', '--target', help='target IP or domain')
	parser.add_argument('-p', '--port', type=int, help='target port')
	parser.add_argument('-c','--command', action='store_true', help='command shell')
	parser.add_argument('-e','--execute', help='execute specific command')
	parser.add_argument('-u', '--upload', help='upload file')
	parser.add_argument("pos_target", nargs="?", help="Target (positional)")
	parser.add_argument("pos_port", nargs="?", type=int, help="Port (positional)")
	args = parser.parse_args()

	target = args.pos_target or args.target
	port = args.pos_port or args.port

	if not target or not port:
		parser.error("You must provide a target and port, either as flags or positional arguments.")

	sc = ShellCat(args, target, port)
	sc.run()
