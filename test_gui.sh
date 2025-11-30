#!/bin/bash
# Quick GUI Test Script for ClassChat

echo "╔════════════════════════════════════════════════════╗"
echo "║     ClassChat GUI Testing - Quick Start Guide     ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check if server is already running
if pgrep -f "server_bonus3.py" > /dev/null; then
    echo "✓ Server is already running"
else
    echo "Starting server..."
    cd "$(dirname "$0")"
    python3 src/server_bonus3.py &
    SERVER_PID=$!
    echo "✓ Server started (PID: $SERVER_PID)"
    sleep 2
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Now launching GUI clients in separate windows..."
echo "═══════════════════════════════════════════════════"
echo ""
echo "Instructions:"
echo "1. Three GUI windows will open"
echo "2. Login as different users:"
echo "   - Window 1: Login as 'Instructor'"
echo "   - Window 2: Login as 'Student1'"
echo "   - Window 3: Login as 'Student2'"
echo ""
echo "3. Test these features:"
echo "   • Send messages between users"
echo "   • Create a group (Instructor)"
echo "   • Join the group (Students)"
echo "   • Send group messages"
echo "   • Transfer a file"
echo "   • Test offline messages (disconnect Student2, send message, reconnect)"
echo ""

read -p "Press Enter to launch GUI clients..."

# Launch GUI clients
echo "Launching GUI Client 1..."
python3 src/client_gui.py &
sleep 1

echo "Launching GUI Client 2..."
python3 src/client_gui.py &
sleep 1

echo "Launching GUI Client 3..."
python3 src/client_gui.py &

echo ""
echo "✓ All GUI clients launched!"
echo ""
echo "═══════════════════════════════════════════════════"
echo "  TESTING CHECKLIST:"
echo "═══════════════════════════════════════════════════"
echo "□ Login with 3 different usernames"
echo "□ Check user list updates automatically"
echo "□ Send direct message (double-click user)"
echo "□ Create a group (Menu: Groups → Create)"
echo "□ Join the group (Menu: Groups → Join)"
echo "□ Send group message (@groupname)"
echo "□ Send a file (select user, click 📁 Send File)"
echo "□ Test offline message:"
echo "  1. Student2 exits"
echo "  2. Instructor sends message to Student2"
echo "  3. Instructor sees '📮 Queued' message"
echo "  4. Student2 reconnects"
echo "  5. Student2 sees '📬 offline messages' notification"
echo ""
echo "Press Ctrl+C in server terminal to stop when done"
echo ""
