import socket
import pygame as pyg
import threading
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8080
s.connect((host, port))


background_color = (255,255,255)
screen = pyg.display.set_mode((300,300))
PLAYER_TURN = False  
player = 0
screen.fill(background_color)

pyg.display.flip()
rectsToDraw = [
    pyg.Rect(0,0,90,90),pyg.Rect(100,0,90,90),pyg.Rect(200,0,90,90),
    pyg.Rect(0,100,90,90),pyg.Rect(100,100,90,90),pyg.Rect(200,100,90,90),
    pyg.Rect(0,200,90,90),pyg.Rect(100,200,90,90),pyg.Rect(200,200,90,90)
]
def drawBoard(screen, rectsToDraw, p):
    for i in range(9):
        color = (180,30,150)
        if p[i] == 1:
            color = (255,0,0)
        elif p[i] == 2:
            color = (0,0,255)
        pyg.draw.rect(screen, color, rectsToDraw[i])
    pyg.display.flip()

def boardEncoder(board):
    toReturn = ""
    for i in board:
        toReturn+=str(i)
    return toReturn
def boardDecoder(board):
    toReturn = []
    for i in board:
        toReturn.append(int(i))
    return toReturn
p=[0 for i in range(9)]

# server comms function
def serverStuff():
    global s
    global PLAYER_TURN
    global player
    global p
    # first message is player
    received = s.recv(1024).decode()
    if received=="1":
        player=1
        PLAYER_TURN=True
        print("You are Player 1")
        # sends initially
        while PLAYER_TURN:
            time.sleep(1)
        s.send(boardEncoder(p).encode())
    else:
        player=2
        PLAYER_TURN=False
        print("You are Player 2")

    # at this point p1 and p2 are equal (not their turn)
    # so they should be waiting for response
    while True:
        received = s.recv(1024).decode()
        print(received)
        if not received:
            break
        p = boardDecoder(received)
        PLAYER_TURN = True
        # wait for player to do turn in the mainthread
        while PLAYER_TURN:
            print("im sleeping")
            time.sleep(1)
        # if passed the guard, send updated board
        toSend = boardEncoder(p)
        s.send(toSend.encode())
    


# starting server comms
threading.Thread(target=serverStuff, args=()).start()
# start gameloop once player assigned
running=True
captioned=False

while running:  
    pos = (-1,-1)
    # drawing game
    if not captioned and player!=0:
        pyg.display.set_caption(str(player))
        captioned=True
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
            s.close()
            pyg.quit()
            sys.exit()
        if event.type == pyg.MOUSEBUTTONDOWN:
            pos = pyg.mouse.get_pos()
    # handeling pos
    # if something changed, auto makes it not the player's turn
    if pos != (-1,-1) and PLAYER_TURN:
        tmp = sum(p)
        if pos[0]//100 == 0:
            if pos[1]//100 ==0:
                p[0] = player
            elif pos[1]//100 == 1:
                p[3] = player
            elif pos[1]//100 == 2:
                p[6] = player
        if pos[0]//100 == 1:
            if pos[1]//100 == 0:
                p.append(1)
                p[1] = player
            elif pos[1]//100 == 1:
                p[4] = player
            elif pos[1]//100 == 2:
                p[7] = player
        if pos[0]//100 == 2:
            if pos[1]//100 ==0:
                p[2] = player
            elif pos[1]//100 == 1:
                p[5] = player
            elif pos[1]//100 == 2:
                p[8] = player          
        if sum(p) != tmp:
            PLAYER_TURN=False
    
    drawBoard(screen,rectsToDraw,p)

