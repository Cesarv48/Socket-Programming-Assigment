# UDP client server implementation

import socket

HOST = '127.0.0.1'  # localhost
PORT = 65432
TIMEOUT = 10  # seconds to wait before assuming the transfer is done

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(TIMEOUT)

client_addr = None

try:
    # bind socket to port and listen for connection
    s.bind((HOST, PORT))
    print(f"Server listening on port {PORT}...")

    # First packet is the expected file size
    packet, client_addr = s.recvfrom(1024)
    expected_size = int(packet.decode())
    print(f"Expecting {expected_size} bytes...")

    # Receive the full file in one datagram
    data, client_addr = s.recvfrom(65536)

    # packet loss handling - if size mismatch packet loss occured
    if len(data) != expected_size:
        raise ConnectionError(f"Packet loss: received {len(data)}/{expected_size} bytes")

    with open('output.jpeg', 'wb') as f:
        f.write(data)

    # file transfer confirmation
    print(f"File saved as output.jpeg ({len(data)} bytes)")
    s.sendto(b"Success: File received and saved.", client_addr)

# basic error handling
except FileNotFoundError: #file not found error
    print("Error: Could not save the file.")
except ConnectionError as e: # connection error
    print(f"Connection error: {e}")
finally:
    s.close() # close server
