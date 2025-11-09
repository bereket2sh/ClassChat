#!/usr/bin/env python3
"""
ClassChat GUI Client
====================
A graphical user interface for ClassChat supporting all features:
- Direct messaging
- Group chatting
- File transfer
- Offline message delivery
- Real-time user list

Built with Tkinter (cross-platform, built into Python)
Compatible with server_bonus3.py
"""

import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import base64
import hashlib
from datetime import datetime

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

class ClassChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ClassChat")
        self.root.geometry("900x650")
        self.root.minsize(800, 500)
        
        # Client state
        self.client_socket = None
        self.username = None
        self.connected = False
        self.online_users = set()
        self.groups = set()
        
        # Setup UI
        self.setup_login_screen()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_login_screen(self):
        """Create login interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Center frame
        login_frame = ttk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = ttk.Label(login_frame, text="ClassChat", font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Subtitle
        subtitle = ttk.Label(login_frame, text="Educational Chat System", font=('Arial', 10))
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Username input
        ttk.Label(login_frame, text="Username:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.username_entry = ttk.Entry(login_frame, font=('Arial', 12), width=20)
        self.username_entry.grid(row=2, column=1, padx=10, pady=10)
        self.username_entry.focus()
        
        # Connect button
        self.connect_btn = ttk.Button(login_frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Status label
        self.login_status = ttk.Label(login_frame, text="", foreground='red')
        self.login_status.grid(row=4, column=0, columnspan=2)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.connect_to_server())
        
        # Server info
        info_label = ttk.Label(login_frame, text=f"Server: {HOST}:{PORT}", font=('Arial', 8), foreground='gray')
        info_label.grid(row=5, column=0, columnspan=2, pady=20)
    
    def connect_to_server(self):
        """Connect to the ClassChat server"""
        username = self.username_entry.get().strip()
        
        if not username:
            self.login_status.config(text="Please enter a username")
            return
        
        if ' ' in username or '@' in username or '/' in username:
            self.login_status.config(text="Username cannot contain spaces, @, or /")
            return
        
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            
            # Send username
            self.client_socket.send(username.encode('utf-8'))
            
            # Wait for acknowledgment
            ack = self.client_socket.recv(1024).decode('utf-8')
            
            if "successfully" in ack.lower():
                self.username = username
                self.connected = True
                self.setup_chat_screen()
                
                # Start receive thread
                receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
                receive_thread.start()
            else:
                self.login_status.config(text=ack)
                self.client_socket.close()
        
        except ConnectionRefusedError:
            self.login_status.config(text="Could not connect to server. Is it running?")
        except Exception as e:
            self.login_status.config(text=f"Connection error: {e}")
    
    def setup_chat_screen(self):
        """Create main chat interface"""
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"ClassChat - {self.username}")
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Send File...", command=self.send_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Disconnect", command=self.disconnect)
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Groups menu
        groups_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Groups", menu=groups_menu)
        groups_menu.add_command(label="Create Group...", command=self.create_group_dialog)
        groups_menu.add_command(label="Join Group...", command=self.join_group_dialog)
        groups_menu.add_command(label="Leave Group...", command=self.leave_group_dialog)
        groups_menu.add_command(label="Refresh Groups", command=self.list_groups)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Users and Groups
        left_panel = ttk.Frame(main_container, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Online Users section
        users_label = ttk.Label(left_panel, text="👤 Online Users", font=('Arial', 10, 'bold'))
        users_label.pack(pady=(0, 5))
        
        users_frame = ttk.Frame(left_panel)
        users_frame.pack(fill=tk.BOTH, expand=True)
        
        self.users_listbox = tk.Listbox(users_frame, height=10, font=('Arial', 10))
        users_scrollbar = ttk.Scrollbar(users_frame, orient=tk.VERTICAL, command=self.users_listbox.yview)
        self.users_listbox.config(yscrollcommand=users_scrollbar.set)
        self.users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        users_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to message user
        self.users_listbox.bind('<Double-Button-1>', self.select_user_from_list)
        
        # Groups section
        groups_label = ttk.Label(left_panel, text="👥 Groups", font=('Arial', 10, 'bold'))
        groups_label.pack(pady=(10, 5))
        
        groups_frame = ttk.Frame(left_panel)
        groups_frame.pack(fill=tk.BOTH, expand=True)
        
        self.groups_listbox = tk.Listbox(groups_frame, height=8, font=('Arial', 10))
        groups_scrollbar = ttk.Scrollbar(groups_frame, orient=tk.VERTICAL, command=self.groups_listbox.yview)
        self.groups_listbox.config(yscrollcommand=groups_scrollbar.set)
        self.groups_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        groups_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to message group
        self.groups_listbox.bind('<Double-Button-1>', self.select_group_from_list)
        
        # Refresh button
        refresh_btn = ttk.Button(left_panel, text="🔄 Refresh", command=self.refresh_all)
        refresh_btn.pack(pady=5, fill=tk.X)
        
        # Right panel - Chat
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat display
        chat_label = ttk.Label(right_panel, text="💬 Messages", font=('Arial', 10, 'bold'))
        chat_label.pack(pady=(0, 5))
        
        self.chat_display = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=('Arial', 10),
            state=tk.DISABLED,
            height=20
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_config('system', foreground='blue', font=('Arial', 9, 'italic'))
        self.chat_display.tag_config('incoming', foreground='green', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('outgoing', foreground='purple', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('group', foreground='orange', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('offline', foreground='gray', font=('Arial', 9, 'italic'))
        self.chat_display.tag_config('error', foreground='red')
        self.chat_display.tag_config('file', foreground='darkblue', font=('Arial', 9))
        
        # Input area
        input_frame = ttk.Frame(right_panel)
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Recipient selection
        recipient_frame = ttk.Frame(input_frame)
        recipient_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(recipient_frame, text="To:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.recipient_var = tk.StringVar()
        self.recipient_combo = ttk.Combobox(
            recipient_frame,
            textvariable=self.recipient_var,
            font=('Arial', 10),
            width=30
        )
        self.recipient_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # File button
        file_btn = ttk.Button(recipient_frame, text="📁 Send File", command=self.send_file_dialog)
        file_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Message input
        message_frame = ttk.Frame(input_frame)
        message_frame.pack(fill=tk.X)
        
        self.message_entry = ttk.Entry(message_frame, font=('Arial', 10))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        send_btn = ttk.Button(message_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text=f"Connected as {self.username}", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial display
        self.display_message("System", f"Connected to ClassChat as {self.username}", 'system')
        self.display_message("System", "Use the dropdown to select a user or group, or type directly", 'system')
        self.display_message("System", "For groups, use @groupname", 'system')
        
        # Request initial lists
        self.root.after(500, self.list_groups)
    
    def receive_messages(self):
        """Receive messages from server (runs in separate thread)"""
        while self.connected:
            try:
                data = self.client_socket.recv(1024 * 1024).decode('utf-8')
                if not data:
                    break
                
                # Parse JSON message
                try:
                    message = json.loads(data)
                    self.handle_message(message)
                except json.JSONDecodeError:
                    # Plain text message (legacy)
                    self.display_message("Server", data, 'system')
            
            except Exception as e:
                if self.connected:
                    self.display_message("Error", f"Connection lost: {e}", 'error')
                    self.connected = False
                break
        
        if self.connected:
            self.disconnect()
    
    def handle_message(self, message):
        """Handle different message types"""
        status = message.get('status', '')
        
        if status == 'message':
            # Direct message
            sender = message.get('sender', 'Unknown')
            text = message.get('text', '')
            timestamp = message.get('timestamp', '')
            
            if timestamp:
                self.display_message(f"{sender} [{timestamp}]", text, 'incoming')
            else:
                self.display_message(sender, text, 'incoming')
        
        elif status == 'group_message':
            # Group message
            sender = message.get('sender', 'Unknown')
            group = message.get('group', 'Unknown')
            text = message.get('text', '')
            self.display_message(f"@{group} - {sender}", text, 'group')
        
        elif status == 'success':
            # Success notification
            text = message.get('message', 'Success')
            self.display_message("✓ Success", text, 'system')
        
        elif status == 'error':
            # Error message
            text = message.get('message', 'Error')
            self.display_message("✗ Error", text, 'error')
        
        elif status == 'queued':
            # Message queued for offline user
            text = message.get('message', 'Message queued')
            self.display_message("📮 Queued", text, 'system')
        
        elif status == 'offline_messages':
            # Offline messages notification
            count = message.get('count', 0)
            self.display_message("📬 Offline Messages", f"You have {count} offline message(s)", 'system')
        
        elif status == 'group_list':
            # Groups list
            groups = message.get('groups', [])
            self.update_groups_list(groups)
        
        elif status == 'user_list':
            # Online users list
            users = message.get('users', [])
            self.update_users_list(users)
        
        elif status == 'file_transfer':
            # File received
            sender = message.get('sender', 'Unknown')
            filename = message.get('filename', 'unknown')
            filesize = message.get('filesize', 0)
            checksum = message.get('checksum', '')
            file_data = message.get('data', '')
            timestamp = message.get('timestamp', '')
            
            self.receive_file(sender, filename, filesize, checksum, file_data, timestamp)
        
        else:
            # Unknown message type - display as is
            self.display_message("Server", str(message), 'system')
    
    def display_message(self, sender, text, tag='incoming'):
        """Display a message in the chat area"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if tag == 'system':
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'offline')
            self.chat_display.insert(tk.END, f"{sender}: ", tag)
            self.chat_display.insert(tk.END, f"{text}\n")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'offline')
            self.chat_display.insert(tk.END, f"{sender}:\n", tag)
            self.chat_display.insert(tk.END, f"  {text}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Send a message"""
        recipient = self.recipient_var.get().strip()
        text = self.message_entry.get().strip()
        
        if not recipient:
            messagebox.showwarning("No Recipient", "Please select or enter a recipient")
            return
        
        if not text:
            messagebox.showwarning("No Message", "Please enter a message")
            return
        
        try:
            # Check if group message
            if recipient.startswith('@'):
                # Group message
                group_name = recipient[1:]
                message = {
                    "status": "group_message",
                    "sender": self.username,
                    "group": group_name,
                    "text": text
                }
                self.display_message(f"You → @{group_name}", text, 'outgoing')
            else:
                # Direct message
                message = {
                    "status": "message",
                    "sender": self.username,
                    "receiver": recipient,
                    "text": text
                }
                self.display_message(f"You → {recipient}", text, 'outgoing')
            
            # Send to server
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            
            # Clear input
            self.message_entry.delete(0, tk.END)
        
        except Exception as e:
            self.display_message("Error", f"Failed to send message: {e}", 'error')
    
    def send_file_dialog(self):
        """Open file dialog and send file"""
        recipient = self.recipient_var.get().strip()
        
        if not recipient:
            messagebox.showwarning("No Recipient", "Please select or enter a recipient first")
            return
        
        # Remove @ from group names
        if recipient.startswith('@'):
            messagebox.showinfo("File Transfer", "File transfer only works for direct messages, not groups")
            return
        
        # Open file dialog
        filepath = filedialog.askopenfilename(title="Select File to Send")
        
        if not filepath:
            return
        
        # Check file size (10MB limit)
        filesize = os.path.getsize(filepath)
        if filesize > 10 * 1024 * 1024:
            messagebox.showerror("File Too Large", "File must be less than 10MB")
            return
        
        try:
            # Read file
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            # Calculate checksum
            checksum = hashlib.sha256(file_data).hexdigest()
            
            # Encode to base64
            encoded_data = base64.b64encode(file_data).decode('utf-8')
            
            # Create message
            filename = os.path.basename(filepath)
            message = {
                "status": "file_transfer",
                "sender": self.username,
                "receiver": recipient,
                "filename": filename,
                "filesize": filesize,
                "checksum": checksum,
                "data": encoded_data
            }
            
            # Send
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            
            self.display_message("📁 File Sent", f"Sent {filename} ({filesize} bytes) to {recipient}", 'file')
        
        except Exception as e:
            messagebox.showerror("File Transfer Error", f"Failed to send file: {e}")
    
    def receive_file(self, sender, filename, filesize, checksum, file_data, timestamp):
        """Receive and save a file"""
        try:
            # Decode base64
            decoded_data = base64.b64decode(file_data)
            
            # Verify checksum
            calculated_checksum = hashlib.sha256(decoded_data).hexdigest()
            
            if calculated_checksum != checksum:
                self.display_message("✗ File Error", f"Checksum mismatch for {filename}", 'error')
                return
            
            # Create downloads directory
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            
            # Handle duplicate filenames
            save_path = os.path.join(downloads_dir, filename)
            counter = 1
            while os.path.exists(save_path):
                name, ext = os.path.splitext(filename)
                save_path = os.path.join(downloads_dir, f"{name}_{counter}{ext}")
                counter += 1
            
            # Save file
            with open(save_path, 'wb') as f:
                f.write(decoded_data)
            
            # Display message
            timestamp_str = f" [{timestamp}]" if timestamp else ""
            self.display_message("📁 File Received", 
                               f"From {sender}{timestamp_str}: {filename} ({filesize} bytes)\nSaved to: {save_path}\n✓ Checksum verified",
                               'file')
        
        except Exception as e:
            self.display_message("✗ File Error", f"Failed to receive file: {e}", 'error')
    
    def create_group_dialog(self):
        """Dialog to create a group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Group")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Group Name:", font=('Arial', 10)).pack(pady=(20, 5))
        
        group_entry = ttk.Entry(dialog, font=('Arial', 10), width=25)
        group_entry.pack(pady=5)
        group_entry.focus()
        
        def create():
            group_name = group_entry.get().strip()
            if not group_name:
                messagebox.showwarning("Invalid Name", "Please enter a group name")
                return
            
            if ' ' in group_name or '@' in group_name:
                messagebox.showwarning("Invalid Name", "Group name cannot contain spaces or @")
                return
            
            # Send create command
            message = {
                "status": "command",
                "command": "create",
                "group": group_name,
                "sender": self.username
            }
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            
            dialog.destroy()
            self.list_groups()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Create", command=create).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        group_entry.bind('<Return>', lambda e: create())
    
    def join_group_dialog(self):
        """Dialog to join a group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Join Group")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Group Name:", font=('Arial', 10)).pack(pady=(20, 5))
        
        group_entry = ttk.Entry(dialog, font=('Arial', 10), width=25)
        group_entry.pack(pady=5)
        group_entry.focus()
        
        def join():
            group_name = group_entry.get().strip()
            if not group_name:
                messagebox.showwarning("Invalid Name", "Please enter a group name")
                return
            
            # Send join command
            message = {
                "status": "command",
                "command": "join",
                "group": group_name,
                "sender": self.username
            }
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            
            dialog.destroy()
            self.list_groups()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Join", command=join).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        group_entry.bind('<Return>', lambda e: join())
    
    def leave_group_dialog(self):
        """Dialog to leave a group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Leave Group")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Group Name:", font=('Arial', 10)).pack(pady=(20, 5))
        
        group_entry = ttk.Entry(dialog, font=('Arial', 10), width=25)
        group_entry.pack(pady=5)
        group_entry.focus()
        
        def leave():
            group_name = group_entry.get().strip()
            if not group_name:
                messagebox.showwarning("Invalid Name", "Please enter a group name")
                return
            
            # Send leave command
            message = {
                "status": "command",
                "command": "leave",
                "group": group_name,
                "sender": self.username
            }
            self.client_socket.send(json.dumps(message).encode('utf-8'))
            
            dialog.destroy()
            self.list_groups()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Leave", command=leave).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        group_entry.bind('<Return>', lambda e: leave())
    
    def list_groups(self):
        """Request groups list from server"""
        try:
            message = {
                "status": "command",
                "command": "groups",
                "sender": self.username
            }
            self.client_socket.send(json.dumps(message).encode('utf-8'))
        except Exception as e:
            self.display_message("Error", f"Failed to get groups: {e}", 'error')
    
    def update_groups_list(self, groups):
        """Update the groups listbox"""
        self.groups_listbox.delete(0, tk.END)
        self.groups = set(groups)
        
        for group in sorted(groups):
            self.groups_listbox.insert(tk.END, group)
        
        # Update recipient combobox
        self.update_recipient_combo()
    
    def update_users_list(self, users):
        """Update the users listbox"""
        self.users_listbox.delete(0, tk.END)
        self.online_users = set(users)
        
        for user in sorted(users):
            if user != self.username:
                self.users_listbox.insert(tk.END, user)
        
        # Update status bar
        user_count = len(users)
        self.status_bar.config(text=f"Connected as {self.username} | {user_count} user(s) online")
        
        # Update recipient combobox
        self.update_recipient_combo()
    
    def update_recipient_combo(self):
        """Update recipient dropdown with users and groups"""
        values = []
        
        # Add users
        for user in sorted(self.online_users):
            if user != self.username:
                values.append(user)
        
        # Add groups with @ prefix
        for group in sorted(self.groups):
            values.append(f"@{group}")
        
        self.recipient_combo['values'] = values
    
    def select_user_from_list(self, event):
        """Handle double-click on user list"""
        selection = self.users_listbox.curselection()
        if selection:
            user = self.users_listbox.get(selection[0])
            self.recipient_var.set(user)
            self.message_entry.focus()
    
    def select_group_from_list(self, event):
        """Handle double-click on group list"""
        selection = self.groups_listbox.curselection()
        if selection:
            group = self.groups_listbox.get(selection[0])
            self.recipient_var.set(f"@{group}")
            self.message_entry.focus()
    
    def refresh_all(self):
        """Refresh users and groups"""
        self.list_groups()
        # Note: User list is updated automatically by server
    
    def show_about(self):
        """Show about dialog"""
        about_text = """ClassChat GUI Client
Version 1.0

Educational TCP/IP Chat System
with support for:
• Direct messaging
• Group chatting
• File transfer
• Offline messages

Built with Python + Tkinter
Compatible with all ClassChat servers

GitHub: bereket2sh/ClassChat"""
        
        messagebox.showinfo("About ClassChat", about_text)
    
    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            self.connected = False
            
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
            
            self.display_message("System", "Disconnected from server", 'system')
            self.status_bar.config(text="Disconnected")
            
            # Optionally return to login screen
            response = messagebox.askyesno("Disconnected", "Return to login screen?")
            if response:
                self.setup_login_screen()
    
    def on_closing(self):
        """Handle window close"""
        if self.connected:
            if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
                self.disconnect()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ClassChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
