"""Simple game - you have a power supply, ground and a load.
You need to connect the right terminals of the load to the power and ground
for it to work.
But - you only get different sections of cable to work with.
You place the cable sections onto the square grid, you can rotate them.
One a cable section is placed - it stays there!
You can dispose of a section without placing it, but you must take the next.
"""
import pygame

__author__ = 'danny'

class Splash(object):
    """Picture of crazy electrician. Clicks/presses fade to menu"""
    pass

class MainGame(object):
    pass

class MainMenu(object):
    """Game, settings, exit"""
    pass

class Settings(object):
    """Sound/music on off. Fullscreen/not is window controls"""
    pass

def main():
    spInstance = Splash()
    game = MainGame()
    menu = MainMenu()
    settings = Settings()

    pass

if __name__ == "__main__":
    main()
