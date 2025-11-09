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

### ✅ Task 4: Client-Client Communication (30 points)
- **Client Registry**: Server maintains username-to-socket mapping
- **Message Routing**: Server forwards messages from sender to receiver
- **JSON Protocol**: Structured message format with sender, receiver, and text
- **Error Handling**: Validates receiver exists, handles disconnections
- **System Notifications**: Join/leave alerts to all clients
- **User List**: Broadcasts online users to all clients
- **Delivery Confirmation**: Sender receives confirmation when message delivered

### 🔄 Bonus Tasks (Optional)
- ✅ **Bonus 5.1**: Group chatting (10 points) - IMPLEMENTED
- ✅ **Bonus 5.2**: File transfer (10 points) - IMPLEMENTED
- ✅ **Bonus 5.3**: Offline messages (10 points) - IMPLEMENTED
- ⏳ Bonus 5.4: Encryption/Decryption (10 points)

## Project Structure

```
ClassChat/
├── src/
│   ├── server.py                  # Basic server (Task 1)
│   ├── server_multithreaded.py    # Multi-threaded server (Task 3)
│   ├── server_task4.py            # Client-client routing server (Task 4)
│   ├── server_bonus1.py           # Group chatting server (Bonus 5.1)
│   ├── server_bonus2.py           # File transfer server (Bonus 5.2)
│   ├── server_bonus3.py           # Offline messages server (Bonus 5.3) ⭐
│   ├── client.py                  # Basic client with threading (Task 1)
│   ├── client_advanced.py         # Advanced client with select() (Task 2)
│   ├── client_task4.py            # JSON messaging client (Task 4)
│   ├── client_bonus1.py           # Group chat client (Bonus 5.1)
│   ├── client_bonus2.py           # File transfer client (Bonus 5.2)
│   └── client_bonus3.py           # Offline messages client (Bonus 5.3) ⭐
├── docs/
│   └── (documentation files - local only)
├── screenshots/
│   ├── task1/                     # Task 1 demo screenshots and report
│   ├── task2/                     # Task 2 demo screenshots and report
│   ├── task3/                     # Task 3 demo screenshots and report
│   ├── task4/                     # Task 4 demo screenshots and report
│   ├── bonus5.1/                  # Bonus 5.1 demo report
│   └── bonus5.2/                  # Bonus 5.2 demo report
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

### Task 4: Client-Client Communication (30 points)

#### Client-Client Routing Features
- ✅ **Client Registration**: Users register with unique usernames
- ✅ **Client Registry**: Server maintains {username: socket} mapping
- ✅ **Message Routing**: Server forwards messages to specific recipients
- ✅ **JSON Protocol**: Structured format {"sender", "receiver", "text"}
- ✅ **Receiver Validation**: Checks if recipient is online before sending
- ✅ **Error Handling**: Notifies sender if receiver not found
- ✅ **Delivery Confirmation**: Sender gets confirmation when message delivered
- ✅ **System Notifications**: Join/leave alerts broadcast to all users
- ✅ **Online User List**: Broadcasts list of connected users
- ✅ **Username Uniqueness**: Prevents duplicate usernames
- ✅ **Automatic Cleanup**: Removes disconnected users from registry

### Bonus 5.1: Group Chatting (10 points) ⭐

#### Group Chat Features
- ✅ **Group Management**: Create, join, and leave groups dynamically
- ✅ **Group Registry**: Server maintains {group_name: set(members)} mapping
- ✅ **Broadcasting**: Messages sent to @groupname reach all group members
- ✅ **Direct Messaging**: Still supports 1-to-1 messages alongside groups
- ✅ **Group Commands**:
  - `/create groupname` - Create a new group (creator auto-joins)
  - `/join groupname` - Join an existing group
  - `/leave groupname` - Leave a group
  - `/groups` - List all active groups and their members
- ✅ **Message Format**: Group messages use @groupname as receiver
- ✅ **Member Visibility**: All group members can see who's in each group
- ✅ **Auto-cleanup**: Empty groups deleted automatically
- ✅ **Broadcast Confirmation**: Sender knows how many members received message
- ✅ **Use Cases**: 
  - Instructor announces to entire class
  - Students ask questions visible to all
  - Group discussions for team projects
  - Department-wide notifications

### Bonus 5.2: File Transfer (10 points) ⭐

#### File Transfer Features
- ✅ **Binary File Support**: Transfer any file type (documents, images, videos, etc.)
- ✅ **File Metadata**: Includes filename, filesize, and SHA256 checksum
- ✅ **Integrity Verification**: Automatic checksum validation on receipt
- ✅ **Base64 Encoding**: Binary data encoded for JSON transport
- ✅ **Download Management**: Files saved to downloads/ directory automatically
- ✅ **Duplicate Handling**: Auto-rename if file already exists
- ✅ **Size Limit**: 10MB maximum file size for safety
- ✅ **Progress Indication**: Upload and download status messages
- ✅ **Error Handling**: Validates file exists, checks recipient is online
- ✅ **File Command**: `/sendfile` for easy file transfers
- ✅ **All Features**: Maintains direct messaging, group chat alongside file transfer
- ✅ **Use Cases**:
  - Share lecture notes with students
  - Submit assignments to instructor
  - Exchange project files with team members
  - Distribute class materials

### Bonus 5.3: Offline Messages (10 points) ⭐

#### Offline Message Features
- ✅ **Message Queue**: Server stores messages for offline users
- ✅ **Automatic Delivery**: Messages delivered when user reconnects
- ✅ **Timestamps**: All offline messages include send time
- ✅ **Message Count**: Shows number of pending messages
- ✅ **File Support**: Queues both text messages and files
- ✅ **Notification**: User notified about pending messages on connect
- ✅ **Persistent Queue**: Messages remain until delivered
- ✅ **Multiple Messages**: Handles multiple queued messages per user
- ✅ **Thread-Safe**: Queue protected with locks for concurrent access
- ✅ **Status Indication**: Sender knows if message was queued or delivered
- ✅ **All Features**: Works with direct messages, groups, and files
- ✅ **Use Cases**:
  - Instructor assigns project to offline students
  - Students receive announcements when they reconnect
  - Team members leave messages for offline teammates
  - No messages lost due to offline status

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

#### Test Bonus 5.1 (Group Chatting): ⭐
1. Start group server: `make server-bonus1`
2. Open 4 terminals for clients:
   - Terminal 2: `make client-bonus1` → Username: Instructor
   - Terminal 3: `make client-bonus1` → Username: Student1
   - Terminal 4: `make client-bonus1` → Username: Student2
   - Terminal 5: `make client-bonus1` → Username: Student3
3. Instructor creates group:
   - To: `/create class2024`
4. Students join group:
   - To: `/join class2024`
5. Check group membership:
   - To: `/groups`
6. Instructor broadcasts to group:
   - To: `@class2024`
   - Message: `Assignment 3 is due next Friday!`
7. All students receive the broadcast
8. Student1 asks question to group:
   - To: `@class2024`
   - Message: `Can we use Python for the assignment?`
9. Verify all group members (Instructor + Students) see the question
10. Test direct message alongside groups:
    - Instructor to Student1: To: `Student1`, Message: `Yes, Python is allowed`
11. Test leave group: To: `/leave class2024`

### Makefile Commands
```bash
# Core Tasks
make server          # Run the basic server (Task 1)
make server-multi    # Run the multi-threaded server (Task 3)
make server-task4    # Run the client-client routing server (Task 4)
make client          # Run the basic client (Task 1)
make client-advanced # Run the advanced client with select() (Task 2)
make client-task4    # Run the JSON messaging client (Task 4)

# Bonus Tasks
make server-bonus1   # Run the group chatting server (Bonus 5.1) ⭐
make client-bonus1   # Run the group chat client (Bonus 5.1) ⭐

# Utilities
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


