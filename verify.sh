#!/bin/bash
# Quick verification script for ClassChat Task 1

echo "=================================="
echo "ClassChat Task 1 Verification"
echo "=================================="
echo ""

# Check Python installation
echo "1. Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "   ✓ $python_version installed"
else
    echo "   ✗ Python 3 not found!"
    exit 1
fi
echo ""

# Check project structure
echo "2. Checking project structure..."
required_files=("src/server.py" "src/client.py" "Makefile" "README.md")
all_found=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file NOT FOUND"
        all_found=false
    fi
done
echo ""

# Check Python syntax
echo "3. Checking Python syntax..."
if python3 -m py_compile src/server.py 2>/dev/null; then
    echo "   ✓ server.py syntax OK"
else
    echo "   ✗ server.py has syntax errors"
    all_found=false
fi

if python3 -m py_compile src/client.py 2>/dev/null; then
    echo "   ✓ client.py syntax OK"
else
    echo "   ✗ client.py has syntax errors"
    all_found=false
fi
echo ""

# Check git repository
echo "4. Checking git repository..."
if [ -d ".git" ]; then
    echo "   ✓ Git repository initialized"
    commit_count=$(git rev-list --count HEAD 2>/dev/null)
    echo "   ✓ Commits: $commit_count"
else
    echo "   ✗ Git repository not initialized"
    all_found=false
fi
echo ""

# Final result
echo "=================================="
if [ "$all_found" = true ]; then
    echo "✅ All checks passed!"
    echo ""
    echo "Next steps:"
    echo "1. Create a GitHub repository"
    echo "2. Follow docs/GITHUB_SETUP.md"
    echo "3. Run: git remote add origin <your-repo-url>"
    echo "4. Run: git push -u origin master"
    echo ""
    echo "To test the chat system:"
    echo "  Terminal 1: make server"
    echo "  Terminal 2: make client"
else
    echo "❌ Some checks failed!"
    echo "Please review the errors above."
fi
echo "=================================="
