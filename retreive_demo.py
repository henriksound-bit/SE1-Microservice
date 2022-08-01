import socket
import json

# Create socket
connectedSocket = socket.socket()

# Define the connection port
port = 12345

# Connect to server
connectedSocket.connect(('127.0.0.1', port))


a = {
    "request": "retrieve",
    "username": "Alex"
}
b = json.dumps(a)
b = b.encode('utf-8')
blen = len(b)
blen_str = str(blen).encode('utf-8')
blen_buffer = b' ' * (1024 - len(blen_str)) + blen_str
connectedSocket.send(blen_buffer)
connectedSocket.send(b)


# Receive data and decode
print(connectedSocket.recv(1024).decode())
print(connectedSocket.recv(1024).decode())


# Close the socket
connectedSocket.close()