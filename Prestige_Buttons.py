from Player import Bullet
from Timer import Timer

import pygame
import time

pygame.init()
tmp = pygame.display.set_mode([1,1])

r = lambda pos,rad: pygame.Rect(pos[0]-rad,pos[1]-rad,rad*2,rad*2) # Creates a rect from centre and radius
logo1,logo2,logo3,logo4,logo5,logo6,logo7,logo8,logo9 = [pygame.image.load(f'Logos/logo{i}.png').convert() for i in range(1,10)]

# Main prestige button
class Button0:
    def __init__(self,banner,surf,font):
        self.surf = surf
        self.pos = [50,50]
        self.radius = 40
        self.text = font.render("Prestige",True,(0,0,0))
        self.available = False
        self.rect = r(self.pos,self.radius)

        self.banner = banner

    def draw(self):
        # Draws white is not available, otherwise, draws green
        pygame.draw.circle(self.surf,(255,255,255) if not self.available else (0,255,0),self.pos,self.radius,0)
        self.surf.blit(self.text,self.text.get_rect(center=self.pos))

    # Uses negative feedback loop to check prestige availability
    def update(self):
        self.available = True
        
        for panel in self.banner.buttons:
            for name,button in panel.items():
                if not (button["used"] == button["use limit"] or name in ["Mags","Regen"]):
                    self.available = False

    def onClick(self,mouse,player,enemies,boss,prestige):
        # If player decides to prestige
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.available:
            self.available = False

            # Resets button stats
            for panel in self.banner.buttons:
                for button in panel.values():
                    button["used"] = 0

            # Resets stats according to new prestige
            player.init_stats(prestige+1)
            boss.init_stats(prestige+1)

            for i in enemies:
                i.init_stats(prestige+1)

            return prestige+1
        return prestige

'''
Each button is initialised with a surface to draw on as well as custom coords,
and sometimes other things which allow for powerups.

The update function updates the internal timer and sometimes other procedures.
The onClick function begins the timer if available. Note that
the timer itself has a builtin system which checks if it is available before starting.

Some functions may have several properties, which serve as identifiers
to other functions to signal them to do something.
However all function have a setter, which sets their unlocked state to
true once the correct prestige has been achieved.

The draw function draws the logo, a border and fills in the background.
If the button has not been unlocked yet, tints the logo darker.
If the button is currently using the ability, it tints it green.
If the button is currently on cooldown, it tints it red.
'''

class Button1:
    def __init__(self,surf,player):
        self.pos = [139,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(10,5)
        self.player = player

    def update(self):
        self.timer.update()
        self.player.health = self.player.maxhealth if self.timer.status == "ability" else self.player.health

    def draw(self):
        self.surf.blit(logo1,logo1.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button2:
    def __init__(self,surf,player):
        self.pos = [218,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(5,20)
        self.player = player

    def update(self):
        self.timer.update()
        
    def draw(self):
        self.surf.blit(logo2,logo2.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    @property
    def instakill(self):
        return {"cooldown":False,"ability":True,"waiting":False}[self.timer.status]

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button3:
    def __init__(self,surf):
        self.pos = [297,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(5,10)

    def update(self):
        self.timer.update()

    def draw(self):
        self.surf.blit(logo3,logo3.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    @property
    def targeted(self):
        return {"cooldown":False,"ability":True,"waiting":False}[self.timer.status]

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button4:
    def __init__(self,surf,player):
        self.pos = [376,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(20,10)
        self.player = player

    def update(self):
        self.timer.update()

        if self.timer.status == "ability" and not self.player.rounds:
            self.player.rounds = self.player.round_size

    def draw(self):
        self.surf.blit(logo4,logo4.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()
            self.player.magasines += 2

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button5:
    def __init__(self,surf):
        self.pos = [455,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(5,20)

    def update(self):
        self.timer.update()

    def draw(self):
        self.surf.blit(logo5,logo5.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    @property
    def gold_rush(self):
        return {"cooldown":False,"ability":True,"waiting":False}[self.timer.status]

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button6:
    def __init__(self,surf):
        self.pos = [534,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(5,10)

    def update(self):
        self.timer.update()

    def draw(self):
        self.surf.blit(logo6,logo6.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    @property
    def shotgun(self):
        return {"cooldown":False,"ability":True,"waiting":False}[self.timer.status]

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button7: 
    def __init__(self,surf,player,s):
        self.pos = [613,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(1,15)
        self.player = player
        self.s = s

        self.shots = 0
        self.max = 5

    def update(self):
        self.timer.update()

        if self.timer.status == "ability" and self.shots <= self.max: 
            for i in range(60):
                b = Bullet([0,0],self.s,self.player.bullet_size)
                b.vector = Bullet.rotate([1,0],i*6)
                self.player.bullets.append(b)

            self.shots += 1

        if self.timer.status == "waiting":
            self.shots = 0

    def draw(self):
        self.surf.blit(logo7,logo7.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)
        
    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button8: 
    def __init__(self,surf):
        self.pos = [692,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(10,20)

    def update(self):
        self.timer.update()

    def draw(self):
        self.surf.blit(logo8,logo8.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    @property
    def slowmo(self):
        return {"cooldown":False,"ability":True,"waiting":False}[self.timer.status]

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button9: 
    def __init__(self,surf,player,s):
        self.pos = [771,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(10,10)
        self.player = player
        self.s = s
        
    def update(self,shotgun):
        self.timer.update()

        if self.timer.status == "ability" and pygame.mouse.get_pressed()[0] and not pygame.Rect(pygame.mouse.get_pos()[0]-1,pygame.mouse.get_pos()[1]-1,2,2).colliderect(self.player.rect):
            self.player.bullets.append(Bullet(pygame.mouse.get_pos(),self.s,self.player.bullet_size))

            if shotgun:
                a,b = Bullet(pygame.mouse.get_pos(),self.s,self.player.bullet_size),Bullet(pygame.mouse.get_pos(),self.s,self.player.bullet_size)

                a.vector = Bullet.normalise(Bullet.rotate(a.vector,10))
                b.vector = Bullet.normalise(Bullet.rotate(b.vector,-10))
                
                self.player.bullets += [a,b]

    def draw(self):
        self.surf.blit(logo9,logo9.get_rect(center=self.pos))
        pygame.draw.circle(self.surf,(50,50,150),self.pos,40,10)

        if not self.unlocked:
            colour = (50,50,50)
        elif self.timer.status == "cooldown":
            colour = (255,0,0)
        elif self.timer.status == "ability":
            colour = (0,255,0)
        else:
            colour = None

        if colour is not None:
            cover = pygame.Surface([60,60],pygame.SRCALPHA,32)
            pygame.draw.circle(cover,(*colour,150),(30,30),30,0)
            self.surf.blit(cover,cover.get_rect(center=self.pos))

        pygame.draw.circle(self.surf,(0,0,0),self.pos,self.radius,5)

    @property
    def auto(self):
        return {"cooldown":False,"ability":True,"waiting":False}[self.timer.status]

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new
