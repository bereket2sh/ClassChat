#!/usr/bin/env python3
"""
ClassChat Advanced Client - Task 2: I/O Multiplexing with select()
This client uses select() for efficient I/O multiplexing instead of threading.
Can simultaneously send and receive messages with lower CPU workload.
"""

import socket
import sys
import select

# Server configuration
SERVER_HOST = '127.0.0.1'  # Server IP address
SERVER_PORT = 12345         # Server port number

def create_advanced_client():
    """
    Creates a TCP client using I/O multiplexing with select().
    
    Instead of using threads, this implementation uses select() to monitor
    multiple file descriptors (socket and stdin) simultaneously.
    
    Benefits:
    - Single thread (lower CPU usage)
    - No context switching overhead
    - Event-driven architecture
    - More efficient resource usage
    """
    
    # Create a socket for communication
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print(f"[CLIENT] Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CLIENT] Connected to server successfully")
        
        # Receive acknowledgement from server
        ack_data = client_socket.recv(1024)
        ack_message = ack_data.decode('utf-8')
        print(f"[CLIENT] Server acknowledgment: {ack_message}")
        print("\n" + "=" * 50)
        print("Advanced Client - Using select() I/O Multiplexing")
        print("You can send and receive messages simultaneously.")
        print("Type 'exit' to quit.")
        print("=" * 50 + "\n")
        
        # List of input sources to monitor
        # sys.stdin = keyboard input
        # client_socket = network input from server
        inputs = [sys.stdin, client_socket]
        
        # Main event loop using select()
        running = True
        print("You: ", end="", flush=True)
        
        while running:
            # select() blocks until at least one of the inputs has data
            # Returns three lists: readable, writable, exceptional
            # We only care about readable (which inputs have data ready)
            try:
                # Wait for any input to be ready (socket or keyboard)
                # Timeout is None = block indefinitely until something happens
                readable, _, _ = select.select(inputs, [], [])
                
                # Process each input that has data ready
                for source in readable:
                    
                    # Case 1: Server sent data through socket
                    if source is client_socket:
                        data = client_socket.recv(1024)
                        
                        if not data:
                            # Empty data means server closed connection
                            print("\n[CLIENT] Server closed the connection")
                            running = False
                            break
                        
                        # Decode and display server message
                        message = data.decode('utf-8')
                        print(f"\n[SERVER] {message}")
                        
                        # Check if server sent exit command
                        if message.lower() == 'exit':
                            print("[CLIENT] Server requested to exit")
                            running = False
                            break
                        
                        # Redisplay the input prompt
                        print("You: ", end="", flush=True)
                    
                    # Case 2: User typed something on keyboard
                    elif source is sys.stdin:
                        # Read line from stdin (keyboard)
                        message = sys.stdin.readline().strip()
                        
                        if message:
                            # Send message to server
                            client_socket.send(message.encode('utf-8'))
                            
                            # Check if user wants to exit
                            if message.lower() == 'exit':
                                print("[CLIENT] Closing connection...")
                                running = False
                                break
                        
                        # Redisplay the input prompt
                        print("You: ", end="", flush=True)
            
            except KeyboardInterrupt:
                print("\n[CLIENT] Interrupted by user")
                running = False
                break
            
            except Exception as e:
                print(f"\n[CLIENT ERROR] {e}")
                running = False
                break
    
    except ConnectionRefusedError:
        print("[CLIENT ERROR] Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"[CLIENT ERROR] {e}")
    
    finally:
        # Clean up connection
        print("\n[CLIENT] Closing connection...")
        client_socket.close()
        print("[CLIENT] Client shutdown complete")

def main():
    """Main entry point for the advanced client"""
    print("=" * 50)
    print("ClassChat Advanced Client - Task 2")
    print("I/O Multiplexing with select()")
    print("=" * 50)
    
    try:
        create_advanced_client()
    except KeyboardInterrupt:
        print("\n[CLIENT] Client interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
