# tcp server can be used when writing command shells or crafting a proxy
# tcp_server_shell.py
import socket
import threading
import sys
import subprocess
import shlex



class Cat:
    def __init__(self,args):
        self.args = args

    def execute (self, cmd):
        cmd = cmd.strip()
        if not cmd :
            return
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()

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


    def handle(self, client_sock):
        if self.args.execute:
            output = self.execute(self.args.execute)
            client_sock.send(output.encode())
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_sock.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_sock.send(message.encode())
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_sock.send(b'SC: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_sock.recv(64)
                    response = self.execute(cmd_buffer.decode())
                    if response:
                        client_sock.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    sys.exit()


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
            
            if self.args.execute or self.args.command or self.args.upload:
                t_recv = threading.Thread(target=self.handle, args=(client_sock,))
                t_recv.start()

            else:
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
