#!/usr/bin/env python3
"""
ClassChat Client - Task 4: Client-Client Communication
This client sends JSON messages to other clients through the server.

Message Format:
{
    "sender": "Alice",
    "receiver": "Bob",
    "text": "Hi, do you know how TCP works?"
}
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
    Handles both routed messages and system notifications.
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
                    # Received message from another client
                    sender = response.get("sender", "Unknown")
                    text = response.get("text", "")
                    print(f"\n[{sender}] {text}")
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
                
                elif status == "user_list":
                    # Updated user list
                    users = response.get("users", [])
                    other_users = [u for u in users if u != username]
                    if other_users:
                        print(f"\n[ONLINE] Users: {', '.join(other_users)}")
                        print(f"To: ", end="", flush=True)
                
                elif status == "success":
                    # Welcome or success message
                    message = response.get("message", "")
                    print(f"\n{message}")
                
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
    """Start the ClassChat client with JSON messaging"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print("=" * 60)
        print("ClassChat Client - Task 4: Client-Client Communication")
        print("=" * 60)
        print(f"[CLIENT] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CLIENT] Connected to server\n")
        
        # Receive username prompt
        prompt = client_socket.recv(1024).decode('utf-8')
        print(prompt, end="", flush=True)
        
        # Get username from user
        username = input().strip()
        
        if not username:
            print("[ERROR] Username cannot be empty")
            return
        
        # Send username to server
        client_socket.send(username.encode('utf-8'))
        
        # Start receiver thread
        receiver = threading.Thread(
            target=receive_messages,
            args=(client_socket, username),
            daemon=True
        )
        receiver.start()
        
        # Give receiver time to get welcome message
        import time
        time.sleep(0.5)
        
        # Display instructions
        print("\n" + "=" * 60)
        print("How to send messages:")
        print("  1. Type the receiver's username")
        print("  2. Press Enter")
        print("  3. Type your message")
        print("  4. Press Enter to send")
        print("\nType 'exit' as receiver to quit")
        print("=" * 60 + "\n")
        
        # Main message sending loop
        while True:
            # Get receiver
            receiver_name = input("To: ").strip()
            
            if receiver_name.lower() == 'exit':
                print("[CLIENT] Disconnecting...")
                break
            
            if not receiver_name:
                continue
            
            # Get message text
            text = input("Message: ").strip()
            
            if not text:
                continue
            
            # Create JSON message
            message = json.dumps({
                "sender": username,
                "receiver": receiver_name,
                "text": text
            })
            
            # Send to server
            try:
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] Failed to send: {e}")
                break
    
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Make sure server is running.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print("[CLIENT] Disconnected")

def main():
    """Main entry point"""
    try:
        start_client()
    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
