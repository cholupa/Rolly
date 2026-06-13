# --CLIENT--
# The purpose of the client file is to gather the distance data from the robot class and send to the server file on a local computer. 

import socket
import struct
import threading
from time import sleep


class BotClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.locker = threading.Lock()
        self.connected = False
        cThread = threading.Thread(target=self.connect)
        cThread.daemon = True
        cThread.start()
        

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


    def send_pack(self,distance, turn):
        byte_data = struct.pack('ii', distance, turn)
        with self.locker:
            try:
                self.sock.sendall(byte_data)
            except (BrokenPipeError, OSError):
                self.connect()
                self.sock.sendall(byte_data)



    def send_async(self,distance, turn):
        thread = threading.Thread(target=self.send_pack, args=(distance, turn))
        thread.daemon = True
        thread.start()
