#!/usr/bin/env python3
# shellcat/client.py

import socket
import sys
import threading

class Cat:
    def __init__(self):
        pass 

    def recv_loop(self, sock):
        """Receive data from server and print to stdout."""
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break  # peer closed
                sys.stdout.write(data.decode('utf-8', errors='replace'))
                sys.stdout.flush()
        except Exception:
            pass

    def send_loop(self, sock):
        """Send stdin to server until EOF (Ctrl-D)."""
        try:
            for line in sys.stdin.buffer:  
                sock.sendall(line)
            
            try:
                sock.shutdown(socket.SHUT_WR)
            except Exception:
                pass
        except Exception:
            pass

    def tcp_client(self, host: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Start receiver in background thread
        t = threading.Thread(target=self.recv_loop, args=(sock,), daemon=True)
        t.start()

        try:
            # Writer runs in main thread
            self.send_loop(sock)
            # Wait for receiver to finish (server may still send trailing data)
            t.join()
        finally:
            try:
                sock.close()
            except Exception:
                pass
