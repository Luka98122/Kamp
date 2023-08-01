import pygame
import random
import Player
pygame.font.init()
pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.init()
GAME_WIDTH = 500
GAME_HEIGHT = 50
CameraX = 0
CameraY = 0
BLOCK_SIZE = 32
# Blocks
AIR = 0
DIRT = 1
GRASS = 2
STONE = 3
WOOD_PLATFORM = 4

colors_dict = {
    AIR : pygame.Color("Cyan"),
    DIRT : pygame.Color("Brown"),
    GRASS : pygame.Color("chartreuse2"),
    STONE : pygame.Color("Grey"),
    WOOD_PLATFORM : None 
}

img_dict = {
    WOOD_PLATFORM : pygame.transform.scale(pygame.image.load("Textures\\Wood_Platform.png"), (BLOCK_SIZE,BLOCK_SIZE))
}


def blur_generate_world(blurAmount):
    world = generate_world()
    listToBlur = []
    for i in range(GAME_WIDTH+blurAmount):
        listToBlur.append(random.randint(0,10))
    
    for i in range(GAME_WIDTH):
        height = int((listToBlur[i]+listToBlur[i+1]+listToBlur[i+2])/blurAmount)
        for j in range(height):
            world[29-j][i] = DIRT
    return world


def smart_generate_world():
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

def generate_world(): # Generate flat world split into layers
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


def draw_world(window,world): # Draw the world
    counter = 0
    for i in range(GAME_HEIGHT):
        for j in range(GAME_WIDTH):
            if j-CameraX >-1 and abs(player.x - (j)) < 60:
                if counter != 0:
                    counter -= 1
                    continue
                color = colors_dict[world[i][j]]
                if color == None:
                    color = pygame.Color("Yellow")
                    #print(f"Drew at {(j,i)}, player is at {(player.x,player.y)}")
                    """""
                    counter = 1
                    while True:
                        if world[i][j+counter] == world[i][j]:
                            counter +=1
                        else:
                            break
                    img = pygame.transform.scale(img_dict[world[i][j]], (BLOCK_SIZE*counter*8,BLOCK_SIZE*8))
                    window.blit(img, pygame.Rect(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE*counter*8, BLOCK_SIZE*8))
                    print(f"Drew at {(j,i)}, player is at {(player.x,player.y)}")
                    continue
                """
                if j-CameraX >-1 and abs(player.x - (j)) < 60:
                    pygame.draw.rect(window, color, pygame.Rect((j-CameraX)*BLOCK_SIZE,(i-CameraY)*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
                    
                    #pygame.draw.rect(window, pygame.Color("Black"), pygame.Rect((j-CameraX)*BLOCK_SIZE,(i-CameraY)*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),1)

window = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
world = blur_generate_world(4)


def applyGrassLayer(world):
    for i in range(GAME_WIDTH):
        for j in range(1,GAME_HEIGHT):
            if i-CameraX >-1 and abs(player.x - (i)) < 60:
                if world[GAME_HEIGHT-j][i] == AIR:
                    if world[GAME_HEIGHT-j+1][i] != WOOD_PLATFORM:
                        world[GAME_HEIGHT-j+1][i] = GRASS
                    break
                    
listOfPlatforms = []          

def debugMode(window,player,listOfPlatforms):
    text_surface = my_font.render(f"Player pos: {(player.x, player.y)}", True, (0, 0, 0))
    window.blit(text_surface, (0,0))
    text_surface = my_font.render(f"Number of blocks placed by player: {len(listOfPlatforms)}", True, (0, 0, 0))
    window.blit(text_surface, (0,50))
    
    
    
    



player = Player.Player(5,5)
player.accuracy = 1
debug = False
holdingDebug = False
while True: # Main game loop
    window.fill("Cyan")
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    keys = pygame.key.get_pressed()
    
    
    CameraX,CameraY = player.update(keys,world, CameraX, CameraY)
    
    mousePos = pygame.mouse.get_pos()
    mouseState = pygame.mouse.get_pressed()
    
    l = player.build(mouseState,mousePos, world, CameraX, CameraY, listOfPlatforms)
    world = l[0]
    listOfPlatforms = l[1]
    applyGrassLayer(world)
    draw_world(window,world)
    player.draw(window, CameraX, CameraY)
    ##img = pygame.transform.scale(img_dict[WOOD_PLATFORM], (BLOCK_SIZE*5,BLOCK_SIZE))
    #window.blit(img, pygame.Rect(0*BLOCK_SIZE, 5*BLOCK_SIZE, BLOCK_SIZE*5, BLOCK_SIZE))
    
    #Update Display
    if keys[pygame.K_F3]:
        if holdingDebug == False:
            if debug == False:
                debug = True
            else:
                debug = False
            holdingDebug = True
    else:
        holdingDebug = False
    
    if debug:
        debugMode(window,player,listOfPlatforms)
    pygame.display.update()
    clock.tick(60)