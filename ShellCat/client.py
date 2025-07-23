# tcp client to test for services, send garbage data, fuzz.

import socket

target_host = "www.google.com"
target_port = 80

# AF_INET = IPv4 address
# SOCK_STREAM = TCP Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

response = client.recv(4096)

print(response.decode())

client.close()













