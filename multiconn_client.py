import sys
import socket
import threading
from _thread import *

class Client(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 65432
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENT.connect((self.host, self.port))
        self._start()


    def _start(self):
        send_thread = threading.Thread(target=self._send)
        send_thread.start()
        recvieve_thread = threading.Thread(target=self._recieve)
        recvieve_thread.start()



    def _send(self):
        while True:
            
            send_message = input("--> ")
            if send_message != "end":
                self.CLIENT.send(send_message.encode("utf-8"))
            else:
                self.CLIENT.send(send_message.encode("utf-8"))
                self.CLIENT.close()
                break


    def _recieve(self):
        while True:
            try:
                recv_message = self.CLIENT.recv(1024).decode("utf-8")
                print(recv_message)
            except OSError:
                break


if __name__ == '__main__':
    client = Client()


