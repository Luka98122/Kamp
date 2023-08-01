import pygame
import math
BLOCK_SIZE = 32
class Player:
    img = pygame.image.load("Textures\\Player.png")
    img = pygame.transform.scale(img, (BLOCK_SIZE,BLOCK_SIZE))
    accuracy = 1
    ddy = 0.1
    dx = 0
    dy = 5
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def update(self,keys,world, cameraX, cameraY):
        self.dx = 0
        self.dy += self.ddy
        if self.dy > -0.3 and self.dy < 1:
            self.dy = 1
        if self.dy > 2:
            self.dy = 2
        if keys[pygame.K_a]:
            self.dx = -1*self.accuracy
        if keys[pygame.K_d]:
            self.dx = 1*self.accuracy
        if keys[pygame.K_SPACE] and world[int(self.y+1)][int(self.x)] != 0:
            self.dy = -1.8*self.accuracy
        else:
            if self.y > 29 and self.y < 30:
                self.y = 30
        for i in range(self.accuracy):
            try:
                if self.x+self.dx/self.accuracy>=0:
                    if world[int(self.y)][math.ceil(self.x+self.dx/self.accuracy)] == 0 and self.dx != 0:
                        self.x += self.dx/self.accuracy
                        cameraX += self.dx/self.accuracy
                        print(f"Moved x {self.x}")
            except:
                pass
            for i in range(abs(int(self.dy))):
                if world[math.ceil(self.y+self.dy/abs(self.dy))][int(self.x)] == 0 and self.dy != 0:
                    self.y +=  self.dy/abs(self.dy)
                    cameraY += self.dy/abs(self.dy)
                    print(f"Moved y {self.y}")
            """""
            try:
                if self.y + self.dy/self.accuracy > 0:
                    if world[math.ceil(self.y+self.dy/self.accuracy)][int(self.x)] == 0 and self.dy != 0:
                        self.y += self.dy / self.accuracy
                        cameraY += self.dy / self.accuracy
                        print(f"Moved y {self.y}")
            except:
                pass
            """
            return [cameraX,cameraY]
    
    def build(self, mouseState, mousePos, world, Camera_X, Camera_Y, l):
        if mouseState[0]:
            x = int(int(mousePos[0]+Camera_X*BLOCK_SIZE)//BLOCK_SIZE)
            y = int(int(mousePos[1]+Camera_Y*BLOCK_SIZE)//BLOCK_SIZE)
            try:
                if world[y][x] == 0:
                    world[y][x] = 4
                    l.append([x,y])
            except:
                print("Tried to build out of bounds")
        if mouseState[2]:
            x = int(int(mousePos[0]+Camera_X*BLOCK_SIZE)//BLOCK_SIZE)
            y = int(int(mousePos[1]+Camera_Y*BLOCK_SIZE)//BLOCK_SIZE)
            try:
                if world[y][x] == 4:
                    world[y][x] = 0
                    print("Deleted")
                    print(len(l))
                    for i in range(len(l)):
                        if l[i] == [x,y]:
                            del l[i]
                            print(len(l))
                            break
            except:
                print("Tried to delete out of bounds")
        return [world,l]
            
    
    def draw(self,window : pygame.surface, CAMERA_X, CAMERA_Y):
        window.blit(self.img, pygame.Rect((self.x-CAMERA_X)*BLOCK_SIZE,(self.y-CAMERA_Y)*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))