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

    def _rect(self, colour, rect):
        pygame.draw.rect(self._screen, colour, rect)

    def _line(self, colour, start, end):
        pygame.draw.line(self._screen, colour, start, end)

class Splash(object):
    """Picture of crazy electrician. Clicks/presses fade to menu"""
    pass

class MainGame(SceneBase):
    electric_blue = (192, 192, 255)
    black = (0, 0, 0)
    grey = (0x88, 0x88, 0x88)

    bg_colour = electric_blue

    top_coord = 50

    game_rect_colour = black
    game_rect_height = 300
    game_rect_width = 300
    game_rect_left = 170
    game_rect = (game_rect_left, top_coord, game_rect_width, game_rect_height)

    straight_line = pygame.image.load("StraightLine.png")

    next_item_rect = (35, top_coord, 100, 100)
    next_item_colour = black

    grid_size = 50
    grid_colour = grey
    grid_left = game_rect_left
    grid_right = game_rect_left + game_rect_width
    grid_top = top_coord
    grid_bottom = top_coord + game_rect_height



    def enter(self):
        """Enter the game screen"""
        self._playing = True

        while self._playing:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self._playing = False
            self._render()

    def _draw_grid(self):
        [self._line(self.grid_colour, (self.grid_left, row + self.top_coord), (self.grid_right, row + self.top_coord))
         for row in range(0, self.game_rect_height, self.grid_size)]
        [self._line(self.grid_colour, (self.grid_left + col, self.grid_top), (self.grid_left + col, self.grid_bottom))
         for col in range(0, self.game_rect_width, self.grid_size)]

    def _render(self):
        self._screen.fill(self.bg_colour)
        self._rect(self.game_rect_colour, self.game_rect)
        self._rect(self.next_item_colour, self.next_item_rect)

        self._draw_grid()

        self._screen.blit(self.straight_line, self.next_item_rect)

        pygame.display.flip()


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
