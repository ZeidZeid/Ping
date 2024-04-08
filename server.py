import socket
import threading
import pickle
import time
# Define the size of the header used in messages
HeaderSize = 10
# Function to handle client connections
def client_thread(clientsocket, address):
    print(f"Connection from {address} has been established.")
    while True:
        full_msg = b''
        new_msg = True
        while True:
            try:
                # Receive a message from the client
                msg = clientsocket.recv(16)
                if new_msg:
                    msglen = int(msg[:HeaderSize].strip())
                    new_msg = False

                full_msg += msg

                if len(full_msg) - HeaderSize == msglen:
                    full_msg = pickle.loads(full_msg[HeaderSize:])
                    print(f"Received from {address}: {full_msg}")
                    new_msg = True
                    break
            except:
                break
 # Check if the received message is a "ping"
        if full_msg == "ping":
            response = "reached and pinged back like a heartbeat"
        else:
            response = f"Echo: {full_msg}"

        response = pickle.dumps(response)
        response = bytes(f"{len(response):<{HeaderSize}}", 'utf-8') + response
        clientsocket.send(response)

    clientsocket.close()
    print(f"Connection with {address} closed.")

# Create a socket object for the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1235))
s.listen(5)
# Continuously accept new connections
while True:
    clientsocket, address = s.accept()
    threading.Thread(target=client_thread, args=(clientsocket, address)).start()
