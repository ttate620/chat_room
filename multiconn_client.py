import sys
import socket
import threading
from _thread import *


host = 'localhost'
port = 65432

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect((host, port))


def send():
    while True:
        send_message = input()
        if send_message != "end":
            CLIENT.send(send_message.encode("utf8"))
        else:
            CLIENT.send(send_message.encode("utf8"))
            CLIENT.close()
            break


def recieve():
    while True:
        try:
            recv_message = CLIENT.recv(1024).decode("utf8")
            print(recv_message)
        except OSError:
            break


if __name__ == '__main__':

    recvieve_thread = threading.Thread(target=recieve)
    recvieve_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()
