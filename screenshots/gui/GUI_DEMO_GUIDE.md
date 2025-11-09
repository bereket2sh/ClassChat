# ClassChat GUI Client Demo Guide

## Overview

The GUI client (`client_gui.py`) provides a graphical user interface for ClassChat with all features available in CLI clients, but with an intuitive point-and-click interface.

## Features

### ✅ Complete Feature Set
- Direct messaging (1-to-1)
- Group chatting (broadcast to multiple users)
- File transfer (with progress and checksum verification)
- Offline message delivery (with timestamps)
- Real-time user list
- Real-time group list
- Visual message history with color coding

### ✅ User-Friendly Interface
- Login screen with username entry
- Sidebar with online users and groups
- Scrollable message display area
- Dropdown recipient selector
- File picker dialog for easy file selection
- Menu bar with organized commands
- Status bar showing connection info

### ✅ Visual Enhancements
- Color-coded messages by type
- Emoji indicators (👤 users, 👥 groups, 📁 files, 📬 offline, etc.)
- Timestamps for all messages
- Bold text for usernames
- Italic text for system messages
- Different colors for incoming vs outgoing

## How to Run

### Step 1: Start the Server
```bash
cd ClassChat
python3 src/server_bonus3.py
```

### Step 2: Launch GUI Client(s)
```bash
# In new terminals:
make client-gui
# Or:
python3 src/client_gui.py
```

You can launch multiple GUI clients in separate windows to simulate multiple users.

## GUI Walkthrough

### 1. Login Screen

When you first launch the GUI, you see:
```
┌─────────────────────────────────────┐
│          ClassChat                  │
│   Educational Chat System           │
│                                     │
│  Username: [____________]           │
│                                     │
│         [Connect]                   │
│                                     │
│  Server: 127.0.0.1:12345           │
└─────────────────────────────────────┘
```

**Actions:**
1. Enter your username (no spaces, no @, no /)
2. Press Enter or click "Connect"
3. Wait for connection acknowledgment

### 2. Main Chat Window

After connecting, you see the main interface:

```
┌──────────────────────────────────────────────────────────────┐
│ ClassChat - Connected as: YourUsername                   [X] │
│ File | Groups | Help                                         │
├─────────────────┬────────────────────────────────────────────┤
│ 👤 Online Users │ 💬 Messages                                │
│                 │                                            │
│ Instructor      │ [10:30:15] System:                        │
│ Student1        │   Connected to ClassChat as YourUsername  │
│ Student2        │   Use the dropdown to select user/group   │
│                 │   For groups, use @groupname              │
│ 👥 Groups       │                                            │
│                 │                                            │
│ CS101           │                                            │
│ StudyGroup      │                                            │
│                 │                                            │
│ [🔄 Refresh]    │                                            │
│                 │                                            │
├─────────────────┴────────────────────────────────────────────┤
│ To: [Select User ▼]               [📁 Send File]            │
│ Message: [_________________________]  [Send]                 │
├──────────────────────────────────────────────────────────────┤
│ Connected as YourUsername | 3 user(s) online                │
└──────────────────────────────────────────────────────────────┘
```

### 3. Sending a Direct Message

**Method 1: Using Dropdown**
1. Click the "To:" dropdown
2. Select a username (e.g., "Student1")
3. Type your message in the "Message:" field
4. Press Enter or click "Send"

**Method 2: Using User List**
1. Double-click a username in the left sidebar
2. The recipient is auto-filled
3. Type your message
4. Press Enter or click "Send"

**Method 3: Manual Entry**
1. Type username directly in "To:" field
2. Type message
3. Send

**Result:**
```
💬 Messages
[10:32:00] You → Student1:
  Hello Student1!

[10:32:05] Student1:
  Hi there! How are you?
```

### 4. Sending a Group Message

**Method 1: Using Dropdown**
1. Click "To:" dropdown
2. Select "@GroupName" (note the @ prefix)
3. Type message
4. Send

**Method 2: Using Group List**
1. Double-click group name in left sidebar
2. Recipient auto-filled with "@GroupName"
3. Type message
4. Send

