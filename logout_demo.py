import socket
import json


# Create socket
connectedSocket = socket.socket()

# Define the connection port
port = 12345

# Connect to the server
connectedSocket.connect(('127.0.0.1', port))

x = {
    "request": "logout",
    "username": "Alex",
}
y = json.dumps(x)
y = y.encode('utf-8')
ylen = len(y)
ylen_str = str(ylen).encode('utf-8')
ylen_buffer = b' ' * (1024 - len(ylen_str)) + ylen_str
connectedSocket.send(ylen_buffer)
connectedSocket.send(y)


# Receive data and decode
print(connectedSocket.recv(1024).decode())
print(connectedSocket.recv(1024).decode())
print(connectedSocket.recv(1024).decode())

# Close the socket
connectedSocket.close()