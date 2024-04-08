import socket
import threading
import pickle
import tkinter as tk
import time
from tkinter import scrolledtext

HeaderSize = 10

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Client")
 # Creating and packing the message entry field
        self.msg_entry = tk.Entry(root, width=50)
        self.msg_entry.pack()

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()
# Creating and packing the area where messages will be displayed
        self.output_area = scrolledtext.ScrolledText(root)
        self.output_area.pack()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname(), 1235))

        threading.Thread(target=self.receive_message, daemon=True).start()
        threading.Thread(target=self.send_heartbeat, daemon=True).start()

    def send_message(self):
        # Function to send a message
        message = self.msg_entry.get()
        if message:
            self.msg_entry.delete(0, tk.END)
            message = pickle.dumps(message)
            message = bytes(f"{len(message):<{HeaderSize}}", 'utf-8') + message
            self.socket.send(message)

    def receive_message(self):
        # Function to receive messages
        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(16)
                if new_msg:
                    msglen = int(msg[:HeaderSize].strip())
                    new_msg = False

                full_msg += msg
# Check if the full message has been received
                if len(full_msg) - HeaderSize == msglen:
                    full_msg = pickle.loads(full_msg[HeaderSize:])
                    self.output_area.insert(tk.END, f"{full_msg}\n")
                    new_msg = True
                    break

    def send_heartbeat(self):
        # Function to send heartbeat messages
        while True:
            message = "ping"
            message = pickle.dumps(message)
            message = bytes(f"{len(message):<{HeaderSize}}", 'utf-8') + message
            self.socket.send(message)
            time.sleep(5)

root = tk.Tk()
app = ClientApp(root)
root.mainloop()
