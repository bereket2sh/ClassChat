#!/usr/bin/env python3
"""
ClassChat Client - Bonus Task 5.1: Group Chatting
This client supports both direct messaging and group broadcasting.

Features:
- Direct messages: Send to specific users
- Group messages: Send to @groupname
- Group commands: /create, /join, /leave, /groups
"""

import socket
import sys
import threading
import json

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def receive_messages(client_socket, username):
    """
    Receive messages from server in a dedicated thread.
    Handles direct messages, group messages, and system notifications.
    """
    while True:
        try:
            data = client_socket.recv(4096)
            
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
                    print(f"\n[{sender}] {text}")
                    print(f"To: ", end="", flush=True)
                
                elif status == "group_message":
                    # Received group message
                    group = response.get("group", "Unknown")
                    sender = response.get("sender", "Unknown")
                    text = response.get("text", "")
                    print(f"\n[@{group} - {sender}] {text}")
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

def start_client():
    """Start the ClassChat client with group chatting support"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print("=" * 60)
        print("ClassChat Client - Bonus 5.1: Group Chatting")
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
        
        # Give time for welcome messages
        import time
        time.sleep(0.5)
        
        # Display usage instructions
        print("\n" + "=" * 60)
        print("How to use ClassChat:")
        print("=" * 60)
        print("Direct Message:")
        print("  1. Enter receiver's username")
        print("  2. Enter your message")
        print("")
        print("Group Message:")
        print("  1. Enter @groupname as receiver")
        print("  2. Enter your message")
        print("")
        print("Group Commands:")
        print("  /create groupname  - Create a new group")
        print("  /join groupname    - Join an existing group")
        print("  /leave groupname   - Leave a group")
        print("  /groups            - List all groups")
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
                
                # Handle group commands
                if receiver.startswith("/"):
                    # Send command as a message with receiver as command
                    message_data = {
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
