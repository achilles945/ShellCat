# ShellCat


**ShellCat** is a powerful, Python-based Netcat clone designed for hackers, developers, and network engineers.  
It offers everything you expect from traditional Netcat — plus the flexibility of Python.

Easily create reverse shells, transfer files, scan ports, or pipe raw data — all from one portable CLI tool.

> - _Stream. Shell. Transfer. Scan. Dominate the network._

---


## Why ShellCat?

Whether you're building your own backdoor, testing network security, or automating dev tools —  
**ShellCat** gives you full control over network sockets in a familiar, scriptable way.

Built for flexibility. Inspired by Netcat. Powered by Python.

---

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Logic](#logic)
- [Example Usage](#example-usage)
- [License](#license)

---

## Features

- Remote command execution & interactive shells
- File upload and transfer
- TCP port scanning (built-in)
- TCP client/server communication
- UDP client/server communication
- Python architecture for easy extension
- Works on Linux based Operating Systems


---

## Directory Structure

```
ShellCat/
│
├── ShellCat/                  # Package folder with modules
│   ├── __init__.py
│   ├── client.py
│   ├── server.py
│   ├── udp_client.py
│   ├── udp_server.py
│   ├── scanner.py
│
├── shellcat.py                # Main CLI script (entrypoint users run)
├── README.md
├── LICENSE
└── setup.py                 # Optional: if you package/install your tool

```

---


## Logic

```

                          ┌────────────────┐
                          │  shellcat.py   │   ← Main CLI entrypoint
                          └──────┬─────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Parse CLI Arguments    │
                    └────────────┬────────────┘
                                 │
            ┌────────────────────┴────────────────────┐
            │                                         │
   ┌────────▼────────┐                      ┌─────────▼────────┐
   │   Client Mode   │                      │   Server Mode    │
   │  (client.py)    │                      │  (server.py)     │
   └──────┬──────────┘                      └─────────┬────────┘
          │                                            │
  ┌───────▼───────────┐                        ┌───────▼────────────────┐
  │ Connect to Target │                        │ Listen & Accept Client │
  └───────┬───────────┘                        └───────┬────────────────┘
          │                                            │
          ▼                                            ▼
┌──────────────────────┐                    ┌────────────────────────────┐
│ Send/Receive Data    │◄─────┐             │ Handle Connection Type     │
│ (user input loop)    │      │             │ (Shell, Upload, Execute)   │
└──────────────────────┘      │             └────────────────────────────┘
                              │                       
                              │
                              ▼
                     scanner.py (optional port scanning)



```


## Example Usage

```bash
# Press CTRL+D to send request

# Start a Bind Shell (Server Mode)
python3 shellcat.py -l -t 0.0.0.0 -p 8888 -c

# Connect as Client(Interactive)
python3 shellcat.py -t <server-ip> -p 8888

# Execute Command on connect (Server Mode)
python3 shellcat.py 0.0.0.0 4444 -l -e "uname -a"

# Scan a Host
python3 shellcat.py -sc <target ip> -ht <host-ip>


# Upload a file to server
# Server
python3 shellcat.py -l -u /tmp/upload.bin -p 9001 -t host-ip

# Client
cat file.bin | python3 shellcat.py 192.168.1.5 9001


# Connect to remote server
python3 shellcat.py wwww.example.com 80
GET / HTTP/1.1
Host:example.com

```


---

## License

This project is licensed under the MIT License

---
