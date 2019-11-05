# Turret-Defence
A turret based game in Python 3.x using the Pygame library.

# How to play
The game revolves around a single turret in the middle of a field.\
To earn money and score points, click around the turret to shoot bullets.\
When your magasine is empty, press 'r' to reload.

Be aware of your magasines (you can see the amount on the banner on the right),\
as if you run out and cannot afford any more, you lose.

You can upgrade stats which will buff/nerf certain aspects of the game using money.\
The buttons on the banner will light up green is you can buy it,\
and a certain shade of red depending on how close it is to being maxed out.

When you have maxed out all your upgrades, the prestige button will light up, and click it to reset all stats to harder than before.\
With each prestige comes a new powerup, which you can use on a cooldown timer.\
The end goal is to unlock the 10th prestige, at which point you finish the game.

# Prestige powerups:
- Prestige 0: Nothing
- Prestige 1: Immunity for 10 seconds, cooldown 5 seconds
- Prestige 2: Instant kills for 5 seconds, cooldown 20 seconds
- Prestige 3: Auto-aim for 5 seconds, cooldown 10 seconds
- Prestige 4: 2 free magasines and free auto reload for 20 seconds, cooldown 10 seconds
- Prestige 5: Doubled money and score gain for 5 seconds, cooldown 20 seconds
- Prestige 6: Triple cannon for 5 seconds, cooldown 10 seconds
- Prestige 7: Sprays a wave of bullets around the circumference of the turret for 1 second, cooldown 15 seconds
- Prestige 8: Slows time by half for 10 seconds, cooldown 20 seconds
- Prestige 9: No-click shooting (hold left-click), and no ammo used for 10 seconds, cooldown 10 seconds
- Prestige 10: Win

# Requirements
I am using the [Python 3.7](https://www.python.org/downloads/release/python-370/) IDLE.\
Python 3.x and Pygame 1.7.x or above is required.\
You can download pygame either [here](https://www.pygame.org/download.shtml), [here](https://bitbucket.org/pygame/pygame/downloads/) or [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame).
