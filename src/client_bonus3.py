#!/usr/bin/env python3
"""
ClassChat Client - Bonus Task 5.3: Offline Messages
Supports direct messaging, group chatting, file transfer, and offline message delivery.

Features:
- Direct messages: Send to specific users (even if offline)
- Group messages: Send to @groupname
- File transfer: Send files to specific users
- Offline messages: Receive queued messages on connect
- Group commands: /create, /join, /leave, /groups
"""

import socket
import sys
import threading
import json
import base64
import hashlib
import os

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def calculate_checksum(file_path):
    """Calculate SHA256 checksum of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # Read in 64KB chunks
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[ERROR] Could not calculate checksum: {e}")
        return None

def receive_messages(client_socket, username):
    """
    Receive messages from server in a dedicated thread.
    Handles direct messages, group messages, file transfers, offline messages, and system notifications.
    """
    while True:
        try:
            data = client_socket.recv(1048576)  # 1MB buffer for files
            
            if not data:
                print("\n[CLIENT] Server closed connection")
                break
            
            try:
                # Parse JSON response
                response = json.loads(data.decode('utf-8'))
                status = response.get("status", "")
                
                if status == "message":
                    # Received direct message from another client
                    sender = response.get("sender", "Unknown")
                    text = response.get("text", "")
                    timestamp = response.get("timestamp", "")
                    
                    if timestamp:
                        print(f"\n[{sender}] [{timestamp}] {text}")
                    else:
                        print(f"\n[{sender}] {text}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "group_message":
                    # Received group message
                    group = response.get("group", "Unknown")
                    sender = response.get("sender", "Unknown")
                    text = response.get("text", "")
                    print(f"\n[@{group} - {sender}] {text}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "file_transfer":
                    # Received file from another client
                    sender = response.get("sender", "Unknown")
                    filename = response.get("filename", "unknown_file")
                    filesize = response.get("filesize", 0)
                    checksum = response.get("checksum", "")
                    data_b64 = response.get("data", "")
                    timestamp = response.get("timestamp", "")
                    
                    if timestamp:
                        print(f"\n[FILE RECEIVED] From {sender} [{timestamp}]: {filename} ({filesize} bytes)")
                    else:
                        print(f"\n[FILE RECEIVED] From {sender}: {filename} ({filesize} bytes)")
                    
                    try:
                        # Decode base64 data
                        file_data = base64.b64decode(data_b64)
                        
                        # Verify checksum
                        received_checksum = hashlib.sha256(file_data).hexdigest()
                        if received_checksum != checksum:
                            print(f"[WARNING] Checksum mismatch! File may be corrupted.")
                            print(f"  Expected: {checksum}")
                            print(f"  Received: {received_checksum}")
                        
                        # Save file to downloads directory
                        downloads_dir = "downloads"
                        if not os.path.exists(downloads_dir):
                            os.makedirs(downloads_dir)
                        
                        save_path = os.path.join(downloads_dir, filename)
                        
                        # Avoid overwriting existing files
                        counter = 1
                        base_name, extension = os.path.splitext(filename)
                        while os.path.exists(save_path):
                            save_path = os.path.join(downloads_dir, f"{base_name}_{counter}{extension}")
                            counter += 1
                        
                        with open(save_path, 'wb') as f:
                            f.write(file_data)
                        
                        print(f"[FILE SAVED] {save_path}")
                        if received_checksum == checksum:
                            print(f"[VERIFIED] Checksum OK")
                        
                        if timestamp:
                            print(f"[SENT] {timestamp}")
                    
                    except Exception as e:
                        print(f"[ERROR] Failed to save file: {e}")
                    
                    print(f"To: ", end="", flush=True)
                
                elif status == "offline_messages":
                    # Notification about pending offline messages
                    count = response.get("count", 0)
                    message = response.get("message", "")
                    print(f"\n{'='*60}")
                    print(f"📬 {message}")
                    print(f"{'='*60}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "system":
                    # System notification
                    message = response.get("message", "")
                    print(f"\n[SYSTEM] {message}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "error":
                    # Error message
                    message = response.get("message", "")
                    print(f"\n[ERROR] {message}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "sent":
                    # Message delivery confirmation
                    message = response.get("message", "")
                    if "offline" in message.lower() or "queued" in message.lower():
                        print(f"\n[📮 QUEUED] {message}")
                    else:
                        print(f"\n[✓] {message}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "success":
                    # Command success message
                    message = response.get("message", "")
                    print(f"\n[SUCCESS] {message}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "user_list":
                    # Updated user list
                    users = response.get("users", [])
                    other_users = [u for u in users if u != username]
                    if other_users:
                        print(f"\n[ONLINE USERS] {', '.join(other_users)}")
                        print(f"To: ", end="", flush=True)
                
                elif status == "group_list":
                    # List of groups
                    groups = response.get("groups", {})
                    if groups:
                        print(f"\n[GROUPS]")
                        for group_name, members in groups.items():
                            print(f"  @{group_name}: {', '.join(members)}")
                    else:
                        print(f"\n[GROUPS] No groups created yet")
                    print(f"To: ", end="", flush=True)
                
                elif status == "help":
                    # Help/commands message
                    commands = response.get("commands", {})
                    print(f"\n[COMMANDS]")
                    for cmd, desc in commands.items():
                        print(f"  {cmd}: {desc}")
                    print(f"To: ", end="", flush=True)
                
                else:
                    # Unknown status, display raw message
                    print(f"\n[SERVER] {response.get('message', str(response))}")
                    print(f"To: ", end="", flush=True)
            
            except json.JSONDecodeError:
                # Not JSON, display as plain text
                message = data.decode('utf-8')
                print(f"\n{message}", end="", flush=True)
        
        except Exception as e:
            print(f"\n[ERROR] Receive error: {e}")
            break

def send_file(client_socket, username, receiver, file_path):
    """Send a file to another user (works even if offline)"""
    try:
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return
        
        if not os.path.isfile(file_path):
            print(f"[ERROR] Not a file: {file_path}")
            return
        
        # Get file info
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        
        # Check file size (limit to 10MB for safety)
        if filesize > 10 * 1024 * 1024:
            print(f"[ERROR] File too large. Maximum size is 10MB.")
            return
        
        print(f"[FILE] Sending {filename} ({filesize} bytes) to {receiver}...")
        
        # Read file data
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Calculate checksum
        checksum = hashlib.sha256(file_data).hexdigest()
        
        # Encode to base64 for JSON transport
        data_b64 = base64.b64encode(file_data).decode('utf-8')
        
        # Create file transfer message
        message_data = {
            "type": "file",
            "sender": username,
            "receiver": receiver,
            "file_data": {
                "filename": filename,
                "filesize": filesize,
                "checksum": checksum,
                "data": data_b64
            }
        }
        
        # Send to server
        client_socket.send(json.dumps(message_data).encode('utf-8'))
        print(f"[FILE] Upload complete. Waiting for confirmation...")
    
    except Exception as e:
        print(f"[ERROR] Failed to send file: {e}")

def start_client():
    """Start the ClassChat client with offline message support"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print("=" * 60)
        print("ClassChat Client - Bonus 5.3: Offline Messages")
        print("=" * 60)
        print(f"[CLIENT] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[CLIENT] Connected to server\n")
        
        # Registration: Receive username prompt and respond
        prompt = client_socket.recv(1024).decode('utf-8')
        print(prompt, end="", flush=True)
        
        username = input().strip()
        
        if not username:
            print("[CLIENT] Username cannot be empty")
            return
        
        # Send username to server
        client_socket.send(username.encode('utf-8'))
        
        # Start receiver thread
        receiver_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket, username),
            daemon=True
        )
        receiver_thread.start()
        
        # Give time for welcome and offline messages
        import time
        time.sleep(1.0)
        
        # Display usage instructions
        print("\n" + "=" * 60)
        print("How to use ClassChat:")
        print("=" * 60)
        print("Direct Message (works for offline users too!):")
        print("  1. Enter receiver's username")
        print("  2. Enter your message")
        print("")
        print("Group Message:")
        print("  1. Enter @groupname as receiver")
        print("  2. Enter your message")
        print("")
        print("Send File (works for offline users too!):")
        print("  1. Enter /sendfile as receiver")
        print("  2. Enter username of recipient")
        print("  3. Enter full path to file")
        print("")
        print("Group Commands:")
        print("  /create groupname  - Create a new group")
        print("  /join groupname    - Join an existing group")
        print("  /leave groupname   - Leave a group")
        print("  /groups            - List all groups")
        print("")
        print("💡 Offline Messages: Messages sent to offline users")
        print("   will be queued and delivered when they reconnect!")
        print("")
        print("Type 'exit' as receiver to quit")
        print("=" * 60 + "\n")
        
        # Main message loop
        while True:
            try:
                # Get receiver (username, @group, or command)
                receiver = input("To: ").strip()
                
                if not receiver:
                    continue
                
                if receiver.lower() == 'exit':
                    print("[CLIENT] Disconnecting...")
                    break
                
                # Handle file transfer command
                if receiver == "/sendfile":
                    file_receiver = input("Recipient username: ").strip()
                    if not file_receiver:
                        print("[ERROR] Recipient username cannot be empty")
                        continue
                    
                    file_path = input("File path: ").strip()
                    if not file_path:
                        print("[ERROR] File path cannot be empty")
                        continue
                    
                    send_file(client_socket, username, file_receiver, file_path)
                    continue
                
                # Handle group commands
                if receiver.startswith("/"):
                    # Send command as a message with receiver as command
                    message_data = {
                        "type": "message",
                        "sender": username,
                        "receiver": receiver,
                        "text": ""
                    }
                    client_socket.send(json.dumps(message_data).encode('utf-8'))
                    continue
                
                # Get message text
                message = input("Message: ").strip()
                
                if not message:
                    print("[ERROR] Message cannot be empty")
                    continue
                
                # Create JSON message
                message_data = {
                    "type": "message",
                    "sender": username,
                    "receiver": receiver,
                    "text": message
                }
                
                # Send to server
                client_socket.send(json.dumps(message_data).encode('utf-8'))
                
            except KeyboardInterrupt:
                print("\n[CLIENT] Interrupted by user")
                break
            except Exception as e:
                print(f"[ERROR] Send error: {e}")
                break
    
    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {SERVER_HOST}:{SERVER_PORT}")
        print("[ERROR] Make sure the server is running")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")
    finally:
        client_socket.close()
        print("[CLIENT] Disconnected from server")

def main():
    """Main entry point"""
    try:
        start_client()
    except KeyboardInterrupt:
        print("\n[CLIENT] Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
