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
    res.name = dict["name"]
    return [res, dict["cameraX"], dict["cameraY"]]

lastRecv = 0
def listenToServer():
    global lastRecv
    while True:
        print("Entered")
        try:
            res = s.recvfrom(200000)[0].decode()
            print("Got")
            print(json.loads(res)["newPlayer"])
            try:
                #print(json.loads(res)["newPlayer"])
                res2 = buildPlayer(json.loads(res)["newPlayer"][1])
                cameraX = res2[1]
                cameraY = res2[2]
                players.append(res2[0])
                print("Gave player")
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            lastRecv = res
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
    s.send(dec_playerPosition.encode())
    print("Sent")
    print("GONANN RECV")
    time.sleep(0.05)
    try:
        res = s.recvfrom(50000)
        res = res[0].decode()
    except Exception as e:
        res = lastRecv
        print(e)
    res = json.loads(res)
    print("Recvd")
    for player in players:
        if player.name == userName and res != 0:
            player = buildPlayer(res)[0]
            cameraX = buildPlayer(res)[1]
            cameraY = buildPlayer(res)[2]
            print("BUILT")
    for player in players:
        player.draw(scr, cameraX, cameraY)
    pygame.display.update()
    

    