
# ClassChat

A TCP/IP-based chat system for classroom communication between students and instructors.

## Features

- Real-time messaging (client-server, client-client)
- Group chat, file transfer, offline messages
- Multi-threaded server for concurrent clients
- GUI client (Tkinter) and CLI clients

## Installation

```bash
git clone https://github.com/bereket2sh/ClassChat.git
cd ClassChat
```

## Usage

Start the server:
```bash
python src/server.py
```
Start a client:
```bash
python src/client.py
```
For advanced features, see other scripts in `src/`.

## Requirements

- Python 3.6+
- Tkinter (for GUI)

## Makefile Commands

```bash
make server          # Run basic server
make client          # Run basic client
make client-gui      # Run GUI client
make clean           # Remove cache files
make help            # List commands
```


## License

Academic use only – Class Project

## Author

Bereket, CSCE 513, November 2025

