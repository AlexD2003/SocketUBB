import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Client")
        self.root.geometry("400x500")
        self.create_widgets()
        self.sock = None
        self.protocol = socket.SOCK_STREAM

    def create_widgets(self):
        self.server_ip_label = tk.Label(self.root, text="Server IP:")
        self.server_ip_label.pack(pady=5)
        
        self.server_ip_entry = tk.Entry(self.root)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.server_ip_entry.pack(pady=5)

        self.protocol_label = tk.Label(self.root, text="Select Protocol:")
        self.protocol_label.pack(pady=5)

        self.protocol_var = tk.StringVar(value="TCP")

        self.tcp_radio = tk.Radiobutton(self.root, text="TCP", variable=self.protocol_var, value="TCP", command=self.set_protocol)
        self.tcp_radio.pack()

        self.udp_radio = tk.Radiobutton(self.root, text="UDP", variable=self.protocol_var, value="UDP", command=self.set_protocol)
        self.udp_radio.pack()

        self.message_label = tk.Label(self.root, text="Message to send:")
        self.message_label.pack(pady=5)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_button.pack(pady=5)

        self.response_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10)
        self.response_text.pack(pady=5)

        self.connect_button = tk.Button(self.root, text="Connect to Server", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

    def set_protocol(self):
        if self.protocol_var.get() == "TCP":
            self.protocol = socket.SOCK_STREAM
        else:
            self.protocol = socket.SOCK_DGRAM

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        try:
            self.sock = socket.socket(socket.AF_INET, self.protocol)
            if self.protocol == socket.SOCK_STREAM:
                self.sock.connect((server_ip, 65432))
            self.append_response(f"Connected to server ({'TCP' if self.protocol == socket.SOCK_STREAM else 'UDP'})\n")
        except socket.error as e:
            self.append_response(f"Connection failed: {e}\n")

    def send_message(self):
        if self.sock is None:
            self.append_response("Please connect to the server first.\n")
            return
        message = self.message_entry.get()
        if message:
            threading.Thread(target=self._send_message_thread, args=(message,)).start()

    def _send_message_thread(self, message):
        try:
            if self.protocol == socket.SOCK_STREAM:
                self.sock.send(message.encode())
            else:
                self.sock.sendto(message.encode(), ("127.0.0.1", 65432))
            self.append_response(f"Message sent: {message}\n")
            self.receive_message()
        except socket.error as e:
            self.append_response(f"Error sending message: {e}\n")

    def receive_message(self):
        try:
            if self.protocol == socket.SOCK_STREAM:
                response = self.sock.recv(1024).decode()
            else:
                response, _ = self.sock.recvfrom(1024)
                response = response.decode()
            self.append_response(f"Server reply: {response}\n")
        except socket.error as e:
            self.append_response(f"Error receiving message: {e}\n")

    def append_response(self, message):
        self.response_text.insert(tk.END, message)
        self.response_text.yview(tk.END)

root = tk.Tk()
app = ClientApp(root)
root.mainloop()
