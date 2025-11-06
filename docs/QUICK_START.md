# Quick Start Guide - ClassChat Task 1

## Setup Instructions

### 1. Clone or Download the Repository
If you have the repository on GitHub:
```bash
git clone <your-repo-url>
cd ClassChat
```

### 2. Verify Python Installation
Make sure Python 3 is installed:
```bash
python3 --version
```
Should show Python 3.6 or higher.

### 3. Test the Installation
```bash
make test
```

## Running ClassChat

### Step 1: Start the Server

Open a terminal window and run:
```bash
cd ClassChat
make server
```

You should see:
```
Starting ClassChat Server...
==================================================
ClassChat Server - Task 1
==================================================
[SERVER] Server started on 127.0.0.1:12345
[SERVER] Waiting for client connection...
```

### Step 2: Start the Client

Open a **NEW** terminal window and run:
```bash
cd ClassChat
make client
```

You should see:
```
Starting ClassChat Client...
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

You: 
```

### Step 3: Send Messages

Type your message and press Enter:
```
You: Hello, this is my first message!
```

The server will respond, and you'll see both in your terminals.

### Step 4: Exit

Type `exit` and press Enter to close the connection:
```
You: exit
```

Both client and server will shut down gracefully.

## Troubleshooting

### Problem: "Address already in use"
**Solution**: Wait 30 seconds and try again, or run:
```bash
lsof -ti:12345 | xargs kill -9
```

### Problem: "Connection refused"
**Solution**: Make sure the server is running first before starting the client.

### Problem: Python not found
**Solution**: Install Python 3:
```bash
sudo apt-get install python3  # Ubuntu/Debian
```

## Alternative: Run Without Makefile

Start server:
```bash
python3 src/server.py
```

Start client (in another terminal):
```bash
python3 src/client.py
```

## What's Next?

After completing Task 1, the next tasks are:
- **Task 2**: Advanced Client with I/O Multiplexing
- **Task 3**: Multi-Thread Communication Server
- **Task 4**: Client-Client Communication

## Need Help?

Check the full documentation:
- `README.md` - Complete project overview
- `docs/TASK1_TECHNICAL_REPORT.md` - Detailed technical documentation

---

Happy Chatting! 🚀
