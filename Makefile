# ClassChat Makefile
# Provides convenient commands to run server, client, and manage the project

.PHONY: server client client-advanced clean help test

# Default target
help:
	@echo "ClassChat - Available Commands:"
	@echo "================================"
	@echo "make server          - Start the ClassChat server"
	@echo "make client          - Start the basic client (Task 1)"
	@echo "make client-advanced - Start the advanced client with select() (Task 2)"
	@echo "make test            - Run basic tests"
	@echo "make clean           - Remove Python cache files"
	@echo "make help            - Show this help message"
	@echo ""
	@echo "Usage:"
	@echo "  1. Open a terminal and run: make server"
	@echo "  2. Open another terminal and run: make client-advanced"

# Run the server
server:
	@echo "Starting ClassChat Server..."
	python3 src/server.py

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
	python3 -m py_compile src/client.py
	python3 -m py_compile src/client_advanced.py
	@echo "All syntax checks passed!"
