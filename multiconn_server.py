import sys
import threading
from _thread import *
import socket


class multiConnServer(object) :
    def __init__(self):
        self.CONNECTIONS = {}
        self.ADDRESSES = {}
        self.host = 'localhost'
        self.port = 65432
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind((self.host, self.port))





    def handle_connection(self, client, addr):
        print('----- new user has connected -----')
        greeter_msg = "username? "
        client.send(greeter_msg.encode("utf-8"))
        serv_thread = threading.Thread(target=self.service_connection,
                                    args=(client,))
        serv_thread.start()


    def service_connection(self, client):
        uname = client.recv(1024).decode("utf-8")
        self.CONNECTIONS[client] = uname
        welcome_msg = "-*-*- Welcome "+ uname +" -*-*-"
        self.broadcast(welcome_msg, None)

        while True:
            msg = client.recv(1024).decode("utf-8")
            if msg == "end":
                msg = "has left chat"
                self.broadcast(msg, client)
                del self.CONNECTIONS[client]
                break
            else:
                self.broadcast(msg, client)


    def broadcast(self, message, client):
        for sockets in self.CONNECTIONS:
            if sockets != client:
                sockets.send((message).encode("utf8"))
                
                


if __name__ == '__main__':

    server = multiConnServer()
    server.SERVER.listen(5)
    print('socket listening on port ', server.port)
    while True:

        client, addr = server.SERVER.accept()  
        connectionThread = threading.Thread(target=server.handle_connection, args=(client, addr,))
        connectionThread.start()
        connectionThread.join()

    SERVER.close()
