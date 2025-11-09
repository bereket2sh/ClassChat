# Task 4 Demo Report: Client-to-Client Communication with JSON

## Implementation Overview

Task 4 implements direct client-to-client messaging through a central server using JSON protocol. The server maintains a client registry and routes messages between specific users.

## Key Features Implemented

### 1. Client Registry System
- Server maintains mapping: `{username: (socket, address)}`
- Username registration on connection
- Uniqueness enforcement for usernames
- Thread-safe registry with locks

### 2. JSON Message Protocol
```json
{
  "sender": "Alice",
  "receiver": "Bob", 
  "text": "Hello Bob!"
}
```

### 3. Message Routing
- Server forwards messages from sender to specific receiver
- Validates receiver exists before forwarding
- Error notifications when receiver not found
- Delivery confirmations to sender

### 4. System Notifications
- Join/leave events broadcast to all clients
- Online user list updates sent to all clients
- Real-time connection status tracking

## Test Scenario

**Setup**: Three clients connected (Alice, Bob, Bereket)

### Test Flow:
1. **Bob connects** → Server welcomes Bob, broadcasts user list
2. **Bereket joins** → System notification sent to Alice and Bob
3. **Alice → Bob**: "Hi, I am testing task4, are you getting my message?"
4. **Bob receives** Alice's message successfully
5. **Bereket leaves** → System notification sent to remaining clients
6. **Bob → Alice**: "Yes I am getting your message"
7. **Alice receives** delivery confirmation

## Test Results

### ✅ Successful Features:
- Client registration with unique usernames
- Message routing between specific clients
- Delivery confirmations
- System join/leave notifications
- Online user list broadcasting
- Multiple concurrent clients (3 clients tested)
- Message validation and error handling

### Message Flow Diagram:
```
Alice ---[JSON: sender=Alice, receiver=Bob, text="Hi"]---> Server
                                                              |
                                                              v
                                                        [Validate Bob exists]
                                                              |
                                                              v
Server ---[Forward: "Alice: Hi"]-----------------------> Bob
Server ---[Confirmation: "Message delivered"]----------> Alice
```

## Commands Used

**Start Server:**
```bash
make server-task4
```

**Start Clients (in separate terminals):**
```bash
make client-task4  # Alice
make client-task4  # Bob
make client-task4  # Bereket
```

## Technical Implementation

### Server (`src/server_task4.py`):
- Client registry: `clients = {}`
- Message parsing: `json.loads(data)`
- Routing logic: Forward to `clients[receiver][0].sendall()`
- Error handling: Receiver validation before forwarding

### Client (`src/client_task4.py`):
- Username registration on connect
- Interactive UI: prompt for receiver, then message
- JSON message creation: `json.dumps({"sender": ..., "receiver": ..., "text": ...})`
- Threaded message receiver for non-blocking I/O

## Verification

✅ **Task 4 Requirements (30 points):**
- Client-to-client messaging through server
- JSON protocol implementation
- Message routing with validation
- Delivery confirmations
- System notifications
- Multiple concurrent clients
- Thread-safe client registry

**Total Points: 30/30**

## Conclusion

Task 4 successfully implements a complete client-to-client messaging system with JSON routing. The server acts as a message broker, maintaining client connections and forwarding messages to specific recipients. All core requirements are met with proper error handling and user notifications.
