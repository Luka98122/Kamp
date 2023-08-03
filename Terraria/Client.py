import pygame
import random
import Player
import Button
import json
import time
import socket
from Item import *
from Globals import *
import threading

players = [] # Liosta svih igraca koji client poznaje ukljucujuci sebe


def buildPlayer(dict):
    res = Player.Player(dict["x"], dict["y"])
    res.dx = dict["dx"]
    res.dy = dict["dy"]
    return [res, dict["cameraX"], dict["cameraY"]]


def listenToServer():
    while True:
        print("Entered")
        try:
            res = s.recvfrom(10000)[0].decode()
            print("Got")
            try:
                #print(json.loads(res)["newPlayer"])
                res2 = buildPlayer(json.loads(res)["newPlayer"][1])
                cameraX = res2[1]
                cameraY = res2[2]
                players.append(res2[0])
            except Exception as e:
                print(e)
                print(json.loads(res)["newPlayer"])
                pass
        except Exception as e:
            print(e)
            pass
cameraX = 0
cameraY = 0
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
s.send(userName.encode())
scr = pygame.display.set_mode((1280,720))
pygame.display.init()
game = True
playerPosition = {"keys":"", "mouse":"", "mouseCoords":""}


#s2 = socket.socket()
#s.bind(('', 13496))
#s.connect(("127.0.0.1", 12096))
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
    s.send(dec_playerPosition.encode())
    for player in players:
        player.draw(scr, cameraX, cameraY)
    pygame.display.update()
    time.sleep(10)
    

    