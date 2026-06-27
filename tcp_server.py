# TCP client server implementation

import socket

HOST = '127.0.0.1' #localhost
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoid "address in use" errors

try:
    s.bind((HOST, PORT)) # bind host and port and listen for connection
    s.listen(1)
    print(f"Server listening on port {PORT}...")

    # accept connection
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    # Receive the file size first (16 byte header)
    header = conn.recv(16)
    file_size = int(header.decode().strip())
    print(f"Expecting {file_size} bytes...")

    # Keep reading until we have the full file
    data = b''
    while len(data) < file_size: 
        chunks = conn.recv(4096)
        if not chunks:
            break
        data += chunks

    # Save the file
    with open('output.jpeg', 'wb') as f:
        f.write(data)

    print(f"File saved as output.jpeg ({len(data)} bytes)")
    conn.send(b"Success: File received and saved.") # file confirmation

# basic error handling
except FileNotFoundError: #file not found error
    print("Error: Could not save the file.")
except ConnectionError as e: # connection error
    print(f"Connection error: {e}")
finally:
    s.close() # close server
