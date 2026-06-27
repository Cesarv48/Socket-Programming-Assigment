#tcp client server implementation

import socket
import os

HOST = '127.0.0.1'  # localhost
PORT = 65432
FILE_NAME = 'input.jpeg'

# error handling for file input 
try:
    # Check the file exists before doing anything
    if not os.path.isfile(FILE_NAME):
        raise FileNotFoundError(f"'{FILE_NAME}' not found in system.")

    # read file
    with open(FILE_NAME, 'rb') as f:
        file_data = f.read()

    print(f"Read '{FILE_NAME}' ({len(file_data)} bytes)")

    # creating client and connecting to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    # data is exchanged
    # Send the file size first as a 16-byte header so the server
    # knows exactly how many bytes to expect
    header = str(len(file_data)).ljust(16).encode()
    client.sendall(header) #send the total size of header

    # Send the actual file data
    client.sendall(file_data)
    print("File sent. Waiting for delivery...")

    # decode file
    data = client.recv(1024).decode() # receive the data the sender sends back
    print(f"Server says: {data}") # confirm data was received

#basic error handling
except FileNotFoundError as x:
    print(f"Error: {x}") # file not found error handling
except ConnectionRefusedError:
    print("Error: Could not connect to server. Check if TCP server is running") # unable to connect to server error handling
except ConnectionError as x:
    print(f"Connection error: {x}") # connection error handling
finally:
    client.close() # close client socket and end server connection