**Result:**
```
💬 Messages
[10:35:00] You → @CS101:
  Class is starting in 5 minutes!

[10:35:10] @CS101 - Student1:
  Thanks for the reminder!
```

### 5. Sending a File

**Method 1: Button**
1. Select recipient first (important!)
2. Click "📁 Send File" button
3. File picker dialog opens
4. Navigate to file
5. Click "Open"
6. File is sent automatically

**Method 2: Menu**
1. Select recipient
2. Click "File" menu → "Send File..."
3. Follow file picker dialog

**Limitations:**
- Files must be under 10MB
- Only works for direct messages (not groups)
- Recipient must be selected first

**Result:**
```
💬 Messages
[10:40:00] 📁 File Sent:
  Sent notes.pdf (245680 bytes) to Student1

[Recipient sees:]
[10:40:01] 📁 File Received:
  From Instructor: notes.pdf (245680 bytes)
  Saved to: downloads/notes.pdf
  ✓ Checksum verified
```

### 6. Managing Groups

#### Create a Group
1. Click "Groups" menu → "Create Group..."
2. Dialog opens: "Group Name: [_______]"
3. Enter group name (no spaces, no @)
4. Click "Create"
5. Group appears in group list

#### Join a Group
1. Click "Groups" menu → "Join Group..."
2. Dialog opens: "Group Name: [_______]"
3. Enter existing group name
4. Click "Join"
5. You can now send/receive messages to/from this group

#### Leave a Group
1. Click "Groups" menu → "Leave Group..."
2. Dialog opens: "Group Name: [_______]"
3. Enter group name you're in
4. Click "Leave"
5. Group removed from your list

#### Refresh Groups
1. Click "Groups" menu → "Refresh Groups"
2. Or click "🔄 Refresh" button in left sidebar
3. Group list updates

### 7. Offline Messages

**Scenario: Someone Sends You Message While Offline**

When you connect after being offline:
```
💬 Messages
============================================================
📬 You have 3 offline message(s)
============================================================

[Instructor] [2025-11-08 14:30:15]
  Assignment 3 is due next Friday

[Student1] [2025-11-08 15:45:00]
  Want to study together?

[📁 FILE RECEIVED] From Instructor [2025-11-08 16:00:00]:
  homework3.pdf (152340 bytes)
  [FILE SAVED] downloads/homework3.pdf
  [VERIFIED] Checksum OK
```

**What You See When Sending to Offline User:**
```
[10:50:00] 📮 Queued:
  Message queued for Student2 (currently offline)
```

The message is stored on the server and delivered when they reconnect.

### 8. Using the Menu Bar

#### File Menu
- **Send File...** - Opens file picker (same as button)
- **Disconnect** - Close connection but keep window open
- **Exit** - Quit application

#### Groups Menu
- **Create Group...** - Dialog to create new group
- **Join Group...** - Dialog to join existing group
- **Leave Group...** - Dialog to leave a group
- **Refresh Groups** - Update group list

#### Help Menu
- **About** - Shows version and feature info

### 9. Color Coding

Messages are color-coded for easy identification:

| Color | Meaning |
|-------|---------|
| **Green Bold** | Messages from other users (incoming) |
| **Purple Bold** | Your messages (outgoing) |
| **Orange Bold** | Group messages |
| **Blue Italic** | System notifications |
| **Gray Italic** | Timestamps and offline messages |
| **Dark Blue** | File transfer notifications |
| **Red** | Error messages |

### 10. Keyboard Shortcuts

- **Enter** in username field → Connect to server
- **Enter** in message field → Send message
- **Double-click** on user → Select as recipient
- **Double-click** on group → Select as recipient

## Common Workflows

### Workflow 1: Instructor Announcement
1. Instructor logs in
2. Creates group "CS101" (Groups → Create Group)
3. Students join "CS101" (Groups → Join Group)
4. Instructor sends: To: @CS101, Message: "Exam next week"
5. All students in CS101 receive the message

