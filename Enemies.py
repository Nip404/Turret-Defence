import pygame
import math
import random

class Enemy:
    # Stats
    basehealth = 100
    speed = 2
    size = 15
    spawnrate = 10
    
    def __init__(self,surface,s):
        self.health = self.basehealth

        # Movement data
        sector = random.randint(0,3)
        self.pos = [random.randint(0,s[0]) if sector in [0,2] else (0 if sector == 1 else 500),random.randint(0,s[1]) if sector in [1,3] else (0 if not sector else 500)]
        self.vector = self.normalise([[i/2 for i in s][i] - self.pos[i] for i in range(2)])

        # Drawing data
        self.surf = surface
        self.s = s
        self.rect = pygame.Rect(self.pos[0]-self.size,self.pos[1]-self.size,self.size*2,self.size*2)

    @staticmethod
    # Static method returns a unit vector
    def normalise(vector):
        return [i/math.sqrt(sum(i**2 for i in vector)) for i in vector]

    def draw(self):
        pygame.draw.circle(self.surf,(200,0,0),list(map(int,self.pos)),self.size,0)
        pygame.draw.rect(self.surf,(255,0,0),list(map(int,(self.pos[0]-25,self.pos[1]-25,50,10))),0)
        pygame.draw.rect(self.surf,(0,255,0),list(map(int,(self.pos[0]-25,self.pos[1]-25,50*(self.health/self.basehealth),10))),0)

    def spawn(self,enemies,frame,fps,boss):
        # Returns original list if it is not the correct time, otherwise returns list with appended enemy
        return enemies + [Enemy(self.surf,self.s)] if not frame % (6*self.spawnrate) else enemies

    def animate(self):
        self.pos = [self.pos[i] + (self.speed*self.vector[i]) for i in range(2)]
        self.rect = pygame.Rect(self.pos[0]-self.size,self.pos[1]-self.size,self.size*2,self.size*2)

class Boss:
    def __init__(self,surface,s):
        # Stats
        self.alive = False
        self.size = 25
        self.speed = 1
        self.basehealth = 500
        self.health = self.basehealth
        self.spawnrate = 100
        self.damaged = False # Appears darker when not damaged

        # Other
        self.surf = surface
        self.s = s
        self.rect = pygame.Rect(-1,-1,0,0)
        
    def respawn(self,frame):
        # Resets main variables
        if not frame % (6 * self.spawnrate) and not self.alive:
            sector = random.randint(0,3)
            self.pos = [random.randint(0,self.s[0]) if sector in [0,2] else (0 if sector == 1 else 500),random.randint(0,self.s[1]) if sector in [1,3] else (0 if not sector else 500)]
            self.vector = Enemy.normalise([[i/2 for i in self.s][i] - self.pos[i] for i in range(2)])
            self.alive = True
            self.health = self.basehealth
            self.damaged = False

    def draw(self):
        if not self.alive:
            return
        
        pygame.draw.circle(self.surf,((100,100,0) if not self.damaged else (200,0,0)),list(map(int,self.pos)),self.size,0)
        pygame.draw.rect(self.surf,(255,0,0),(self.pos[0]-25,self.pos[1]-40,50,10),0)
        pygame.draw.rect(self.surf,(0,255,0),(self.pos[0]-25,self.pos[1]-40,50 * (self.health/self.basehealth),10),0)

    def animate(self):
        if not self.alive:
            return
        
        self.pos = [self.pos[i] + (self.speed*self.vector[i]) for i in range(2)]
        self.rect = pygame.Rect(self.pos[0]-self.size,self.pos[1]-self.size,self.size*2,self.size*2)
