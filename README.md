# ClassChat System

A TCP/IP-based online chat system for class communications and discussions between students and instructors.

## Project Overview

ClassChat is designed to facilitate real-time communication among students in a class setting. This project implements a client-server architecture using socket programming with TCP/IP protocol.

## Current Implementation Status

### ✅ Task 1: Client-Server Communication using TCP/IP (30 points)
- **Server Implementation**: Complete TCP server with socket creation, binding, listening, and message handling
- **Client Implementation**: Complete TCP client with connection, send/receive capabilities using threading
- **Protocol**: TCP/IP with proper acknowledgment system
- **Bidirectional Communication**: Both server and client can send/receive messages simultaneously

### ✅ Task 2: Advanced Client with I/O Multiplexing (20 points)
- **I/O Multiplexing**: Implemented using `select()` system call
- **Single-threaded**: No threading overhead, lower CPU usage
- **Event-driven**: Monitors both socket and keyboard input simultaneously
- **Efficient**: Waits for events instead of busy polling or blocking

### ✅ Task 3: Multi-Thread Communication Server (20 points)
- **Threading Model**: Each client gets dedicated thread for independent communication
- **Concurrent Connections**: Supports multiple clients simultaneously
- **Thread Management**: Automatic thread creation and cleanup
- **Client Tracking**: Thread-safe client list management with locks
- **Scalable**: Can handle many concurrent connections efficiently

### 🔄 Upcoming Tasks
- Task 4: Client-Client Communication (30 points)
- Bonus Tasks: Group chatting, file transfer, offline messages, encryption

## Project Structure

