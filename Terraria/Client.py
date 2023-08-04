import pygame
import random
import Player
import Button
import json
import time
import socket
from Item import *
from Globals import Globals

import threading
GAME_HEIGHT = 500
GAME_WIDTH = 50
players = [] # Liosta svih igraca koji client poznaje ukljucujuci sebe

CameraX = 0
CameraY = 0

def buildPlayer(dict):
    res = Player.Player(dict["x"], dict["y"])
    res.dx = dict["dx"]
    res.dy = dict["dy"]
    res.name = dict["name"]
    return [res, dict["CameraX"], dict["CameraY"]]

lastRecv = 0

def draw_world(window,world, player, CameraX, CameraY): # Draw the world - crta svet po ili boji koji taj blok ima, ili po teksturi. ( Globals.colors_dict i Globals.img_dict)
    counter = 0
    for i in range(GAME_HEIGHT):
        for j in range(GAME_WIDTH): 
            if j-Globals.CameraX >-1 and player.x - (j) < 21 and j-player.x < 21:
                if counter != 0:
                    counter -= 1
                    continue
                color = Globals.colors_dict[world[i][j]]
                if color == None:
                    color = pygame.Color("Yellow")
                    img = Globals.img_dict[Globals.WOOD_PLATFORM]
                    window.blit(Globals.img_dict[Globals.WOOD_PLATFORM], pygame.Rect((j-CameraX)*Globals.BLOCK_SIZE,(i-CameraY)*Globals.BLOCK_SIZE,Globals.BLOCK_SIZE,20))
                    continue
                    #print(f"Drew at {(j,i)}, player is at {(player.x,player.y)}")
                    """""
                    counter = 1
                    while True:
                        if world[i][j+counter] == world[i][j]:
                            counter +=1
                        else:
                            break
                    img = pygame.transform.scale(img_dict[world[i][j]], (Globals.BLOCK_SIZE*counter*8,Globals.BLOCK_SIZE*8))
                    window.blit(img, pygame.Rect(j*Globals.BLOCK_SIZE, i*Globals.BLOCK_SIZE, Globals.BLOCK_SIZE*counter*8, Globals.BLOCK_SIZE*8))
                    print(f"Drew at {(j,i)}, player is at {(player.x,player.y)}")
                    continue
                """
                if j-CameraX >-1 and abs(player.x - (j)) < 60:
                    pygame.draw.rect(window, color, pygame.Rect((j-CameraX)*Globals.BLOCK_SIZE,(i-CameraY)*Globals.BLOCK_SIZE,Globals.BLOCK_SIZE,Globals.BLOCK_SIZE))
                    
                    #pygame.draw.rect(window, pygame.Color("Black"), pygame.Rect((j-CameraX)*Globals.BLOCK_SIZE,(i-CameraY)*Globals.BLOCK_SIZE,Globals.BLOCK_SIZE,Globals.BLOCK_SIZE),1)



def recvall(sock, count, buf):
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4, b'')
    for i in range(4):
        if lengthbuf.decode()[:i].isnumeric():
            lengthbuf = int(lengthbuf.decode()[:i])
            buf = lengthbuf.decode()[:4]
            buf = buf.encode()
            break
    length =lengthbuf
    print("RECEIVVVVVVVVVVVVVVVVVVVVVVVVVVV")
    return recvall(sock, length, buf)



def send_one_message(sock, data):
    length = len(data)
    sock.sendall(str(length).encode())
    sock.sendall((str(length)+str(data)).encode())









recvs =[]
world = []
def listenToServer():
    global lastRecv
    while True:
        print("Entered")
        try:
            res = recv_one_message(s)
            lastRecv = res
            recvs.append(res)
            if res == "world":
                world = []
                for i in range(10):
                    res = recv_one_message(s).decode()
                    recvs.append(res)
                    lastRecv = res
                    for j in range(5):
                        world.append(json.loads(res)[j])
            print("Got")
            print(json.loads(res)["newPlayer"])
            try:
                #print(json.loads(res)["newPlayer"])
                res2 = buildPlayer(json.loads(res)["newPlayer"][1])
                CameraX = res2[1]
                CameraY = res2[2]
                players.append(res2[0])
                print("Gave player")
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            lastRecv = res
            pass
CameraX = 0
CameraY = 0
pygame.font.init()
pygame.init()
s = socket.socket()
a = int(input("Your port"))
s.bind(('', a))
port = 12095
userName = input("Username: ")

t1 = threading.Thread(target=listenToServer)
t1.start()

s.connect(("127.0.0.1", port))
send_one_message(s, userName)
scr = pygame.display.set_mode((1280,720))
pygame.display.init()
game = True
playerPosition = {"keys":"", "mouse":"", "mouseCoords":""}


s.settimeout(10)
while game:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouseCords = pygame.mouse.get_pos()
    playerPosition["keys"] = pygame.key.get_pressed()
    playerPosition["mouse"] = pygame.mouse.get_pressed()
    playerPosition["mouseCoords"] = pygame.mouse.get_pos()
    dec_playerPosition = json.dumps(playerPosition)
    print("About to send")
    send_one_message(s,(dec_playerPosition+"END"))
    print("Sent")
    print("GONANN RECV")
    time.sleep(15.05)
    res = json.loads(lastRecv)
    print("Recvd")
    for player in players:
        if player.name == userName and res != 0:
            player = buildPlayer(res)[0]
            CameraX = buildPlayer(res)[1]
            CameraY = buildPlayer(res)[2]
            draw_world(scr,world, player, CameraX, CameraY)
            print("BUILT")
    for player in players:
        player.draw(scr, CameraX, CameraY)
    
    pygame.display.update()
     

    