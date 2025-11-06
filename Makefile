# ClassChat Makefile
# Provides convenient commands to run server, client, and manage the project

.PHONY: server server-multi client client-advanced clean help test

# Default target
help:
	@echo "ClassChat - Available Commands:"
	@echo "================================"
	@echo "make server          - Start the basic server (Task 1)"
	@echo "make server-multi    - Start the multi-threaded server (Task 3)"
	@echo "make client          - Start the basic client (Task 1)"
	@echo "make client-advanced - Start the advanced client with select() (Task 2)"
	@echo "make test            - Run basic tests"
	@echo "make clean           - Remove Python cache files"
	@echo "make help            - Show this help message"
	@echo ""
	@echo "Usage (Multi-threaded server):"
	@echo "  1. Open a terminal and run: make server-multi"
	@echo "  2. Open more terminals and run: make client (or make client-advanced)"
	@echo "  3. Multiple clients can connect simultaneously!"

# Run the server
server:
	@echo "Starting ClassChat Server (Task 1)..."
	python3 src/server.py

# Run the multi-threaded server
server-multi:
	@echo "Starting ClassChat Multi-Threaded Server (Task 3)..."
	python3 src/server_multithreaded.py

# Run the client
client:
	@echo "Starting ClassChat Client (Task 1)..."
	python3 src/client.py

# Run the advanced client with I/O multiplexing
client-advanced:
	@echo "Starting ClassChat Advanced Client (Task 2 - select())..."
	python3 src/client_advanced.py

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
	python3 -m py_compile src/client.py
	python3 -m py_compile src/client_advanced.py
	@echo "All syntax checks passed!"
