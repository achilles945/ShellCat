# tcp server can be used when writing command shells or crafting a proxy
# tcp_server_shell.py
import socket
import threading
import sys

class Cat:
    def __init__(self):
        pass

    def handle_client_recv(self, client_sock):
        """Read from client and dump to local stdout."""
        try:
            while True:
                data = client_sock.recv(4096)
                if not data:
                    break  # client closed
                sys.stdout.write(data.decode('utf-8', errors='replace'))
                sys.stdout.flush()
        except Exception:
            pass
        finally:
            try:
                client_sock.close()
            except Exception:
                pass

    def handle_client_send(self, client_sock):
        """Read local stdin and send to client until EOF (Ctrl-D)."""
        try:
            for line in sys.stdin.buffer:   # bytes lines
                client_sock.sendall(line)
            # finished sending; optionally half-close
            try:
                client_sock.shutdown(socket.SHUT_WR)
            except Exception:
                pass
        except Exception:
            pass

    def tcp_server(self, IP, PORT):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((IP, PORT))
        srv.listen(5)
        print(f'[*] Listening on {IP}:{PORT} — waiting for one client')

        try:
            client_sock, addr = srv.accept()
            print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

            # start receiver thread (client -> stdout)
            t_recv = threading.Thread(target=self.handle_client_recv, args=(client_sock,), daemon=True)
            t_recv.start()

            # main thread will handle sending (stdin -> client)
            self.handle_client_send(client_sock)

            # wait for receiver to finish
            t_recv.join()
        finally:
            try:
                srv.close()
            except Exception:
                pass
