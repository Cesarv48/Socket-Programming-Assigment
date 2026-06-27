# UDP client server implementation

import socket
import os

HOST = '127.0.0.1'  # localhost
PORT = 65432
FILE_NAME = 'input.jpeg'

# error if file not found in system
try:
    if not os.path.isfile(FILE_NAME):
        raise FileNotFoundError(f"'{FILE_NAME}' not found in system.")

    # open and read file
    with open(FILE_NAME, 'rb') as f:
        file_data = f.read()

    print(f"Read '{FILE_NAME}' ({len(file_data)} bytes)")

    # create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(10) # timeout if time exceeds 10 seconds

    # Send file size first so server knows how many bytes to expect
    client.sendto(str(len(file_data)).encode(), (HOST, PORT))

    # Send the entire file in one datagram
    client.sendto(file_data, (HOST, PORT))

    print("All packets sent. Waiting for confirmation...")

    # receive and decode data
    try:
        data, _ = client.recvfrom(1024)
        print(f"Server says: {data.decode()}")
    except socket.timeout:
        print("No confirmation received, server may not have gotten all packets.") # message for timeout

# basic error handling
except FileNotFoundError as e:
    print(f"Error: {e}") # file not found error
except OSError as e:
    print(f"Network error: {e}") # network connection error
finally:
    client.close() # close client socket and end server connection