### Workflow 2: Student Collaboration
1. Student1 and Student2 are online
2. Student1 double-clicks "Student2" in user list
3. Types: "Want to work on the project together?"
4. Student2 receives message instantly
5. Student2 double-clicks "Student1"
6. Types response

### Workflow 3: File Sharing
1. Instructor has "lecture_slides.pdf"
2. Selects "Student1" from dropdown
3. Clicks "📁 Send File"
4. Selects "lecture_slides.pdf"
5. Student1 sees notification
6. File saved to "downloads/lecture_slides.pdf"

### Workflow 4: Offline Message Delivery
1. Student2 is offline (not connected)
2. Instructor sends: To: Student2, Message: "Check your email"
3. Instructor sees "📮 Queued" notification
4. Later, Student2 connects
5. Student2 immediately sees "📬 You have 1 offline message(s)"
6. Message displayed with original timestamp

## Troubleshooting

### Problem: "Could not connect to server. Is it running?"
**Solution:** Make sure server is running first:
```bash
python3 src/server_bonus3.py
```

### Problem: "Username cannot contain spaces, @, or /"
**Solution:** Use simple usernames like "Instructor", "Student1", "Alice", etc.

### Problem: File picker doesn't open
**Solution:** 
1. Make sure you selected a recipient first
2. Check that tkinter is installed
3. Try using the menu: File → Send File

### Problem: Groups list is empty
**Solution:** 
1. Click "🔄 Refresh" button
2. Or use Groups → Refresh Groups
3. Create a group if none exist

### Problem: Can't see online users
**Solution:** 
1. Users list updates automatically
2. Try reconnecting if list seems stale
3. Check server output to see who's connected

### Problem: Messages not appearing
**Solution:**
1. Check you're connected (status bar shows "Connected")
2. Verify server is running
3. Check if recipient username is correct

## System Requirements

- **Python 3.6+** (any version with tkinter)
- **Tkinter** (usually pre-installed):
  - Linux: `sudo apt-get install python3-tk` (if needed)
  - macOS: Included with Python
  - Windows: Included with Python
- **Operating System**: Windows, macOS, or Linux

## GUI vs Terminal Clients

| Aspect | GUI Client | Terminal Client |
|--------|------------|-----------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Visual Appeal** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Learning Curve** | Minutes | Requires docs |
| **File Selection** | File picker | Type path |
| **User Selection** | Click/dropdown | Type username |
| **Message History** | Scrollable, colored | Scrolls up |
| **Multitasking** | Keep window open | Terminal focused |
| **Resource Usage** | Moderate | Minimal |
| **SSH Compatible** | No | Yes |
| **Automation** | No | Yes |

## Best Practices

1. **Select Recipient First** before sending files
2. **Double-click Users/Groups** for quick selection
3. **Use Refresh** if lists seem outdated
4. **Check Status Bar** to verify connection
5. **Read System Messages** (blue text) for important info
6. **Group Names** should be simple and descriptive
7. **File Names** should be clear (recipient sees original name)
8. **Close Properly** using File → Exit (not window X)

## Demo Script

For a complete demo of all features:

**Terminal 1: Server**
```bash
cd ClassChat
python3 src/server_bonus3.py
```

**Terminal 2: GUI Client 1**
```bash
make client-gui
# Login as "Instructor"
```

**Terminal 3: GUI Client 2**
```bash
make client-gui
# Login as "Student1"
```

**Terminal 4: GUI Client 3**
```bash
make client-gui
# Login as "Student2"
```

**Demo Flow:**
1. All three clients connect → See each other in user list
2. Instructor creates group "CS101"
3. Students join "CS101"
4. Instructor sends message to @CS101
5. Instructor sends direct message to Student1
6. Instructor sends file to Student1
7. Student2 disconnects
8. Instructor sends message to Student2 (gets queued)
9. Student2 reconnects → Receives offline message

## Conclusion

The GUI client provides an intuitive, user-friendly interface for ClassChat that requires no memorization of commands. It's perfect for:
- Classroom demonstrations
- New users
- Quick file transfers
- Visual message tracking
- Multi-user testing

All features from the terminal clients are available with the added benefit of a graphical interface!
