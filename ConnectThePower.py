"""Simple game - you have a power supply, ground and a load.
You need to connect the right terminals of the load to the power and ground
for it to work.
But - you only get different sections of cable to work with.
You place the cable sections onto the square grid, you can rotate them.
One a cable section is placed - it stays there!
You can dispose of a section without placing it, but you must take the next.
"""
import pygame
from GameCore import  GameCore
from Point import Point

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

class MainGameUI(SceneBase):
    electric_blue = (192, 192, 255)
    black = (0, 0, 0)
    grey = (0x88, 0x88, 0x88)

    bg_colour = electric_blue

    top_coord = 50

    game_rect_colour = black
    game_rect = pygame.Rect(170, top_coord, 300, 300)

    next_item_rect = (35, top_coord, 100, 100)
    next_item_colour = black

    grid_size = 50
    grid_colour = grey
    grid_left = game_rect.left
    grid_right = game_rect.right
    grid_top = game_rect.top
    grid_bottom = game_rect.bottom
    grid_cols = tuple([col for col in range(grid_left, grid_right, grid_size)])
    grid_rows = tuple([row for row in range(grid_top, grid_bottom, grid_size)])

    def enter(self):
        """Enter the game screen"""
        self.segments = {GameCore.StraightSegment: pygame.image.load("StraightLine.png"),
                         GameCore.CornerSegment: pygame.image.load("RightAngle.png")}

        self._core = GameCore()

        self._playing = True

        while self._playing:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self._playing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self._playMove(pos)
            self._render()

    def _draw_grid(self):
        [self._line(self.grid_colour, (self.grid_left, row), (self.grid_right, row))
         for row in self.grid_rows]
        [self._line(self.grid_colour, (col, self.grid_top), (col, self.grid_bottom))
         for col in self.grid_cols]

    def _renderSegment(self, segment, rect):
        seg_image = self.segments[type(segment)]
        rotation = segment.rotation * 90
        rotsegment = pygame.transform.rotate(seg_image, rotation)
        self._screen.blit(rotsegment, rect)

    def _renderMoves(self):
        for coords, move in self._core.allMoves():
            coords = self.fromCoreGrid(coords)
            rect = pygame.Rect(tuple(coords), (self.grid_size, self.grid_size))
            self._renderSegment(move, rect)

    def _render(self):
        self._screen.fill(self.bg_colour)
        self._rect(self.game_rect_colour, self.game_rect)
        self._rect(self.next_item_colour, self.next_item_rect)

        self._draw_grid()

        self._renderSegment(self._core.nextSegment(), self.next_item_rect)

        self._renderMoves()
        pygame.display.flip()

    def toCoreGrid(self, pos):
        """Given a position, convert to game core grid coords"""
        return (Point(pos) - Point(self.game_rect.topleft)) / self.grid_size

    def fromCoreGrid(self, pos):
        """Given a core grid coord, convert to ui position"""
        return (Point(pos) * self.grid_size) + Point(self.game_rect.topleft)

    def _playMove(self, pos):
        if self.game_rect.collidepoint(pos):
            print "Played in rect at point %s" % (str(pos),)
            pos = self.toCoreGrid(pos)
            print "Core grid is point %s" % (str(pos),)
            self._core.playMove(pos)
        if self._core.hasWon():
            print "I think you won!"

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
    game = MainGameUI(screen)
    menu = MainMenu()
    settings = Settings()
    game.enter()    
    
if __name__ == "__main__":
    main()
