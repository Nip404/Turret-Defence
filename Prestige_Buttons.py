from Timer import Timer

import pygame
import time

pygame.init()
tmp = pygame.display.set_mode([1,1])

r = lambda pos,rad: pygame.Rect(pos[0]-rad,pos[1]-rad,rad*2,rad*2)

logos = []
for i in range(1,10):
    try:
        logos.append(pygame.image.load(f"Logos/logo{i}.png").convert())
    except:
        logos.append(pygame.Surface([30,30]))
        
logo1,logo2,logo3,logo4,logo5,logo6,logo7,logo8,logo9 = logos

class Button0:
    def __init__(self,surf,font):
        self.surf = surf
        self.pos = [50,50]
        self.radius = 40
        self.text = font.render("Prestige",True,(0,0,0))
        self.available = False
        self.rect = r(self.pos,self.radius)

    def draw(self):
        pygame.draw.circle(self.surf,(255,255,255) if not self.available else (0,255,0),self.pos,self.radius,0)
        self.surf.blit(self.text,self.text.get_rect(center=self.pos))

    def update(self,banner):
        self.available = True
        
        for panel in banner.buttons:
            for name,button in panel.items():
                if not (button["used"] == button["use limit"] or name in ["Mags","Regen"]):
                    self.available = False
                    
    def onClick(self,mouse,banner,player,enemies,boss,prestige):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.available:
            self.available = False

            for panel in banner.buttons:
                for button in panel.values():
                    button["used"] = 0

            player.init_stats(prestige+1)
            boss.init_stats(prestige+1)

            for i in enemies:
                i.init_stats(prestige+1)

            return prestige+1
        return prestige

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
        self.player.damage = 1000 if self.timer.status == "ability" else self.player.damage

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

class Button6: # Triple cannon for 5 seconds, cooldown 10
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

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button7: # Ability to fire 60 bullets at once around the circumference of the turret for 5 seconds, cooldown 20
    def __init__(self,surf):
        self.pos = [613,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(5,20)

    def update(self):
        self.timer.update()

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

class Button8: # Slows time by half for 10 seconds, cooldown 20 seconds
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

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new

class Button9: # No-click shooting (hold left-click) for 10 seconds, cooldown 10
    def __init__(self,surf):
        self.pos = [771,50]
        self.radius = 30
        self.surf = surf
        self.unlocked = False
        self.rect = r(self.pos,self.radius)

        self.timer = Timer(10,10)

    def update(self):
        self.timer.update()

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

    def onClick(self,mouse):
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.rect) and self.unlocked:
            self.timer.start()

    @property
    def unlock(self):
        return self.unlocked

    @unlock.setter
    def unlock(self,new):
        self.unlocked = new
