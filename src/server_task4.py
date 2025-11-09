#!/usr/bin/env python3
"""
ClassChat Server - Task 4: Client-Client Communication
This server routes messages between clients using JSON protocol.

Core Functions:
1. Client management - Register clients with usernames
2. Receive messages from sending client
3. Forward messages to receiving client
"""

import socket
import sys
import threading
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Client registry: {username: (socket, address)}
clients = {}
clients_lock = threading.Lock()

def broadcast_user_list():
    """Send updated user list to all clients"""
    with clients_lock:
        user_list = list(clients.keys())
        message = json.dumps({
            "status": "user_list",
            "users": user_list
        })
        for username, (client_socket, _) in clients.items():
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                pass

def handle_client(client_socket, address):
    """
    Handle communication with a single client.
    Implements client registration and message routing.
    """
    username = None
    
    try:
        # Step 1: Client Registration
        # Ask for username
        client_socket.send("Enter your username: ".encode('utf-8'))
        username_data = client_socket.recv(1024)
        
        if not username_data:
            client_socket.close()
            return
        
        username = username_data.decode('utf-8').strip()
        
        # Check if username already taken
        with clients_lock:
            if username in clients:
                error_msg = json.dumps({
                    "status": "error",
                    "message": f"Username '{username}' is already taken. Disconnecting..."
                })
                client_socket.send(error_msg.encode('utf-8'))
                client_socket.close()
                return
            
            # Register client
            clients[username] = (client_socket, address)
        
        print(f"[SERVER] {username} connected from {address}")
        
        # Send welcome message
        welcome = json.dumps({
            "status": "success",
            "message": f"Welcome {username}! You are now connected to ClassChat."
        })
        client_socket.send(welcome.encode('utf-8'))
        
        # Notify all clients about new user
        join_notification = json.dumps({
            "status": "system",
            "message": f"{username} has joined the chat"
        })
        with clients_lock:
            for user, (sock, _) in clients.items():
                if user != username:
                    try:
                        sock.send(join_notification.encode('utf-8'))
                    except:
                        pass
        
        # Broadcast updated user list
        broadcast_user_list()
        
        # Step 2 & 3: Receive and Forward Messages
        while True:
            data = client_socket.recv(4096)
            
            if not data:
                print(f"[SERVER] {username} disconnected")
                break
            
            try:
                # Parse JSON message
                message_data = json.loads(data.decode('utf-8'))
                
                # Extract fields
                sender = message_data.get("sender", username)
                receiver = message_data.get("receiver", "")
                text = message_data.get("text", "")
                
                print(f"[MESSAGE] From {sender} to {receiver}: {text}")
                
                # Validate receiver exists
                with clients_lock:
                    if receiver not in clients:
                        # Receiver not found - send error to sender
                        error_response = json.dumps({
                            "status": "error",
                            "message": f"User '{receiver}' is not connected."
                        })
                        client_socket.send(error_response.encode('utf-8'))
                        continue
                    
                    # Get receiver's socket
                    receiver_socket, _ = clients[receiver]
                
                # Forward message to receiver
                forward_message = json.dumps({
                    "status": "message",
                    "sender": sender,
                    "receiver": receiver,
                    "text": text
                })
                
                try:
                    receiver_socket.send(forward_message.encode('utf-8'))
                    
                    # Send confirmation to sender
                    confirmation = json.dumps({
                        "status": "sent",
                        "message": f"Message delivered to {receiver}"
                    })
                    client_socket.send(confirmation.encode('utf-8'))
                    
                except Exception as e:
                    # Failed to send to receiver
                    error_response = json.dumps({
                        "status": "error",
                        "message": f"Failed to deliver message to {receiver}"
                    })
                    client_socket.send(error_response.encode('utf-8'))
            
            except json.JSONDecodeError:
                error_response = json.dumps({
                    "status": "error",
                    "message": "Invalid message format. Please use JSON."
                })
                client_socket.send(error_response.encode('utf-8'))
            
            except Exception as e:
                print(f"[ERROR] {username}: {e}")
                error_response = json.dumps({
                    "status": "error",
                    "message": f"Server error: {str(e)}"
                })
                try:
                    client_socket.send(error_response.encode('utf-8'))
                except:
                    pass
    
    except Exception as e:
        print(f"[ERROR] Client handler error: {e}")
    
    finally:
        # Cleanup: Remove client from registry
        if username:
            with clients_lock:
                if username in clients:
                    del clients[username]
            
            print(f"[SERVER] {username} removed from registry")
            
            # Notify others about disconnect
            leave_notification = json.dumps({
                "status": "system",
                "message": f"{username} has left the chat"
            })
            with clients_lock:
                for user, (sock, _) in clients.items():
                    try:
                        sock.send(leave_notification.encode('utf-8'))
                    except:
                        pass
            
            # Broadcast updated user list
            broadcast_user_list()
        
        client_socket.close()

def start_server():
    """Start the ClassChat server with client-to-client routing"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        
        print("=" * 60)
        print("ClassChat Server - Task 4: Client-Client Communication")
        print("=" * 60)
        print(f"[SERVER] Server started on {HOST}:{PORT}")
        print("[SERVER] Supporting client-to-client messaging with JSON")
        print("[SERVER] Press Ctrl+C to stop\n")
        
        while True:
            client_socket, address = server_socket.accept()
            
            # Create handler thread for this client
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )
            thread.start()
            
            # Display active users
            with clients_lock:
                print(f"[SERVER] Active users: {list(clients.keys())}\n")
    
    except KeyboardInterrupt:
        print("\n[SERVER] Server interrupted by user")
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
    finally:
        # Close all client connections
        with clients_lock:
            for username, (sock, _) in clients.items():
                try:
                    sock.close()
                except:
                    pass
            clients.clear()
        
        server_socket.close()
        print("[SERVER] Server shutdown complete")

def main():
    """Main entry point"""
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
