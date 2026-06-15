#--CLIENT--#
# this file contains the code for the client side of the robot, main function is to relay the distancing data to the server on the local computer
# for drawing.
# the packet contains 2 integers, a distance value and a directional value
# host will be a computer within the local network
# use of non dedicated ports recommended

import socket
import struct
import threading
from time import sleep


# the bot client is meant to make sure that processes in sending data to the server do not interrupt the actul robot performance by blocking the main thread of the program.
# during initialization set variable and also locks the client thread to prevent main thread blocking
# immediately start the thread to open the socket

class BotClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.locker = threading.Lock()
        cThread = threading.Thread(target=self.connect)
        cThread.daemon = True
        cThread.start()
        
    # connect opens the socket for use
    # if cannot connect retry after 3 second sleep on going, it is assumed server should be up prior to calling the client

    def connect(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                print("Connected")
                break
            except (ConnectionRefusedError, OSError):
                print("Server not available, retrying...")
                sleep(3)

    # packages data to be sent
    # data type should be two integers
    # if the connection is broken try to reconnect on new thread

    def send_pack(self,distance, turn):
        byte_data = struct.pack('ii', distance, turn)
        with self.locker:
            try:
                self.sock.sendall(byte_data)
            except (BrokenPipeError, OSError):
                self.sock = None
                reconThread = threading.Thread(target=self.connect)
                reconThread.daemon = True
                reconThread.start()

    # async calls the send pack function under a new background thread
    def send_async(self,distance, turn):
        thread = threading.Thread(target=self.send_pack, args=(distance, turn))
        thread.daemon = True
        thread.start()
