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

import sys, os


pygame.font.init()
pygame.init()

my_font = pygame.font.SysFont('Comic Sans MS', 20)

GAME_WIDTH = 500
GAME_HEIGHT = 50
CameraX = 0 # Offset za kameru
CameraY = 0


# Blocks - Svi blokovi imaju jednu vrednost kojom su zabelezeni u matrici
AIR = 0
DIRT = 1
GRASS = 2
STONE = 3
WOOD_PLATFORM = 4


buttons = [Button.Button(pygame.Rect(0,150,150,75), "Reset builds", 32)] # Ovo je samo dugmo za resetovanje buildova u debug menuju



def blur_generate_world(blurAmount): # Trenutno (2.8.2023) koristim ovo da generisem svet. Uzimam prosecnu vrednost random brojeva da dobijem vise smooth teren.
    # BlurAmount je od kolko brojeva da uzmem prosek. Sto je veci, to je ravnije
    world = generate_world()
    listToBlur = []
    for i in range(GAME_WIDTH+blurAmount):
        listToBlur.append(random.randint(0,10))
    
    for i in range(GAME_WIDTH):
        height = int((listToBlur[i]+listToBlur[i+1]+listToBlur[i+2])/blurAmount)
        for j in range(height):
            world[29-j][i] = DIRT
    return world


def smart_generate_world(): # Stari metod generisanja sveta
    world = generate_world() # Generate flat world, that hills will be added to
    num_of_hills = random.randint(int(GAME_WIDTH/10), int(GAME_WIDTH/5)) # Number of hills to be generated
    for i in range(num_of_hills):
        while True:
            x = random.randint(5,GAME_WIDTH-16) # Start x position of hill
            if world[29][x] == AIR:
                break
        height = random.randint(5,12) # Height of generated hill
        for j in range(height):
            for z in range(x, x+random.randint(5,15)): # Width
                prob = random.randint(0,100)
                if prob<97:
                    if world[29-j+1][z] != AIR:
                       world[29-j][z] = GRASS
                       world[29-j+1][z] = DIRT       
    return world

def generate_world(): # Generate flat world split into layers ( Pravi svet od par slojeva, na koje druge dve generate world funkcije mogu da nagradjuju)
    world = []
    for i in range(GAME_HEIGHT):
        world.append([])
        for j in range(GAME_WIDTH):
            block = None
            if i > 0 and i < 30:
                block = AIR
            elif i >=30 and i < 40:
                block = DIRT
            elif i >= 40 and i < 45:
                block = DIRT
            else:
                block = STONE
            world[i].append(block) 
    return world


def draw_world(window,world, player): # Draw the world - crta svet po ili boji koji taj blok ima, ili po teksturi. ( Globals.colors_dict i Globals.img_dict)
    counter = 0
    for i in range(GAME_HEIGHT):
        for j in range(GAME_WIDTH): 
            if j-CameraX >-1 and player.x - (j) < 21 and j-player.x < 21:
                if counter != 0:
                    counter -= 1
                    continue
                color = Globals.colors_dict[world[i][j]]
                if color == None:
                    color = pygame.Color("Yellow")
                    img = Globals.img_dict[WOOD_PLATFORM]
                    window.blit(Globals.img_dict[WOOD_PLATFORM], pygame.Rect((j-CameraX)*Globals.BLOCK_SIZE,(i-CameraY)*Globals.BLOCK_SIZE,Globals.BLOCK_SIZE,20))
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

#window = pygame.display.set_mode((1280,720)) # Incijalizacija prozora
clock = pygame.time.Clock()
world = blur_generate_world(6)


def applyGrassLayer(world, player): # Zamenjuje sve top blokove dirta sa travom
    for i in range(GAME_WIDTH):
        for j in range(1,GAME_HEIGHT):
            if i-CameraX >-1 and abs(player.x - (i)) < 60:
                if world[GAME_HEIGHT-j][i] == AIR:
                    if world[GAME_HEIGHT-j+1][i] != WOOD_PLATFORM:
                        world[GAME_HEIGHT-j+1][i] = GRASS
                    break
                    
listOfPlatforms = []          

def debugMode(window,player,listOfPlatforms, clock : pygame.time.Clock, mouseState, mousePos):
    text_surface = my_font.render(f"Player pos: {(player.x, player.y)}", True, (0, 0, 0))
    window.blit(text_surface, (0,0))
    text_surface = my_font.render(f"Number of blocks placed by player: {len(listOfPlatforms)}", True, (0, 0, 0))
    window.blit(text_surface, (0,50))
    text_surface = my_font.render(f"Fps: {int(clock.get_fps())}", True, (0, 0, 0))
    window.blit(text_surface, (0,100))
    if buttons[0].update(mouseState,mousePos) == True:
        for p in listOfPlatforms:
            world[p[1]][p[0]] = AIR
        listOfPlatforms = []
    buttons[0].draw(window)
    return listOfPlatforms
    
    
    


