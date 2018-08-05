import pygame
import math

class Bullet:
    def __init__(self,mouse,s,size):
        self.vector = self.normalise([mouse[i] - [i/2 for i in s][i] for i in range(2)])
        self.pos = [i/2 for i in s]
        self.size = size
        self.rect = pygame.Rect(self.pos[0]-self.size,self.pos[1]-self.size,self.size*2,self.size*2)

    @staticmethod
    # Static method returns a unit vector
    def normalise(vector):
        return [i/math.sqrt(sum(i**2 for i in vector)) for i in vector]

    def animate(self,speed=4):
        # Adds vector to current pos
        self.pos = [self.pos[i] + (speed*self.vector[i]) for i in range(2)]

    def draw(self,surf):
        pygame.draw.circle(surf,(255,255,0),list(map(int,self.pos)),int(self.size),0)
        self.rect = pygame.Rect(self.pos[0]-self.size,self.pos[1]-self.size,self.size*2,self.size*2)

class Turret:
    def __init__(self,surface,s):
        # Main game variables
        self.surf = surface
        self.s = s
        self.rect = pygame.Rect(self.s[0]/2-25,self.s[1]/2-25,50,50)
        self.bullets = []
        self.kills = 0
        self.money = 10000000
        self.score = 0

        self.init_stats(prestige=0)

    def init_stats(self,prestige):
        self.maxhealth = 100 - (5 * prestige)
        self.health = self.maxhealth

        self.regen_factor = 1
        self.regen_rate = 5

        self.bullet_speed = 4 - (0.2 * prestige)
        self.bullet_size = 4 - (0.2 * prestige)
        self.damage = 25 - (2 * prestige)
        self.round_size = 20 - prestige
        self.magasines = 14
        self.rounds = self.round_size

        self.mag_cost = 100 + (20 * prestige)
        self.profit = 10 - (0.5 * prestige)

    def animate(self):
        for bullet in self.bullets:
            bullet.animate(self.bullet_speed)

    def collide(self,enemies,boss):
        # Checks for overflow
        if self.health > self.maxhealth:
            self.health = self.maxhealth

        # Used because deleting items whilst looping in for loop disrupts indexing method
        dead_enemies = []
        used_bullets = []

        # Tracks location in enemy list (p) and enemy object (i)
        for p,i in enumerate(enemies):
            # If enemy collided with turret
            if self.rect.colliderect(i.rect):
                # Lose health inversely proportional to damage done
                self.health -= 5 * (i.health/i.basehealth)
                dead_enemies.append(p)
                self.score += self.profit

            # Tracks location in bullets list (p2) and bullet object (b)
            for p2,b in enumerate(self.bullets):
                # if bullets hit enemy
                if i.rect.colliderect(b.rect):
                    self.money += self.profit
                    self.score += self.profit
                    enemies[p].health -= self.damage
                    used_bullets.append(p2)
                    
                    # If enemy is dead
                    if not i.health:
                        dead_enemies.append(p)
                        self.money += self.profit
                        self.score += self.profit
                        self.kills += 1

        for p,b in enumerate(self.bullets):
            # If bullet hit boss
            if b.rect.colliderect(boss.rect) and boss.alive:
                boss.damaged = True
                boss.health -= self.damage
                boss.alive = boss.health > 0 # Uses boolean instead of "if" statement
                self.money += self.profit
                self.score += self.profit
                used_bullets.append(p)

                # If dead
                if not boss.alive:
                    self.kills += 1
                    self.money += self.profit * 5
                    self.score += self.profit * 5

        # If boss is still alive and is colliding with turret
        if boss.rect.colliderect(self.rect) and boss.alive:
            self.health -= 20 * (boss.health/boss.basehealth)
            boss.alive = False
            self.score += 5 * self.profit

        # Removes used bullets and dead enemies with updated money and score
        self.bullets = [i for p,i in enumerate(self.bullets) if not p in used_bullets]
        return [i for p,i in enumerate(enemies) if not p in dead_enemies],boss

    def shoot(self,mouse):
        # Dosen't shoot if rounds are empty or mouse in clicking on turret or mouse is outside playable area
        if not self.rounds or pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) or not all(0 <= i <= self.s[p] for p,i in enumerate(mouse)):
            return

        # New bullet
        self.bullets.append(Bullet(mouse,self.s,self.bullet_size))
        self.rounds -= 1

    def reload(self):
        # Must empty clip before reloading, and must have a magasine available or be able to afford one
        if not self.rounds and (self.magasines or self.money >= self.mag_cost):
            self.magasines -= 1
            self.rounds = self.round_size

    def regen(self,frame,fps):
        # Regenerates by a certain factor at a certain rate (both are upgradable)
        if not frame % (fps * self.regen_rate):
            self.health += self.regen_factor

    def check_end(self):
        # Ends game if dead or it is not possible to shoot anymore
        return True if (self.health <= 0 or (self.magasines <= 0 and self.money < self.mag_cost and not self.rounds)) else False

    def draw(self):
        # Turret body
        pygame.draw.rect(self.surf,(100,100,100),list(map(int,(self.s[0]/2-25,self.s[1]/2-25,50,50))),0)
        pygame.draw.rect(self.surf,(255,0,0),list(map(int,(self.s[0]/2-50,self.s[1]/2-50,100,20))),0)

        if self.health > 0:
            pygame.draw.rect(self.surf,(0,255,0),list(map(int,(self.s[0]/2-50,self.s[1]/2-50,100*(self.health/self.maxhealth),20))),0)

        pygame.draw.circle(self.surf,(44,44,44),[int(i/2) for i in self.s],10,0)

        # Turret barrel
        pass
        
        # Bullets
        for bullet in self.bullets:
            bullet.draw(self.surf)

    def clean(self):
        # Deletes any bullets if they are outside playable area
        self.bullets = [i for i in self.bullets if not any(e < 0 or e > self.s[p] for p,e in enumerate(i.pos))]
