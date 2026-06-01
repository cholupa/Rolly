#--CLIENT--#
# a client for the robot to send data to the local computer server. The data is used for the turtle drawing program within the server file.
# Use of socket and threading to ensure these files do not interfere with the main robot processes, acting in the background
import socket
import struct
import threading

HOST = '10.0.0.232'
PORT = 5000
BYTES = 1024

def send_pack(data):
    byte_data = struct.pack('f', data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(byte_data)

def send_async(data):
    thread = threading.Thread(target=send_pack, args=(data,))
    thread.daemon = True
    thread.start()
