import sys
import threading
from _thread import *
import socket


# print_lock is Lock obj. State either locked or unlocked. Created in unlocked state.
# methods are accquire()(if unlocked , unlocked->locked if locked blocked until release) and release()(only called on locked state, locked->unlocked)
host = 'localhost'
port = 65432
lock = threading.Lock()

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((host, port))
print('socket binded to port ', port)

CONNECTIONS = {}
ADDRESSES = {}


def accept_connection():

    while True:
        clientSocket, addr = SERVER.accept()
        print('connected to : ', addr[0], ': ', addr[1])
        greeter_msg = "Hello from server! \n Enter username here : "
        clientSocket.send(greeter_msg.encode("utf8"))
        serv_thread = threading.Thread(target=service_connection,
                                       args=(clientSocket,))
        serv_thread.start()


def service_connection(client):

    uname = client.recv(1024).decode("utf8")
    CONNECTIONS[client] = uname
    welcome_msg = "Welcome "+uname + " to the chat"
    broadcast(welcome_msg, client)

    while True:
        msg = client.recv(1024).decode("utf8")
        if msg == "end":
            msg = "has left chat"
            broadcast(msg, client)
            del CONNECTIONS[client]
            break
        else:
            broadcast(msg, client)


def broadcast(message, client):
    uname = CONNECTIONS[client]

    for sockets in CONNECTIONS:
        if sockets != client:

            print(message)
            sockets.send((uname + ": " + message).encode("utf8"))


if __name__ == '__main__':
    SERVER.listen(5)
    print('socket is listening...')
    connectionThread = threading.Thread(target=accept_connection)
    connectionThread.start()
    connectionThread.join()
    SERVER.close()
