#!/usr/bin/env python3
"""
ClassChat Server - Bonus Task 5.1: Group Chatting
Extends Task 4 with group chat functionality for announcements and discussions.

Core Functions:
1. Client management with usernames
2. Group management (create, join, leave)
3. Direct messaging (client-to-client)
4. Group broadcasting (one-to-many)
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

# Group registry: {group_name: set(usernames)}
groups = {}
groups_lock = threading.Lock()

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

def send_group_list(client_socket):
    """Send list of available groups to a client"""
    with groups_lock:
        group_list = {}
        for group_name, members in groups.items():
            group_list[group_name] = list(members)
        
        message = json.dumps({
            "status": "group_list",
            "groups": group_list
        })
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            pass

def create_group(group_name, creator):
    """Create a new group with the creator as first member"""
    with groups_lock:
        if group_name in groups:
            return False, f"Group '{group_name}' already exists"
        
        groups[group_name] = {creator}
        return True, f"Group '{group_name}' created successfully"

def join_group(group_name, username):
    """Add a user to a group"""
    with groups_lock:
        if group_name not in groups:
            return False, f"Group '{group_name}' does not exist"
        
        groups[group_name].add(username)
        return True, f"Joined group '{group_name}'"

def leave_group(group_name, username):
    """Remove a user from a group"""
    with groups_lock:
        if group_name not in groups:
            return False, f"Group '{group_name}' does not exist"
        
        if username not in groups[group_name]:
            return False, f"You are not a member of '{group_name}'"
        
        groups[group_name].remove(username)
        
        # Delete group if empty
        if len(groups[group_name]) == 0:
            del groups[group_name]
            return True, f"Left group '{group_name}' (group deleted - no members)"
        
        return True, f"Left group '{group_name}'"

def broadcast_to_group(group_name, sender, message_text):
    """Send a message to all members of a group"""
    with groups_lock:
        if group_name not in groups:
            return False, f"Group '{group_name}' does not exist"
        
        members = groups[group_name].copy()
    
    # Send to all group members
    success_count = 0
    with clients_lock:
        for member in members:
            if member in clients:
                member_socket, _ = clients[member]
                group_message = json.dumps({
                    "status": "group_message",
                    "group": group_name,
                    "sender": sender,
                    "text": message_text
                })
                try:
                    member_socket.send(group_message.encode('utf-8'))
                    success_count += 1
                except:
                    pass
    
    return True, f"Message sent to {success_count}/{len(members)} members in '{group_name}'"

def handle_client(client_socket, address):
    """
    Handle communication with a single client.
    Supports registration, direct messaging, and group chatting.
    """
    username = None
    
    try:
        # Step 1: Client Registration
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
            "message": f"Welcome {username}! You are now connected to ClassChat with Group Support."
        })
        client_socket.send(welcome.encode('utf-8'))
        
        # Send available commands
        help_msg = json.dumps({
            "status": "help",
            "commands": {
                "Direct message": "Use receiver's username",
                "Group message": "Use @groupname as receiver",
                "Create group": "/create groupname",
                "Join group": "/join groupname",
                "Leave group": "/leave groupname",
                "List groups": "/groups"
            }
        })
        client_socket.send(help_msg.encode('utf-8'))
        
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
        
        # Step 2 & 3: Message and Command Processing
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
                
                # Handle group management commands
                if receiver.startswith("/"):
                    command_parts = receiver.split(maxsplit=1)
                    command = command_parts[0]
                    
                    if command == "/create":
                        if len(command_parts) < 2:
                            response = json.dumps({
                                "status": "error",
                                "message": "Usage: /create groupname"
                            })
                        else:
                            group_name = command_parts[1]
                            success, msg = create_group(group_name, username)
                            response = json.dumps({
                                "status": "success" if success else "error",
                                "message": msg
                            })
                        client_socket.send(response.encode('utf-8'))
                        send_group_list(client_socket)
                    
                    elif command == "/join":
                        if len(command_parts) < 2:
                            response = json.dumps({
                                "status": "error",
                                "message": "Usage: /join groupname"
                            })
                        else:
                            group_name = command_parts[1]
                            success, msg = join_group(group_name, username)
                            response = json.dumps({
                                "status": "success" if success else "error",
                                "message": msg
                            })
                        client_socket.send(response.encode('utf-8'))
                        send_group_list(client_socket)
                    
                    elif command == "/leave":
                        if len(command_parts) < 2:
                            response = json.dumps({
                                "status": "error",
                                "message": "Usage: /leave groupname"
                            })
                        else:
                            group_name = command_parts[1]
                            success, msg = leave_group(group_name, username)
                            response = json.dumps({
                                "status": "success" if success else "error",
                                "message": msg
                            })
                        client_socket.send(response.encode('utf-8'))
                        send_group_list(client_socket)
                    
                    elif command == "/groups":
                        send_group_list(client_socket)
                    
                    else:
                        response = json.dumps({
                            "status": "error",
                            "message": f"Unknown command: {command}"
                        })
                        client_socket.send(response.encode('utf-8'))
                    
                    continue
                
                # Handle group messages (receiver starts with @)
                if receiver.startswith("@"):
                    group_name = receiver[1:]  # Remove @ prefix
                    print(f"[GROUP] {sender} to @{group_name}: {text}")
                    
                    success, msg = broadcast_to_group(group_name, sender, text)
                    response = json.dumps({
                        "status": "success" if success else "error",
                        "message": msg
                    })
                    client_socket.send(response.encode('utf-8'))
                    continue
                
                # Handle direct messages (client-to-client)
                print(f"[DIRECT] From {sender} to {receiver}: {text}")
                
                # Validate receiver exists
                with clients_lock:
                    if receiver not in clients:
                        error_response = json.dumps({
                            "status": "error",
                            "message": f"User '{receiver}' is not connected."
                        })
                        client_socket.send(error_response.encode('utf-8'))
                        continue
                    
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
        # Cleanup: Remove client from all groups
        if username:
            with groups_lock:
                groups_to_delete = []
                for group_name, members in groups.items():
                    if username in members:
                        members.remove(username)
                        if len(members) == 0:
                            groups_to_delete.append(group_name)
                
                for group_name in groups_to_delete:
                    del groups[group_name]
            
            # Remove client from registry
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
    """Start the ClassChat server with group chatting support"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        
        print("=" * 60)
        print("ClassChat Server - Bonus 5.1: Group Chatting")
        print("=" * 60)
        print(f"[SERVER] Server started on {HOST}:{PORT}")
        print("[SERVER] Features: Direct messaging + Group broadcasting")
        print("[SERVER] Commands: /create, /join, /leave, /groups")
        print("[SERVER] Group messages use @groupname format")
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
            
            # Display active users and groups
            with clients_lock:
                print(f"[SERVER] Active users: {list(clients.keys())}")
            with groups_lock:
                if groups:
                    print(f"[SERVER] Active groups: {list(groups.keys())}\n")
                else:
                    print(f"[SERVER] Active groups: None\n")
    
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
        
        groups.clear()
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
