import ipaddress
import os
import socket
import struct
import sys
import time
import threading



MESSAGE = 'PYTHONRULES!'


class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4 
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # human readable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))
            self.protocol = src(self.protocol_num)
    def sniff(host):
        
        socket_protocol = socket.IPPROTO_ICMP
        sniffer = socket.socket(socket.AF_INET, 
                                socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        try:
            while True:
                raw_buffer = sniffer.recvfrom(65535) [0]
                ip_header = IP(raw_buffer[0:20])
                print('Protocol: %s %s -> %s' %
                      (ip_header.protocol, ip_header.src_address,
                       ip_header.dst_address))
        except KeyboardInterrupt:
            sys.exit()

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]
    def sniff(host):
        
        socket_protocol = socket.IPPROTO_ICMP
        sniffer = socket.socket(socket.AF_INET,
                                socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
        try:
            while True:
                raw_buffer = sniffer.recvfrom(65535) [0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == 'ICMP':
                    print('Protocol: %s %s -> %s' %
                          (ip_header.protocol, ip_header.src_address,
                           ip_header.dst_address))
                    #print(f'Version: {ip_header.ver}')
                    print(f'Version: {ip_header.ver}, Header Length: {ip_header.ihl}, TTL:{ip_header.ttl}')

                    # calculate where our ICMP packet starts
                    offset = ip_header.ihl * 4
                    buff = raw_buffer[offset:offset + 8]
                    # create out ICMP structure
                    icmp_header = ICMP(buff)
                    print('ICMP -> Type: %s Code: %s\n' %
                          (icmp_header.type, icmp_header.code))

        except KeyboardInterrupt:
            sys.exit()

def udp_sender(target_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        while True:
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(target_ip), 65212))
            time.sleep(0.5)


class Scanner:
    def __init__(self, host, target_ip):
        self.target_ip = target_ip
        self.host = host
        self.found_target = None
        socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.stop_event = threading.Event()
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    def sniff(self):
        timeout_seconds = 10.0
        timer = threading.Timer(timeout_seconds, self.stop_event.set)
        timer.start()

        try:
            while not self.stop_event.is_set():
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)

                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ip_header.src_address == self.target_ip:
                            if raw_buffer[-len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                tgt = str(ip_header.src_address)
                                print(f'Host Up: {tgt}')
                                self.found_target = tgt
                                self.stop_event.set()
        except KeyboardInterrupt:
            pass

        timer.cancel()


class Cat:

    @staticmethod
    def Scan(target,host_ip):
        target_ip = ipaddress.ip_address(target)
        s = Scanner(host_ip, target_ip)
        time.sleep(1)
        t = threading.Thread(target=udp_sender, args=(target_ip,), daemon=True)
        t.start()
        s.sniff()
