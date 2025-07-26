# tcp client to test for services, send garbage data, fuzz.

import socket

#target_host = "www.google.com"
#target_port = 80
class ShellCat:

    def __init__(self):
        pass

    def tcp_client(self, target_host, target_port, payload):
        try:
            # AF_INET = IPv4 address
            # SOCK_STREAM = TCP Client
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client.connect((target_host, target_port))

            client.send(payload)

            response = client.recv(4096)

            print(response.decode())

            client.close()
        except Exception as e:
            print(e)












