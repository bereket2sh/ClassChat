# ClassChat Makefile
# Provides convenient commands to run server, client, and manage the project

.PHONY: server server-multi server-task4 server-bonus1 server-bonus2 client client-advanced client-task4 client-bonus1 client-bonus2 clean help test

# Default target
help:
	@echo "ClassChat - Available Commands:"
	@echo "================================"
	@echo "Core Tasks:"
	@echo "  make server          - Start the basic server (Task 1)"
	@echo "  make server-multi    - Start the multi-threaded server (Task 3)"
	@echo "  make server-task4    - Start client-client routing server (Task 4)"
	@echo "  make client          - Start the basic client (Task 1)"
	@echo "  make client-advanced - Start the advanced client with select() (Task 2)"
	@echo "  make client-task4    - Start the client-client messaging client (Task 4)"
	@echo ""
	@echo "Bonus Tasks:"
	@echo "  make server-bonus1   - Start server with group chatting (Bonus 5.1)"
	@echo "  make client-bonus1   - Start client with group support (Bonus 5.1)"
	@echo "  make server-bonus2   - Start server with file transfer (Bonus 5.2) ⭐"
	@echo "  make client-bonus2   - Start client with file transfer (Bonus 5.2) ⭐"
	@echo ""
	@echo "Utilities:"
	@echo "  make test            - Run basic tests"
	@echo "  make clean           - Remove Python cache files"
	@echo "  make help            - Show this help message"
	@echo ""
	@echo "Usage (Bonus 5.1 - Group Chatting):"
	@echo "  1. Terminal 1: make server-bonus1"
	@echo "  2. Terminal 2: make client-bonus1  (Instructor)"
	@echo "  3. Terminal 3: make client-bonus1  (Student1)"
	@echo "  4. Terminal 4: make client-bonus1  (Student2)"
	@echo "  5. Instructor: /create class2024"
	@echo "  6. Students: /join class2024"
	@echo "  7. Instructor sends to @class2024 - all students receive!"
	@echo ""
	@echo "Usage (Bonus 5.2 - File Transfer):"
	@echo "  1. Terminal 1: make server-bonus2"
	@echo "  2. Terminal 2: make client-bonus2  (Alice)"
	@echo "  3. Terminal 3: make client-bonus2  (Bob)"
	@echo "  4. Alice: To: /sendfile → Recipient: Bob → File: document.pdf"
	@echo "  5. Bob receives file in downloads/ folder with checksum verification!"

# Run the server
server:
	@echo "Starting ClassChat Server (Task 1)..."
	python3 src/server.py

# Run the multi-threaded server
server-multi:
	@echo "Starting ClassChat Multi-Threaded Server (Task 3)..."
	python3 src/server_multithreaded.py

# Run the Task 4 server with client-to-client routing
server-task4:
	@echo "Starting ClassChat Task 4 Server (Client-Client Routing)..."
	python3 src/server_task4.py

# Run the Bonus 5.1 server with group chatting
server-bonus1:
	@echo "Starting ClassChat Bonus 5.1 Server (Group Chatting)..."
	python3 src/server_bonus1.py

# Run the Bonus 5.2 server with file transfer
server-bonus2:
	@echo "Starting ClassChat Bonus 5.2 Server (File Transfer)..."
	python3 src/server_bonus2.py

# Run the client
client:
	@echo "Starting ClassChat Client (Task 1)..."
	python3 src/client.py

# Run the advanced client with I/O multiplexing
client-advanced:
	@echo "Starting ClassChat Advanced Client (Task 2 - select())..."
	python3 src/client_advanced.py

# Run the Task 4 client with JSON messaging
client-task4:
	@echo "Starting ClassChat Task 4 Client (Client-Client Messaging)..."
	python3 src/client_task4.py

# Run the Bonus 5.1 client with group support
client-bonus1:
	@echo "Starting ClassChat Bonus 5.1 Client (Group Chatting)..."
	python3 src/client_bonus1.py

# Run the Bonus 5.2 client with file transfer
client-bonus2:
	@echo "Starting ClassChat Bonus 5.2 Client (File Transfer)..."
	python3 src/client_bonus2.py

# Clean Python cache files
clean:
	@echo "Cleaning up Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Clean complete!"

# Basic test to verify Python files syntax
test:
	@echo "Running syntax checks..."
	python3 -m py_compile src/server.py
	python3 -m py_compile src/server_multithreaded.py
	python3 -m py_compile src/server_task4.py
	python3 -m py_compile src/server_bonus1.py
	python3 -m py_compile src/server_bonus2.py
	python3 -m py_compile src/client.py
	python3 -m py_compile src/client_advanced.py
	python3 -m py_compile src/client_task4.py
	python3 -m py_compile src/client_bonus1.py
	python3 -m py_compile src/client_bonus2.py
	@echo "All syntax checks passed!"
	python3 -m py_compile src/client_advanced.py
	python3 -m py_compile src/client_task4.py
	python3 -m py_compile src/client_bonus1.py
	@echo "All syntax checks passed!"
