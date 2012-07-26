"""Simple game - you have a power supply, ground and a load.
You need to connect the right terminals of the load to the power and ground
for it to work.
But - you only get different sections of cable to work with.
You place the cable sections onto the square grid, you can rotate them.
One a cable section is placed - it stays there!
You can dispose of a section without placing it, but you must take the next.
"""
import pygame
from time import sleep

__author__ = 'danny'

class SceneBase(object):
    def __init__(self, screen):
        self._screen = screen

class Splash(object):
    """Picture of crazy electrician. Clicks/presses fade to menu"""
    pass

class MainGame(SceneBase):
    def enter(self):
        """Enter the game screen"""
        sleep(10)

class MainMenu(object):
    """Game, settings, exit"""
    pass

class Settings(object):
    """Sound/music on off. Fullscreen/not is window controls"""
    pass

def init():
    screen = pygame.display.set_mode((640, 400))
    return screen
  
def main():
    screen = init()
    spInstance = Splash()
    game = MainGame(screen)
    menu = MainMenu()
    settings = Settings()
    game.enter()    
    
if __name__ == "__main__":
    main()
