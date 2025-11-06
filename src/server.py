#!/usr/bin/env python3
"""
ClassChat Server - Task 1: Basic Client-Server Communication
This server implements TCP/IP socket communication with a single client.
"""

import socket
import sys

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

def create_server():
    """
    Creates and configures a TCP server socket.
    Implements the following steps:
    1. Create a socket for communication
    2. Bind the local port and connection address
    3. Configure TCP protocol with port number
    4. Listen for client connection
    5. Accept connection from client
    6. Send Acknowledgment
    7. Receive message from client
    8. Send message to client
    """
    
    # Step 1: Create a socket for communication
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow socket reuse to avoid "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Step 2 & 3: Bind the local port and connection address with TCP protocol
        server_socket.bind((HOST, PORT))
        print(f"[SERVER] Server started on {HOST}:{PORT}")
        
        # Step 4: Listen for client connection
        # Backlog of 1 means only 1 pending connection (Task 1 requirement)
        server_socket.listen(1)
        print("[SERVER] Waiting for client connection...")
        
        # Step 5: Accept connection from client
        client_socket, client_address = server_socket.accept()
        print(f"[SERVER] Client connected from {client_address}")
        
        # Step 6: Send Acknowledgment
        ack_message = "Connection established. Welcome to ClassChat Server!"
        client_socket.send(ack_message.encode('utf-8'))
        print("[SERVER] Acknowledgment sent to client")
        
        # Communication loop
        while True:
            # Step 7: Receive message from client
            data = client_socket.recv(1024)  # Buffer size of 1024 bytes
            
            if not data:
                print("[SERVER] Client disconnected")
                break
            
            message = data.decode('utf-8')
            print(f"[SERVER] Received from client: {message}")
            
            # Check for exit command
            if message.lower() == 'exit':
                print("[SERVER] Client requested to exit")
                response = "Goodbye! Connection closing..."
                client_socket.send(response.encode('utf-8'))
                break
            
            # Step 8: Send message to client (echo back with confirmation)
            response = f"Server received: {message}"
            client_socket.send(response.encode('utf-8'))
            print(f"[SERVER] Sent to client: {response}")
        
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
    
    finally:
        # Clean up connections
        print("[SERVER] Closing connections...")
        client_socket.close()
        server_socket.close()
        print("[SERVER] Server shutdown complete")

def main():
    """Main entry point for the server"""
    print("=" * 50)
    print("ClassChat Server - Task 1")
    print("=" * 50)
    
    try:
        create_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Server interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
