#---SERVER---#
# The server file to run on a local computer.
# The server receives the movement data from the client and uses it to command the turtle object to draw the path on screen.

import socket
import turtle
import threading
import struct

HOST = '0.0.0.0'
PORT = 5000
BYTES = 1024
packet = 0


def startServing():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen()
            print(f"Listening on port {PORT}..")
            connection, address = sock.accept()
            while True:
                connection, address = sock.accept()
                with connection:
                    print(f"Connected: {address}")
                    data = connection.recv(BYTES)
                    if not data:
                        print("No Packet")
                        break
                    packet = struct.unpack( 'f', data)[0]
                    connection.sendall(b'Packet Received')
                    print(packet)
    finally:
        print("Exiting..")

server_thread = threading.Thread(target=startServing)
server_thread.daemon = True
server_thread.start()


ttWindow = turtle.Screen()
tt = turtle.Turtle()

turtle.mainloop()

