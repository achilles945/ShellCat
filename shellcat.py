#!/bin/python3

import argparse
import sys
import textwrap
import shellcat.client as client
import shellcat.server as server
import shellcat.udp_client as udpclient
import shellcat.udp_server as udpserver
import shellcat.scanner as scanner

class ShellCat:
	def __init__(self, args):
		self.args = args
		self.target = self.args.pos_target or self.args.target
		self.host = self.args.host
		self.port = args.pos_port or args.port

	def run(self):
		if self.args.udp and self.args.listen and self.target and self.port:
			self.udp_listen()
		elif self.args.udp and self.target and self.port:
			self.upd_send()
		elif self.args.listen and self.target and self.port:
			self.listen()
		elif self.target and self.port:
			self.send()
		elif self.args.scan and self.target and self.args.host:
			self.scan()
		else:
			print("[!] Invalid Arguments")
			parser.print_help()


	def send(self):
		try:
			Client = client.Cat()
			Client.tcp_client(self.target, self.port)
		except Exception as e:
			print(f"[!] TCP Send error: {e}")

	def listen(self):
		try:
			Server = server.Cat(self.args)
			Server.tcp_server(self.target, self.port)
		except Exception as e:
			print(f"[!] TCP Listen error: {e}")
	
	def upd_send(self):
		try:
			Udpclient = udpclient.Cat()
			Udpclient.udp_client_main(self.target, self.port)
		except Exception as e:
			print(f"[!] UDP Send Error: {e}")

	def udp_listen(self):
		try:
			Udpserver = udpserver.Cat()
			Udpserver.udp_server_run(self.target, self.port)
		except Exception as e:
			print(f"[!] UDP Listen error {e}")

	def scan(self):
		try:
			Scanner = scanner.Cat()
			Scanner.Scan(self.target,self.host)
		except Exception as e:
			print(f"[!] Scanner error {e}")


EXAMPLES = textwrap.dedent("""\
Examples:
  # Press CTRL+D to send request

  # Start a Bind Shell (Server Mode)
  python3 shellcat.py -l -t 0.0.0.0 -p 8888 -c

  # Connect as Client (Interactive)
  python3 shellcat.py -t <server-ip> -p 8888

  # Execute Command on connect (Server Mode)
  python3 shellcat.py -l -t 0.0.0.0 -p 4444 -e "uname -a"

  # Scan a Host
  python3 shellcat.py -sc -t <target-ip> -ht <host-ip>

  # Upload a file to server
  # Server:
  python3 shellcat.py -l -u /tmp/upload.bin -p 9001 -t <host-ip>
  # Client:
  cat file.bin | python3 shellcat.py 192.168.1.5 9001

  # Connect to remote server and send raw HTTP request
  python3 shellcat.py www.example.com 80
  GET / HTTP/1.1
  Host: example.com
""")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='ShellCat Net Tool',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=EXAMPLES)
	parser.add_argument('-udp','--udp', action='store_true',help='Use UDP Protocol')
	parser.add_argument('-l','--listen', action='store_true', help='listen mode')
	parser.add_argument('-t', '--target', help='target IP or domain')
	parser.add_argument('-ht', '--host', help='Host IP Address')
	parser.add_argument('-p', '--port', type=int, help='target port')
	parser.add_argument('-sc', '--scan', action='store_true',help= 'Scan Remote IP')
	parser.add_argument('-c','--command', action='store_true', help='command shell')
	parser.add_argument('-e','--execute', help='execute specific command')
	parser.add_argument('-u', '--upload', help='upload file')
	parser.add_argument("pos_target", nargs="?", help="Target (positional)")
	parser.add_argument("pos_port", nargs="?", type=int, help="Port (positional)")
	args = parser.parse_args()

	if args.pos_target:
		args.target = args.pos_target
	if args.pos_port:
		args.port = args.pos_port

	sc = ShellCat(args)
	sc.run()
