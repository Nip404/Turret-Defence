from Prestige_Buttons import Button0,Button1,Button2,Button3,Button4,Button5,Button6,Button7,Button8,Button9

import pygame
import math
import time

class Banner:
    def __init__(self,surf,s,font,font2,turret,enemy,boss):
        # Class-wide scoped variables used for graphics
        self.surf = surf
        self.s = s
        self.font = font
        self.font2 = font2
        self.startx = self.s[0]
        self.banner_res = [self.surf.get_width()-self.s[0],s[1]]
        self.banner = self.get_banner(self.banner_res)
        self.buttonsize = 27

        self.turret = turret
        self.enemy = enemy
        self.boss = boss

        # Upgrades on banner
        self.buttons = [{
                "Health":{"rect":self.rect([105,200],self.buttonsize),"var":{"class":self.turret,"name":"maxhealth"},"effect":25,"used":0,"use limit":5,"money":300},
                "Damage":{"rect":self.rect([165,200],self.buttonsize),"var":{"class":self.turret,"name":"damage"},"effect":25,"used":0,"use limit":5,"money":200},
                "R Factor":{"rect":self.rect([225,200],self.buttonsize),"var":{"class":self.turret,"name":"regen_factor"},"effect":5,"used":0,"use limit":5,"money":500},
                "R Rate":{"rect":self.rect([285,200],self.buttonsize),"var":{"class":self.turret,"name":"regen_rate"},"effect":1,"used":0,"use limit":4,"money":500}
            },{
                "Speed":{"rect":self.rect([105,260],self.buttonsize),"var":{"class":self.turret,"name":"bullet_speed"},"effect":2,"used":0,"use limit":5,"money":100},
                "Size":{"rect":self.rect([165,260],self.buttonsize),"var":{"class":self.turret,"name":"bullet_size"},"effect":2,"used":0,"use limit":5,"money":500},
                "Rounds":{"rect":self.rect([225,260],self.buttonsize),"var":{"class":self.turret,"name":"round_size"},"effect":5,"used":0,"use limit":5,"money":500}
            },{
                "Size":{"rect":self.rect([105,320],self.buttonsize),"var":{"class":self.enemy,"name":"size"},"effect":4,"used":0,"use limit":5,"money":100},
                "Speed":{"rect":self.rect([165,320],self.buttonsize),"var":{"class":self.enemy,"name":"speed"},"effect":-0.25,"used":0,"use limit":5,"money":300},
                "Health":{"rect":self.rect([225,320],self.buttonsize),"var":{"class":self.enemy,"name":"basehealth"},"effect":-10,"used":0,"use limit":5,"money":200},
                "Spawn":{"rect":self.rect([285,320],self.buttonsize),"var":{"class":self.enemy,"name":"spawnrate"},"effect":1,"used":0,"use limit":5,"money":300}
            },{
                "Size":{"rect":self.rect([105,380],self.buttonsize),"var":{"class":self.boss,"name":"size"},"effect":20,"used":0,"use limit":5,"money":200},
                "Speed":{"rect":self.rect([165,380],self.buttonsize),"var":{"class":self.boss,"name":"speed"},"effect":-0.1,"used":0,"use limit":5,"money":400},
                "Health":{"rect":self.rect([225,380],self.buttonsize),"var":{"class":self.boss,"name":"basehealth"},"effect":-50,"used":0,"use limit":5,"money":300}
            },{
                "Mags":{"rect":self.rect([105,440],self.buttonsize),"var":{"class":self.turret,"name":"magasines"},"effect":1,"used":0,"use limit":math.inf,"money":100},
                "Profit":{"rect":self.rect([165,440],self.buttonsize),"var":{"class":self.turret,"name":"profit"},"effect":10,"used":0,"use limit":5,"money":500},
                "Regen":{"rect":self.rect([225,440],self.buttonsize),"var":{"class":self.turret,"name":"health"},"effect":500,"used":0,"use limit":math.inf,"money":500}
            }]

    def rect(self,pos,radius):
        # Creates rect from circle
        return pygame.Rect(pos[0]-radius,pos[1]-radius,radius*2,radius*2)

    def update(self,fps):
        # Used for updating banner and player/enemy/boss stats when upgrading
        self.fps = fps

        # Draws changed on banner
        self.update_graphics()

    def click(self,mouse,enemies):
        # Looping through each section of buttons
        for panel in self.buttons:
            # Looping through each button in section
            for name,button in panel.items():

                # If user clicked on the current button, and the upgrade is not maxed out and user can afford it (and if user clicked for regen but turret is at max health)
                if self.rect(mouse,1).colliderect(button["rect"]) and button["used"] < button["use limit"] and self.turret.money >= button["money"] and not (name == "Regen" and button["var"]["class"].health >= button["var"]["class"].maxhealth):

                    # Updates the variable in the class to the variable + effect (essentially a += between classes)
                    
                    try: # Special case for enemies, since they save their attributes in instances
                        setattr(button["var"]["class"],button["var"]["name"],getattr(button["var"]["class"],button["var"]["name"])+button["effect"])
                    except:
                        pass
                    
                    button["used"] += 1
                    self.turret.money -= button["money"]
                    self.turret.score += 100 * button["used"]

    def update_graphics(self):
        self.banner.fill((255,255,255))

        # Headers
        for p,i in enumerate([self.font2.render("FPS: %s" % str(self.fps)[:6],True,(0,0,0)),self.font2.render("Kills: %d" % self.turret.kills,True,(0,0,0)),self.font2.render("Score: %d" % self.turret.score,True,(0,0,0)),self.font2.render("Money: %d" % self.turret.money,True,(0,0,0)),self.font.render("Turret Health: %d/%d" % (self.turret.health,self.turret.maxhealth),True,(0,0,0))]):
            self.banner.blit(i,i.get_rect(center=[[self.banner_res[0]/4,self.banner_res[1]/20],[self.banner_res[0]/4,self.banner_res[1]*0.14],[self.banner_res[0]*0.75,self.banner_res[1]/20],[self.banner_res[0]*0.75,self.banner_res[1]*0.14],[self.banner_res[0]/2,self.banner_res[1]/5]][p]))

        # Round graphics
        rounds = self.font.render("Bullets left in round:",True,(0,0,0))
        R = rounds.get_rect(topleft=[self.banner_res[0]/20,self.banner_res[1]/4])
        self.banner.blit(rounds,R)

        gap_r = (self.banner_res[0] - R.right)/((2*self.turret.round_size)+1)
        c = [R.right+gap_r,self.banner_res[0]-gap_r]

        pygame.draw.rect(self.banner,(255,0,0),(c[0],R.bottom,c[1]-c[0],R.top-R.bottom),0)
        if (c[1]-c[0]) * (self.turret.rounds/self.turret.round_size):
            pygame.draw.rect(self.banner,(0,255,0),(c[0],R.bottom,(c[1]-c[0]) * (self.turret.rounds/self.turret.round_size),R.top-R.bottom),0)

        # Magasine graphics
        mag = self.font.render("Magasines left:",True,(0,0,0))
        M = mag.get_rect(topleft=[self.banner_res[0]/20,self.banner_res[1]*0.3])
        self.banner.blit(mag,M)

        gap_m = (self.banner_res[0] - M.right)/((2*self.turret.magasines)+1)
        
        for p,i in enumerate(range(1+(2*self.turret.magasines))):
            pygame.draw.rect(self.banner,(255,255,255) if not i % 2 else (0,255,0),(M.right+(p*gap_m),M.bottom,gap_m,M.top-M.bottom),0)

        # Draw buttons
        for panel in self.buttons:
            for name,data in panel.items():
                # Draws an intensity of red directly proportional to amount of times the upgrade has been bought. RED == 255 when upgrade has been maxed out
                pygame.draw.circle(self.banner,((255,255-(255*(data["used"]/data["use limit"])),255-(255*(data["used"]/data["use limit"])))),data["rect"].center,self.buttonsize,0)

                # If upgrade can be bought, previous red circle is drawn over by a green one
                if self.turret.money >= data["money"] and data["used"] < data["use limit"]:
                    pygame.draw.circle(self.banner,(0,255,0),data["rect"].center,self.buttonsize,0)

                # Outline
                pygame.draw.circle(self.banner,(0,0,0),data["rect"].center,self.buttonsize,2)

                # Name
                n = self.font.render(name,True,(0,0,0))
                self.banner.blit(n,n.get_rect(center=data["rect"].center))

        # Coloured tags
        for p,i in enumerate([self.font.render("Player:",True,(0,0,0)),self.font.render("Bullets:",True,(255,200,0)),self.font.render("Enemies:",True,(255,0,0)),self.font.render("Bosses:",True,(0,0,255)),self.font.render("Supplies:",True,(0,255,0))]):
            self.banner.blit(i,i.get_rect(topright=[60,165+([1,3,5,7,9][p]*30)]))

    # Initial banner
    def get_banner(self,resolution):
        b = pygame.Surface(resolution)
        b.fill((255,255,255))

        return b

    def draw(self):
        self.surf.blit(self.banner,(self.startx,0))

