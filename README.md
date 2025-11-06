# ClassChat System

A TCP/IP-based online chat system for class communications and discussions between students and instructors.

## Project Overview

ClassChat is designed to facilitate real-time communication among students in a class setting. This project implements a client-server architecture using socket programming with TCP/IP protocol.

## Current Implementation Status

### ✅ Task 1: Client-Server Communication using TCP/IP (30 points)
- **Server Implementation**: Complete TCP server with socket creation, binding, listening, and message handling
- **Client Implementation**: Complete TCP client with connection, send/receive capabilities
- **Protocol**: TCP/IP with proper acknowledgment system

### 🔄 Upcoming Tasks
- Task 2: Advanced Client with I/O Multiplexing (20 points)
- Task 3: Multi-Thread Communication Server (20 points)
- Task 4: Client-Client Communication (30 points)
- Bonus Tasks: Group chatting, file transfer, offline messages, encryption

## Project Structure

```
ClassChat/
├── src/
│   ├── server.py          # TCP server implementation
│   └── client.py          # TCP client implementation
├── docs/
│   └── (documentation files)
├── screenshots/
│   └── (demo screenshots)
├── README.md
├── Makefile
└── .gitignore
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses built-in `socket` module)

## Installation

1. Clone the repository:
```bash
git clone <your-github-repo-url>
cd ClassChat
```

2. Make the scripts executable (optional):
```bash
chmod +x src/server.py src/client.py
```

## Usage

### Running the Server

Open a terminal and run:
```bash
make server
# Or directly:
python3 src/server.py
```

The server will start listening on `127.0.0.1:12345` and wait for client connections.

### Running the Client

Open another terminal and run:
```bash
make client
# Or directly:
python3 src/client.py
```

The client will connect to the server and you can start sending messages.

### Example Session

**Server Output:**
```
==================================================
ClassChat Server - Task 1
==================================================
[SERVER] Server started on 127.0.0.1:12345
[SERVER] Waiting for client connection...
[SERVER] Client connected from ('127.0.0.1', 54321)
[SERVER] Acknowledgment sent to client
[SERVER] Received from client: Hello, Server!
[SERVER] Sent to client: Server received: Hello, Server!
```

**Client Output:**
```
==================================================
ClassChat Client - Task 1
==================================================
[CLIENT] Connecting to server at 127.0.0.1:12345...
[CLIENT] Connected to server successfully
[CLIENT] Server acknowledgment: Connection established. Welcome to ClassChat Server!

==================================================
You can now send messages to the server.
Type 'exit' to quit.
==================================================

You: Hello, Server!
[CLIENT] Sent to server: Hello, Server!
[CLIENT] Server response: Server received: Hello, Server!
```

## Features (Task 1)

### Server Features
- ✅ Socket creation for communication
- ✅ Port binding and address configuration
- ✅ TCP protocol configuration
- ✅ Listening for client connections
- ✅ Accepting client connections
- ✅ Sending acknowledgment messages
- ✅ Receiving messages from clients
- ✅ Sending responses to clients
- ✅ Graceful connection handling

### Client Features
- ✅ Socket creation for communication
- ✅ TCP protocol configuration
- ✅ Server connection establishment
- ✅ Acknowledgment reception
- ✅ Message sending to server
- ✅ Response reception from server
- ✅ Interactive command-line interface
- ✅ Exit command support

## Technical Implementation

### Server Architecture
- **Socket Type**: TCP (SOCK_STREAM)
- **Address Family**: IPv4 (AF_INET)
- **Host**: 127.0.0.1 (localhost)
- **Port**: 12345
- **Buffer Size**: 1024 bytes
- **Connection Backlog**: 1 (Task 1 single client)

### Client Architecture
- **Socket Type**: TCP (SOCK_STREAM)
- **Address Family**: IPv4 (AF_INET)
- **Server Connection**: 127.0.0.1:12345
- **Buffer Size**: 1024 bytes
- **Encoding**: UTF-8

## Development

### Testing
To test the implementation:
1. Start the server in one terminal
2. Start the client in another terminal
3. Send various messages from client to server
4. Verify bidirectional communication
5. Test the exit command

### Makefile Commands
```bash
make server    # Run the server
make client    # Run the client
make clean     # Clean up Python cache files
```

## AI/ChatGPT Usage

This project was developed with AI assistance for:
- **Code structure and organization**: Used AI to design clean, modular code architecture
- **Documentation**: Generated comprehensive comments and docstrings
- **Best practices**: Applied Python socket programming best practices
- **Error handling**: Implemented robust exception handling mechanisms

### Learning Outcomes
- Understanding of TCP/IP socket programming fundamentals
- Client-server architecture design patterns
- Network communication protocols and handshaking
- Error handling in distributed systems
- Python's socket module and network programming APIs

## Contributing

This is an academic project. For questions or issues, please contact the development team.

## License

Academic use only - Class Project

## Authors

- [Your Name]
- Class: [Your Class Name]
- Date: November 5, 2025

## Acknowledgments

- Python Socket Programming Documentation
- TCP/IP Protocol Specifications
- Course materials and guidelines
