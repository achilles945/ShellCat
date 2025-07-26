# ShellCat

#### **⚠️ This project is currently in development. Some features and documentation may be incomplete. ⚠️**

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
- Modular Python architecture for easy extension
- Works on Linux, macOS, and Windows



---

## Directory Structure

```
ShellCat/
│
├── ShellCat/                  # Package folder with modules
│   ├── __init__.py
│   ├── client.py
│   ├── server.py
│   ├── proxy.py
│   ├── udp.py
│   ├── executor.py
│   ├── filetransfer.py
│   ├── shell.py
│   ├── scanner.py
│   └── utils.py
│
├── tests/                   # Automated test scripts
│   ├── test_client.py
│   ├── test_server.py
│   ├── test_executor.py
│   ├── test_filetransfer.py
│   ├── test_scanner.py
│   └── test_udp.py
│
├── shellcat.py                # Main CLI script (entrypoint users run)
├── README.md
├── LICENSE
├── requirements.txt
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
│ Send/Receive Data    │◄─────┐      ┌─────►│ Handle Connection Type     │
│ (user input loop)    │      │      │      │ (Shell, Upload, Execute)  │
└──────────────────────┘      │      │      └──────────┬────────────────┘
                              │      │                 │
                              │      │        ┌────────▼────────┐
                              │      │        │ executor.py     │ ← Command execution
                              │      │        ├─────────────────┤
                              │      │        │ filetransfer.py │ ← File upload handler
                              │      │        ├─────────────────┤
                              │      │        │ shell.py        │ ← Interactive shell loop
                              │      │        └─────────────────┘
                              │      │
                              │      ▼
                              │  utils.py  ← Socket helpers, shared tools
                              │
                              ▼
                     scanner.py (optional port scanning)



```


## Example Usage

```bash


```


---

## License

This project is licensed under the MIT License

---
