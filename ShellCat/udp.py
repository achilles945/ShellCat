# udp client to test for services, send garbage data, fuzz.


import socket

target_host = "127.0.0.1"
target_port = 9997

# AF_INET = IPv4 address
# SOCK_DGRAM = UDP Client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b"AAABBBCCC",(target_host, target_port))

data, addr = client.recvfrom(4096)

print(data.decode())

client.close()
