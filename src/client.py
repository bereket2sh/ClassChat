#!/usr/bin/env python3
"""
ClassChat Client - Task 1: Basic Client-Server Communication
This client implements TCP/IP socket communication with the server.
"""

import socket
import sys

# Server configuration
SERVER_HOST = '127.0.0.1'  # Server IP address
SERVER_PORT = 12345         # Server port number

def create_client():
    """
    Creates and configures a TCP client socket.
    Implements the following steps:
    1. Create a socket for communication
    2. Configure TCP protocol with IP address of server and port number
    3. Connect with server through socket
    4. Wait for acknowledgement from server
    5. Send message to the server
    6. Receive message from server
    """
    
    # Step 1: Create a socket for communication
    # AF_INET = IPv4, SOCK_STREAM = TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Step 2 & 3: Configure TCP protocol and connect with server
        print(f"[CLIENT] Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CLIENT] Connected to server successfully")
        
        # Step 4: Wait for acknowledgement from server
        ack_data = client_socket.recv(1024)
        ack_message = ack_data.decode('utf-8')
        print(f"[CLIENT] Server acknowledgment: {ack_message}")
        print("\n" + "=" * 50)
        print("You can now send messages to the server.")
        print("Type 'exit' to quit.")
        print("=" * 50 + "\n")
        
        # Communication loop
        while True:
            # Step 5: Send message to the server
            message = input("You: ")
            
            if not message:
                continue
            
            client_socket.send(message.encode('utf-8'))
            print(f"[CLIENT] Sent to server: {message}")
            
            # Check if user wants to exit
            if message.lower() == 'exit':
                # Step 6: Receive final message from server
                response_data = client_socket.recv(1024)
                response = response_data.decode('utf-8')
                print(f"[CLIENT] Server response: {response}")
                break
            
            # Step 6: Receive message from server
            response_data = client_socket.recv(1024)
            
            if not response_data:
                print("[CLIENT] Server closed the connection")
                break
            
            response = response_data.decode('utf-8')
            print(f"[CLIENT] Server response: {response}\n")
        
    except ConnectionRefusedError:
        print("[CLIENT ERROR] Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"[CLIENT ERROR] {e}")
    
    finally:
        # Clean up connection
        print("[CLIENT] Closing connection...")
        client_socket.close()
        print("[CLIENT] Client shutdown complete")

def main():
    """Main entry point for the client"""
    print("=" * 50)
    print("ClassChat Client - Task 1")
    print("=" * 50)
    
    try:
        create_client()
    except KeyboardInterrupt:
        print("\n[CLIENT] Client interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
