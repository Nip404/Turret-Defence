import pygame
import time

class Button0:
    def __init__(self,surf,font):
        self.surf = surf
        self.pos = [50,50]
        self.text = font.render("Prestige",True,(0,0,0))
        self.available = False
        self.rect = pygame.Rect(self.pos[0]-40,self.pos[1]-40,80,80)

    def draw(self):
        pygame.draw.circle(self.surf,(255,255,255) if not self.available else (0,255,0),self.pos,40,0)
        self.surf.blit(self.text,self.text.get_rect(center=self.pos))

    def update(self,banner):
        self.available = True
        
        for panel in banner.buttons:
            for name,button in panel.items():
                if not (button["used"] == button["use limit"] or name in ["Mags","Regen"]):
                    self.available = False
                    
    def onClick(self,mouse,banner,player,enemies,boss,prestige):
        if pygame.Rect(mouse[0]-1,mouse[1]-501,2,2).colliderect(self.rect) and self.available:
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
    pass

class Button2:
    pass

class Button3:
    pass

class Button4:
    pass

class Button5:
    pass

class Button6:
    pass

class Button7:
    pass

class Button8:
    pass

class Button9:
    pass
