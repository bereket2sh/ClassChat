# ClassChat Makefile
# Provides convenient commands to run server, client, and manage the project

.PHONY: server client clean help test

# Default target
help:
	@echo "ClassChat - Available Commands:"
	@echo "================================"
	@echo "make server    - Start the ClassChat server"
	@echo "make client    - Start the ClassChat client"
	@echo "make test      - Run basic tests"
	@echo "make clean     - Remove Python cache files"
	@echo "make help      - Show this help message"
	@echo ""
	@echo "Usage:"
	@echo "  1. Open a terminal and run: make server"
	@echo "  2. Open another terminal and run: make client"

# Run the server
server:
	@echo "Starting ClassChat Server..."
	python3 src/server.py

# Run the client
client:
	@echo "Starting ClassChat Client..."
	python3 src/client.py

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
	@echo "All syntax checks passed!"
