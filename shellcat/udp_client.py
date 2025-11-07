#!/usr/bin/env python3
# shellcat/client.py

import socket
import sys
import threading
import time

# safe default maximum UDP payload (keep under MTU)
MAX_UDP_PAYLOAD = 1400

class Cat:
    def __init__(self, recv_timeout: float = 2.0, max_payload: int = MAX_UDP_PAYLOAD):
        """
        recv_timeout: seconds to wait for a response before looping (prevents recv blocking forever)
        max_payload: maximum bytes to send in a single datagram (prevents fragmentation)
        """
        self.recv_timeout = float(recv_timeout)
        self.max_payload = int(max_payload)

    def recv_loop(self, sock):
        """Receive data from server and print to stdout."""
        try:
            # keep receiving until socket is closed or thread interrupted
            while True:
                try:
                    data = sock.recv(65535)  # connected UDP socket: recv() is fine
                except socket.timeout:
                    # no data this iteration — continue waiting
                    continue
                if not data:
                    break  # peer closed or no data
                # write raw bytes to stdout safely
                try:
                    sys.stdout.buffer.write(data)
                    sys.stdout.flush()
                except Exception:
                    # fallback safe decode
                    sys.stdout.write(data.decode("utf-8", errors="replace"))
                    sys.stdout.flush()
        except Exception as e:
            # print to stderr for debugging
            sys.stderr.write(f"[recv_loop] error: {e}\n")

    def send_loop(self, sock):
        """Send stdin to server until EOF (Ctrl-D). Binary-safe and chunked."""
        try:
            while True:
                chunk = sys.stdin.buffer.read(self.max_payload)
                if not chunk:
                    break
                try:
                    sent = sock.send(chunk)
                    if sent != len(chunk):
                        # partial send on UDP is unusual, warn
                        sys.stderr.write(f"[send_loop] warning: sent {sent}/{len(chunk)} bytes\n")
                except Exception as e:
                    sys.stderr.write(f"[send_loop] send error: {e}\n")
                    break
    
                time.sleep(0)
        except Exception as e:
            sys.stderr.write(f"[send_loop] error reading stdin: {e}\n")

    def udp_client_main(self, host: str, port: int):
        """
        Note: this function uses a UDP socket (SOCK_DGRAM).
        It 'connects' the UDP socket for convenience so recv()/send() may be used.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.settimeout(self.recv_timeout)
            # connect() on UDP sets default peer and allows recv()/send()
            sock.connect((host, port))
        except Exception as e:
            sys.stderr.write(f"[udp_client] socket connect error: {e}\n")
            try:
                sock.close()
            except Exception:
                pass
            return

        # Start receiver in background thread
        t = threading.Thread(target=self.recv_loop, args=(sock,), daemon=True)
        t.start()

        try:
            # Writer runs in main thread
            self.send_loop(sock)

            # give the receiver a short moment to process any final replies
            time.sleep(0.1)
            
            # Wait for receiver to finish (server may still send trailing data)
            t.join(timeout=1.0)
        except KeyboardInterrupt:
            sys.stderr.write("[udp_client] interrupted by user\n")
        except Exception as e:
            sys.stderr.write(f"[udp_client] error: {e}\n")
        finally:
            try:
                sock.close()
            except Exception:
                pass
