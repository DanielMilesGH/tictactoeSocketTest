import socket
import threading
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host="127.0.0.1"
port = 8080

serversocket.bind((host, port))
IDs = 0

boardStates = []


class client(threading.Thread):
    def __init__(self, socket1, socket2, address1, address2):
        threading.Thread.__init__(self)
        self.sock1 = socket1
        self.sock2 = socket2
        self.addr1 = address1
        self.addr2 = address2
        self.start()
        self.ID = IDs
    def run(self):
        global boardStates
        # self.name = self.sock.recv(1024).decode()
        self.sock1.send("1".encode())
        self.sock2.send("2".encode())
        while True:
            # waits for p1 response
            boardStates[self.ID//2] = self.sock1.recv(1024).decode()
            # send that to p2
            self.sock2.send(boardStates[self.ID//2].encode())
            # wait for p2 response
            boardStates[self.ID//2] = self.sock2.recv(1024).decode()
            # send to p1
            self.sock1.send(boardStates[self.ID//2].encode())

serversocket.listen(5)
print("server started and listening")
while True:
    clientsocket1, address1 = serversocket.accept()
    print("waiting for number 2")
    clientsocket2, address2 = serversocket.accept()
    client(clientsocket1, clientsocket2, address1, address2)
    print("Both Clients Started"), 
    boardStates.append("")
    IDs+=1