def saveGame(saveName, world, player, listOfPlatforms, Camera_x, Camera_y):
    json_dict = {"world" : world, "player" : None, "listOfPlatforms" : listOfPlatforms, "CameraX": Camera_x, "CameraY" : Camera_y}
    json_dict["player"] = {"x" : player.x, "y" : player.y}
    
    json_obj = json.dumps(json_dict)
    f = open(f"{saveName}.sav", "w")
    f.write(json_obj)
    f.close()
    
    
def loadGame(saveName):
    f = open(f"{saveName}.sav", "r")
    contents = f.read()
    f.close()
    decoded_dict = json.loads(contents)
    print("DONE")
    return [decoded_dict["world"], Player.Player(decoded_dict["player"]["x"], decoded_dict["player"]["y"]), decoded_dict["listOfPlatforms"], decoded_dict["CameraX"], decoded_dict["CameraY"]]

def drawHUD(window,drawInventory, player : Player):
    if drawInventory:
        window.blit(INVENTORY_IMG,(0,0))
        for i in range(len(player.inventory)):
            window.blit(player.inventory[i][0].img, (47.5*i+25, 30))
            my_font2 = pygame.font.SysFont('Comic Sans MS', 15)
            text_surface = my_font2.render(f"{player.inventory[i][1]}", True, (0, 0, 0))
            window.blit(text_surface, (47.5*i+40, 49))


#player = Player.Player(20,5)
#player.accuracy = 1
debug = False
holdingDebug = False
startButton = Button.Button(pygame.Rect(542,239,240,50),"INVIS", 2)

loadButton = Button.Button(pygame.Rect(543,299,240,50),"INVIS", 2)

MAIN_MENU_IMG = pygame.image.load("Textures\\MainScreen.jpg")
exitButton = Button.Button(pygame.Rect(612,525,60,30), "INVIS", 2)

INVENTORY_IMG = pygame.image.load("Textures\\Inventory.png")
INVENTORY_IMG.set_alpha(200)
holdingI = False
inventoryOpen = False
#player.addToInventory([WoodPlatform, 100])
#MAIN_MENU_IMG = pygame.transform.smoothscale(MAIN_MENU_IMG, (800,800))

world = generate_world()
world = blur_generate_world(15)
recvs = []
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
            a = int(lengthbuf.decode()[:i])
            buf = lengthbuf.decode()[i+1:]
            lengthbuf = a
            buf = buf.encode()
            break
    length =lengthbuf
    return recvall(sock, length-len(buf.decode()), buf)



def send_one_message(sock, data):
    length = len(data)
    sock.sendall(str(length).encode())
    sock.sendall((str(length)+str(data)).encode())







recvs = []
lastRecv = []


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def listenForNewPlayers():
    port = 12095
    s.bind(('', port))
    print("Binded")
    while True:
        try:
            print("Listening")
            s.listen(10)
            client, addr = s.accept()
            a = recv_one_message(client).decode()
            print("Connection established")
            usr = recv_one_message(client).decode()
            print("Info recievedf")
            player1 = Player.Player(0,2)
            players.append([client, addr, player1, usr])
            buildDict = {"x" : player1.x,"y" : player1.y, "dx" : player1.dx, "dy" : player1.dy, "CameraX" : 0, "CameraY": 0, "name" : usr}
            send_one_message(client,"world")
            print("SENTTTTTTTTTTTTTT")
            for i in range(10):
                temp = []
                for j in range(5):
                    temp.append(world[i*5+j])
                send_one_message(client, json.dumps(temp))
                print("Sent part of world")
            for person in players:
                send_one_message(person[0],json.dumps({"newPlayer" : [addr, buildDict, usr], "world" : world}) )
                print("Sent")
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass
players = []
t1 = threading.Thread(target=listenForNewPlayers)
t1.start()

def listenForCommands():

    while True:
        try:
            for play in players:
                a = recv_one_message(play[0]).decode()
                lastRecv = a
                recvs.append(a)
        except Exception as e:
            print(e)
            pass

t2 = threading.Thread(target=listenForCommands)

while True:
    for play in players:
        time.sleep(1000)
        a = lastRecv
        res = json.loads(a)
        CameraX, CameraY = play[2].update(res["keys"], world, CameraX, CameraY)
        #play[2].build(res["mouse"], res["mouseCoords"], world, CameraX, CameraY)
        json_object = json.dumps({"x" : play[2].x,"y" : play[2].y, "dx" : play[2].dx, "dy" : play[2].dy, "CameraX" : CameraX, "CameraY": CameraY, "name" : play[2].name})
        print("Bouta send")
        print(len(json_object))
        time.sleep(0.05)
        play[0].send(json_object+"END".encode())
        print("Send")
    for play in players:
        continue
        dictic = []
        for i in range(len(players)):
            dictic[players[i][3]] = players[i]
        play[0].send(json.dumps(dictic).encosde())
        