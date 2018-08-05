from Player import Turret
from Enemies import Enemy,Boss
from Banners import Banner,Prestige_Banner
from Error import CustomException

import pygame
import sys

# SETTINGS
'''
Difficulty (only affects speed of enemies):

1 - playtest
2 - easy
3 - normal (Default)
4 - hard
5 - very hard
6 - impossible

Note: higher difficulty levels may not run properly depending on cpu strength
'''
Difficulty = 3

'''
Smaller value == more detail

Default: 25
Original: 50

Night mode:
    Min: 1
    Max: 14
Day mode:
    Min: 14
    Max: 350
'''
background_detail = 25

# Initialisations
try:
    fps = {1:15,2:40,3:60,4:80,5:100,6:120}[Difficulty]
except KeyError as e:
    print(f"Error: '{e}' not found, Defaulting difficulty to level 3.")
    fps = 60
finally:
    size = [850,600] # Window Size
    s = [500,500] # Playable screen size
    
    pygame.init()
    screen = pygame.display.set_mode(size,0,32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Turret Defence v8 by NIP")

    # Fonts
    big = pygame.font.SysFont("Garamond MS",60)
    med = pygame.font.SysFont("Garamond MS",40)
    small = pygame.font.SysFont("Garamond MS",18)

    if 0 < background_detail < 15:
        night_mode = True
    elif 15 <= background_detail <= 350:
        night_mode = False
    else:
        raise CustomException("Error: Number is out of bounds. Please change 'background_detail'")

def background():
    # Draws green circles on background backwards (from big to small)
    for p,i in enumerate(reversed(range(50,401,background_detail))):
        pygame.draw.circle(screen,(0,(p*1.4 if night_mode else 130+(p*5)),0),[int(i/2) for i in s],i,0) 

#Pause Screen is blitted over main surface
def get_pause_screen():
    p = pygame.Surface(s)
    p.set_alpha(100) # Transparent cover (0 = transparent, 255 = opaque)
    p.fill((0,0,0))

    head = big.render("Game Paused",True,(255,255,255))
    foot = med.render("Press ESC to resume",True,(255,255,255))

    p.blit(head,head.get_rect(center=[s[0]/2,s[1]/3]))
    p.blit(foot,foot.get_rect(center=[s[0]/2,s[1]*0.6]))

    return p

def main():
    startscreen()
    pause_cover = get_pause_screen()

    # Loops while user plays; can span over multiple games
    while True:
        turret = Turret(screen,s)
        enemies = []
        boss = Boss(screen,s)
        frame = 1 # Causes an issue with boss spawn: 0 % anything = 0
        banner = Banner(screen,s,small,med,turret,Enemy,boss)
        prestige_banner = Prestige_Banner(screen,small)

        paused = False

        # Main Game Loop
        while True:
            clock.tick(fps)

            # Main event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    prestige_banner.onClickMainButton(pygame.mouse.get_pos(),banner,turret,enemies,boss)
                    
                    # Checks if mouse is within banner pos, and updates money and score
                    if banner.rect(pygame.mouse.get_pos(),1).colliderect(pygame.Rect(s[0],0,banner.banner_res[0],banner.banner_res[1])):
                        # Changes mouse pos relative to banner pos
                        banner.click([i-s[0] if not p % 2 else i for p,i in enumerate(pygame.mouse.get_pos())],enemies)

                    # If not clicking on banner and left clicked
                    elif event.button == 1:
                        turret.shoot(pygame.mouse.get_pos())

                elif event.type == pygame.KEYDOWN:
                    # Refills rounds (conditions are verified in function)
                    if event.key == pygame.K_r:
                        turret.reload()

                    # Toggles pause screen
                    elif event.key == pygame.K_ESCAPE:
                        paused = not paused

            # Updates
            pygame.display.set_caption(f"Turret Defence v8 by NIP |||| Prestige: {prestige_banner.prestige}")
            enemies,boss = turret.collide(enemies,boss)
            prestige_banner.update(banner)

            # Deletes bullets which are off-screen, and enemies with negative health
            turret.clean()
            enemies = [i for i in enemies if i.health > 0]

            # Drawing
            background()
            turret.draw()
            banner.update(clock.get_fps())
            boss.draw()
            banner.draw()
            prestige_banner.draw()

            for e in enemies:
                e.draw()

                if not paused:
                    e.animate()

            if not paused:
                # Animation and spawning
                turret.animate()

                # Enemies only spawn when boss is dead
                if not boss.alive:
                    enemies = Enemy(screen,s).spawn(enemies,frame,fps,boss)
                    
                boss.respawn(frame)        
                turret.regen(frame,fps)
                boss.animate()

                frame += 1
            else:
                screen.blit(pause_cover,(0,0))

            pygame.display.flip()

            # If game has ended
            if turret.check_end():
                break

        endscreen(turret,enemies,boss,banner)

def startscreen():
    head = big.render("Turret Defence v8",True,(0,0,0))
    foot = med.render("Click to play",True,(0,0,0))

    while True:
        # Main event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Exits function
                return
            
        # Visual Decoration
        screen.fill((131,111,255))
 
        pygame.draw.rect(screen,(0,0,0),(100,100,40,40),0)
        pygame.draw.circle(screen,(255,255,255),(120,120),10,0)
        pygame.draw.line(screen,(255,255,255),(120,119),(150,119),20)
        pygame.draw.circle(screen,(255,0,0),(620,119),20,0)

        for i in range(7):
            pygame.draw.line(screen,[(80,0,0),(100,0,0),(150,0,0),(200,0,0),(255,0,0),(255,100,0),(255,200,0)][i],(0,500),(size[0],500),[50,40,30,20,10,5,2][i])
        for i in range(4):
            pygame.draw.circle(screen,(255,255,0),(((i+1) * 100) + 120,119),4,0)
        for i in range(2):        
            pygame.draw.rect(screen,([255,0] if not i % 2 else [0,255])+[0],(595,90,50-(20*i),10),0)

        screen.blit(head,head.get_rect(center=[size[0]/2,s[1]*0.45]))
        screen.blit(foot,foot.get_rect(center=[size[0]/2,s[1]*0.65]))

        pygame.display.flip()

def endscreen(turret,enemies,boss,banner):
    head = big.render("Final Score: %d" % turret.score,True,(0,0,0))
    head2 = big.render("%d kills" % turret.kills,True,(0,0,0))
    foot = med.render("Press Space to play again",True,(0,0,0))

    # Similar to pause screen
    end = pygame.Surface(size)
    end.set_alpha(150)
    end.fill((255,0,0))

    while True:
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        # Drawing static game 
        background()
        turret.draw()
        boss.draw()
        banner.draw()

        for i in enemies:
            i.draw()

        # Endscreen
        screen.blit(end,(0,0))

        screen.blit(head,head.get_rect(center=[size[0]/2,size[1]*0.35]))
        screen.blit(head2,head2.get_rect(center=[size[0]*(107/180)-85,size[1]/2]))
        screen.blit(foot,foot.get_rect(center=[size[0]/2,size[1]*0.65]))

        pygame.display.flip()
        
if __name__ == "__main__":
    main()