```
ClassChat/
├── src/
│   ├── server.py                  # Basic server (Task 1)
│   ├── server_multithreaded.py    # Multi-threaded server (Task 3)
│   ├── client.py                  # Basic client with threading (Task 1)
│   └── client_advanced.py         # Advanced client with select() (Task 2)
├── docs/
│   └── (documentation files - local only)
├── screenshots/
│   ├── task1/                     # Task 1 demo screenshots and report
│   └── task2/                     # Task 2 demo screenshots and report
├── README.md
├── Makefile
├── verify.sh
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

#### Option 1: Basic Server (Task 1 - Single Client)
```bash
make server
# Or directly:
python3 src/server.py
```

#### Option 2: Multi-Threaded Server (Task 3 - Multiple Clients) ⭐ RECOMMENDED
```bash
make server-multi
# Or directly:
python3 src/server_multithreaded.py
```

The server will start listening on `127.0.0.1:12345` and wait for client connections.

### Running the Client

#### Option 1: Basic Client (Task 1 - with Threading)
```bash
make client
# Or directly:
python3 src/client.py
```

#### Option 2: Advanced Client (Task 2 - with select())
```bash
make client-advanced
# Or directly:
python3 src/client_advanced.py
```

Both clients will connect to the server and you can start sending messages.

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

## Features

### Task 1: Basic Client-Server Communication (30 points)

#### Server Features
- ✅ Socket creation for communication
- ✅ Port binding and address configuration
- ✅ TCP protocol configuration
- ✅ Listening for client connections
- ✅ Accepting client connections
- ✅ Sending acknowledgment messages
- ✅ Receiving messages from clients
- ✅ Sending messages to clients (bidirectional)
- ✅ Threading for simultaneous send/receive
- ✅ Graceful connection handling

#### Client Features (Basic)
- ✅ Socket creation for communication
- ✅ TCP protocol configuration
- ✅ Server connection establishment
- ✅ Acknowledgment reception
- ✅ Message sending to server
- ✅ Response reception from server
- ✅ Threading for simultaneous operations
- ✅ Interactive command-line interface
- ✅ Exit command support

### Task 2: Advanced Client with I/O Multiplexing (20 points)

#### Advanced Client Features
- ✅ **I/O Multiplexing with select()**: Single-threaded event-driven architecture
- ✅ **Lower CPU Usage**: No threading overhead or context switching
- ✅ **Simultaneous Monitoring**: Watches both socket and stdin at the same time
- ✅ **Event-driven**: Reacts immediately when either input has data
- ✅ **System Callback**: Uses OS-level select() for efficient waiting
- ✅ **Same Functionality**: Send and receive messages just like threaded version
- ✅ **More Efficient**: Better resource utilization for I/O operations

### Task 3: Multi-Thread Communication Server (20 points)

#### Multi-Threaded Server Features
- ✅ **Multiple Concurrent Clients**: Supports unlimited simultaneous connections
- ✅ **Threading Model**: Each client gets its own dedicated thread
- ✅ **Thread-Safe Operations**: Uses locks for client list management
- ✅ **Automatic Thread Management**: Creates and cleans up threads automatically
- ✅ **Client Tracking**: Maintains list of all active connections
- ✅ **Broadcast Capability**: Can send messages to all connected clients
- ✅ **System Notifications**: Alerts when clients join/leave
- ✅ **Unique Client IDs**: Each client gets a unique identifier
- ✅ **Graceful Shutdown**: Properly closes all connections on exit
- ✅ **Scalable Architecture**: Foundation for real chat application

## Technical Implementation

### Server Architecture (Basic - Task 1)
- **Socket Type**: TCP (SOCK_STREAM)
- **Address Family**: IPv4 (AF_INET)
- **Host**: 127.0.0.1 (localhost)
- **Port**: 12345
- **Buffer Size**: 1024 bytes
- **Connection Backlog**: 1 (single client)
- **Concurrency**: Threading for send/receive

### Multi-Threaded Server Architecture (Task 3)
- **Socket Type**: TCP (SOCK_STREAM)
- **Address Family**: IPv4 (AF_INET)
- **Host**: 127.0.0.1 (localhost)
- **Port**: 12345
- **Connection Backlog**: 5 (up to 5 pending connections)
- **Threading**: One thread per client (daemon threads)
- **Client Management**: Thread-safe list with threading.Lock()
- **Scalability**: Handles multiple concurrent clients independently

### Client Architecture (Basic - Task 1)
- **Socket Type**: TCP (SOCK_STREAM)
- **Address Family**: IPv4 (AF_INET)
- **Server Connection**: 127.0.0.1:12345
- **Buffer Size**: 1024 bytes
- **Encoding**: UTF-8
- **Concurrency**: Threading (separate threads for send/receive)

### Advanced Client Architecture (Task 2)
- **Socket Type**: TCP (SOCK_STREAM)
- **I/O Multiplexing**: select() system call
- **Monitored Inputs**: [sys.stdin, client_socket]
- **Event-driven**: Single thread, waits for any input to be ready
- **No Threading**: Lower CPU usage, no context switching
- **Buffer Size**: 1024 bytes
- **Encoding**: UTF-8

## Development

### Testing

#### Test Task 1 & 2:
1. Start basic server: `make server`
2. Start a client:
   - Basic client (Task 1): `make client`
   - Advanced client (Task 2): `make client-advanced`
3. Send messages from both server and client
4. Verify bidirectional communication

#### Test Task 3 (Multi-threaded Server): ⭐
1. Start multi-threaded server: `make server-multi`
2. Open multiple terminals and start clients:
   - Terminal 2: `make client`
   - Terminal 3: `make client`
   - Terminal 4: `make client-advanced`
   - Terminal 5: `make client-advanced`
3. Send messages from different clients
4. Verify all clients connected simultaneously
5. Disconnect one client, verify others still connected
6. Test exit command

### Makefile Commands
```bash
make server          # Run the basic server (Task 1)
make server-multi    # Run the multi-threaded server (Task 3) ⭐
make client          # Run the basic client (Task 1)
make client-advanced # Run the advanced client with select() (Task 2)
make test            # Run syntax checks
make clean           # Clean up Python cache files
make help            # Show all available commands
```

## AI/ChatGPT Usage

This project was developed with AI assistance for:
- **Code structure and organization**: Used AI to design clean, modular code architecture
- **Documentation**: Generated comprehensive comments and docstrings
- **Best practices**: Applied Python socket programming best practices
- **Error handling**: Implemented robust exception handling mechanisms


## License

Academic use only - Class Project

## Authors

- Bereket
- Class: CSCE 513
- Date: November 5, 2025


