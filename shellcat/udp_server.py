#!/usr/bin/env python3
# shellcat/server.py

import socket
import sys
import threading

MAX_UDP_PAYLOAD = 1400

class Cat:
    def __init__(self):
        self.sock = None
        self.running = False
        self.last_client = None   # store last client (addr, port)

    def _recv_loop(self):
        """Receive data -> print to stdout -> remember sender."""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
            except socket.timeout:
                continue
            except Exception:
                break

            if not data:
                continue

            # remember last sender so server can reply from stdin
            self.last_client = addr

            # print received data
            try:
                sys.stdout.buffer.write(data + b"\n")
                sys.stdout.flush()
            except Exception:
                sys.stdout.write(data.decode("utf-8", errors="replace") + "\n")
                sys.stdout.flush()

    def udp_server_run(self, host: str, port: int):
        """
        Start UDP server.
        Receives -> prints to stdout.
        Reads stdin -> sends to last client received from.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.settimeout(1.0)

        self.running = True
        sys.stderr.write(f"[*] UDP server listening on {host}:{port}\n")
        sys.stderr.flush()

        # background receiver thread
        t = threading.Thread(target=self._recv_loop, daemon=True)
        t.start()

        try:
            # stdin -> send to last known client
            for line in sys.stdin.buffer:
                if self.last_client:
                    payload = line[:MAX_UDP_PAYLOAD]
                    self.sock.sendto(payload, self.last_client)
        except KeyboardInterrupt:
            pass

        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass

        sys.stderr.write("[*] Server stopped\n")
        sys.stderr.flush()
