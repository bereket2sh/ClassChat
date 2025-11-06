#!/usr/bin/env python3
"""
ClassChat Multi-Threaded Server - Task 3: Multi-Thread Communication Server
This server uses threading to handle multiple concurrent client connections.
Each client gets its own dedicated thread for independent communication.
"""

import socket
import sys
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# Global list to track connected clients
clients = []  # List of (client_socket, address, client_id) tuples
clients_lock = threading.Lock()  # Thread-safe access to clients list
client_counter = 0  # Unique ID for each client

def broadcast_message(message, sender_socket=None):
    """
    Broadcast a message to all connected clients.
    
    Args:
        message: The message to broadcast
        sender_socket: Socket of the sender (to exclude from broadcast if needed)
    """
    with clients_lock:
        for client_socket, _, _ in clients:
            # Optionally skip the sender
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"[ERROR] Failed to send to client: {e}")

def handle_client(client_socket, address, client_id):
    """
    Handle communication with a single client in a dedicated thread.
    
    Args:
        client_socket: The client's socket connection
        address: The client's address (IP, port)
        client_id: Unique identifier for this client
    """
    print(f"[SERVER] Client {client_id} connected from {address}")
    
    # Send welcome message to this client
    welcome_msg = f"Welcome to ClassChat! You are Client {client_id}. Type 'exit' to quit."
    try:
        client_socket.send(welcome_msg.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Failed to send welcome to Client {client_id}: {e}")
        return
    
    # Notify all other clients about the new connection
    join_msg = f"[SYSTEM] Client {client_id} has joined the chat"
    broadcast_message(join_msg, sender_socket=client_socket)
    
    # Communication loop for this client
    try:
        while True:
            # Receive message from client
            data = client_socket.recv(1024)
            
            if not data:
                # Client disconnected
                print(f"[SERVER] Client {client_id} disconnected")
                break
            
            message = data.decode('utf-8').strip()
            print(f"[CLIENT {client_id}] {message}")
            
            # Check for exit command
            if message.lower() == 'exit':
                goodbye_msg = "Goodbye! Disconnecting..."
                client_socket.send(goodbye_msg.encode('utf-8'))
                print(f"[SERVER] Client {client_id} requested to exit")
                break
            
            # Echo message back to sender with confirmation
            response = f"[Server received] {message}"
            client_socket.send(response.encode('utf-8'))
            
            # Optionally broadcast to all other clients (uncomment if needed)
            # broadcast_msg = f"[Client {client_id}] {message}"
            # broadcast_message(broadcast_msg, sender_socket=client_socket)
    
    except ConnectionResetError:
        print(f"[SERVER] Client {client_id} connection reset")
    except Exception as e:
        print(f"[ERROR] Client {client_id} error: {e}")
    
    finally:
        # Remove client from active clients list
        with clients_lock:
            clients[:] = [c for c in clients if c[0] != client_socket]
        
        # Notify others about disconnection
        leave_msg = f"[SYSTEM] Client {client_id} has left the chat"
        broadcast_message(leave_msg)
        
        # Close the client socket
        client_socket.close()
        print(f"[SERVER] Client {client_id} handler thread terminated")

def create_multithreaded_server():
    """
    Creates and runs a multi-threaded TCP server.
    Each client connection is handled in a separate thread.
    """
    global client_counter
    
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind and listen
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Allow up to 5 pending connections
        print(f"[SERVER] Multi-threaded server started on {HOST}:{PORT}")
        print(f"[SERVER] Waiting for client connections...")
        print(f"[SERVER] Press Ctrl+C to stop the server\n")
        
        # Main server loop - accept clients continuously
        while True:
            # Accept new client connection (blocks until client connects)
            client_socket, address = server_socket.accept()
            
            # Assign unique ID to client
            client_counter += 1
            client_id = client_counter
            
            # Add client to the list (thread-safe)
            with clients_lock:
                clients.append((client_socket, address, client_id))
            
            # Create and start a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address, client_id),
                daemon=True  # Thread dies when main program exits
            )
            client_thread.start()
            
            # Display current connection count
            with clients_lock:
                print(f"[SERVER] Active connections: {len(clients)}\n")
    
    except KeyboardInterrupt:
        print("\n[SERVER] Server interrupted by user")
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
    
    finally:
        # Clean shutdown - close all client connections
        print("\n[SERVER] Shutting down...")
        with clients_lock:
            for client_socket, _, client_id in clients:
                try:
                    client_socket.send("Server is shutting down.".encode('utf-8'))
                    client_socket.close()
                except:
                    pass
            clients.clear()
        
        # Close server socket
        server_socket.close()
        print("[SERVER] Server shutdown complete")

def main():
    """Main entry point for the multi-threaded server"""
    print("=" * 60)
    print("ClassChat Multi-Threaded Server - Task 3")
    print("Handles Multiple Concurrent Client Connections")
    print("=" * 60)
    
    try:
        create_multithreaded_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Server interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
