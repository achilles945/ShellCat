# tcp client to test for services, send garbage data, fuzz.

import argparse
import socket
import sys


class Cat:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.buffer = buffer

    def tcp_client(self, target_host, target_port):
        try:
            self.socket.connect((target_host, target_port))
            #if self.buffer:
            #    self.socket.send(self.buffer)
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            return

        try:
            while True:
                #print("\n>>> ")
                lines = []
                while True:
                    try:
                        line = input()
                    except EOFError:
                        # treat Ctrl-D as exit from interactive loop
                        print("\n[!] EOF received — exiting.")
                        return
                    if line == "":
                        break
                    lines.append(line)

                payload = "\r\n".join(lines) + "\r\n\r\n"

                # sendall to ensure full payload is transmitted
                try:
                    self.socket.sendall(payload.encode())
                except BrokenPipeError:
                    print("[!] Broken pipe when sending — remote closed connection.")
                    break
                except Exception as e:
                    print(f"[!] Send error: {e}")
                    break

                response_bytes = bytearray()
                self.socket.settimeout(2)
                try:
                    while True:
                        data = self.socket.recv(4096)
                        if not data:
                            break
                        response_bytes.extend(data)
                except socket.timeout:
                    pass

                # decode once, preserve unknown bytes with replacement
                try:
                    response = response_bytes.decode(errors='replace')
                except Exception:
                    # fallback, should not normally happen
                    response = str(response_bytes)

                print("\n[<] Response:")
                print(response)

        except KeyboardInterrupt:
            print("\n[!] User terminated.")
        finally:
            self.socket.close()
