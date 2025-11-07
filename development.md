# ShellCat

## Files

- client.py
- server.py
- proxy.py
- scanner.py
- udp.py
- executor.py
- filetransfer.py
- shell.py
- utils.py


## Build


- **Basic TCP/UDP Connections**
  - Open TCP connections to a target IP and port.
  - Listen for incoming TCP connections.
  - Support for UDP communication (original netcat).

- **Data Transfer**
  - Send and receive arbitrary data over the network.
  - Transfer files between machines.

- **Port Scanning**
  - Scan remote hosts to identify open ports.

- **Remote Shell**
  - Open an interactive remote command shell.
  - Execute commands remotely and receive output.

- **Port Listening**
  - Bind to a local port and listen for incoming connections.

- **Proxying**
  - Relay traffic from one port to another.

- **Scripting & Automation**
  - Can be scripted to automate network debugging or penetration testing.

- **Chatting**
  - Facilitate simple chat servers and clients over the network.

- **IPv4 and IPv6 Support**
  - Handle connections using both IPv4 and IPv6 addresses.

- **Graceful Connection Handling**
  - Manage connection timeouts, retries, and user interrupts.