class Prestige_Banner:
    def __init__(self,surf,font,player,banner,s):
        self.surf = surf
        self.font = font
        self.prestige = 0 # Main prestige tracker

        self.prestige_banner = self.get_banner()
        self.main_button = Button0(banner,self.prestige_banner,self.font) # All buttons
        self.buttons = [Button1(self.prestige_banner,player),
                        Button2(self.prestige_banner,player),
                        Button3(self.prestige_banner),
                        Button4(self.prestige_banner,player),
                        Button5(self.prestige_banner),
                        Button6(self.prestige_banner),
                        Button7(self.prestige_banner,player,s),
                        Button8(self.prestige_banner),
                        Button9(self.prestige_banner,player,s)]

    # Updates individual timers and prestige availablity
    def update(self):
        self.main_button.update()
        self.buttons[-1].update(self.buttons[5].shotgun)

        for i in self.buttons[:-1]:
            i.update()

    # Button interaction and prestige updates
    def onClick(self,mouse,player,enemies,boss):
        old = self.prestige
        self.prestige = self.main_button.onClick(mouse,player,enemies,boss,self.prestige)

        if old < self.prestige and not self.prestige == 10:
            self.buttons[old].unlock = True

        for i in self.buttons:
            i.onClick(mouse)
            
    def draw(self):
        # Draws each button and then blits updated banner
        self.main_button.draw()

        for i in self.buttons:
            i.draw()
        
        self.surf.blit(self.prestige_banner,(0,500))

    def get_banner(self):
        p = pygame.Surface([self.surf.get_width(),100])
        p.fill((50,50,150))

        return p
