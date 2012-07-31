"""Simple game - you have a power supply, ground and a load.
You need to connect the right terminals of the load to the power and ground
for it to work.
But - you only get different sections of cable to work with.
You place the cable sections onto the square grid, you can rotate them.
One a cable section is placed - it stays there!
You can dispose of a section without placing it, but you must take the next.
"""
import pygame
import itertools
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

def addCoords(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by

class Point(object):
    def __init__(self, x, y = None):
        if y is not None:
            self._x = x
            self._y = y
        else:
            self._x, self._y = x

    def __add__(self, other):
        return Point(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        return Point(self._x - other._x, self._y - other._y)

    def __neg__(self):
        return Point(- self._x, -self._y)

    def __cmp__(self, other):
        return self._x == other._x and self._y == other._y

    def __mul__(self, other):
        """Other must be numeric"""
        return Point(self._x * other, self._y * other)

    def __div__(self, other):
        """Other must be numeric"""
        return Point(self._x / other, self._y / other)

    def __hash__(self):
        return hash((self._x, self._y))

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __getitem__(self, item):
        if item is 0:
            return self._x
        if item == 1:
            return self._y

    def __iter__(self):
        yield self._x
        yield self._y

    def __repr__(self):
        return "Point%s" % (str(self),)

    def __str__(self):
        return "(%s, %s)" % (str(self._x), str(self._y))

class GameCore(object):
    """Core game play system"""

    #Directions - offsets on grid system
    top = Point(0, -1)
    right = Point(1, 0)
    bottom = Point(0, 1)
    left = Point(-1, 0)

    grid_cells = 5

    class StraightSegment(object):
        @classmethod
        def getTerminals(self, input_direction, pos):
            return [(pos, -input_direction)]

    class SimpleLevel(object):
        def __init__(self, supply_position, output_position):
            """Positions - a tuple - ((-1,0), right) -
            meaning it is at that coord, supplying to the right."""
            self._supply_position = supply_position
            self._output_position = output_position

        def checkWin(self, moves):
            """Check the set of moves to see if there is a win condition"""
            terminals = [self._supply_position]
            usable_moves = dict(moves)
            while terminals:
                print "Terminals", repr(terminals)
                grid_places = [(pos + direction, -direction) for pos, direction in terminals]
                print "Grid places", repr(grid_places)
                if self._output_position in grid_places:
                    return True
                print "Usable moves #1", repr(usable_moves)


                segments = [(usable_moves[pos], input_dir, pos)
                    for pos, input_dir in grid_places if usable_moves.has_key(pos)]
                print "Segments", repr(segments)
                [usable_moves.pop(pos) for seg, direction, pos in segments]
                print "Usable moves #2", repr(usable_moves)
                new_terminal_groups = [segment[0].getTerminals(input_dir, pos)
                                       for segment, input_dir, pos in segments]
                print "terminal groups", repr(new_terminal_groups)
                sleep(1)
                terminals = list(itertools.chain(*new_terminal_groups))
                sleep(1)
            return False

    level1 = SimpleLevel( (Point(-1, 0), right), (Point(4, 0), left))

    def __init__(self):
        self._moves = {}

    def playMove(self, coords, segment, rotation):
        self._moves[Point(coords)] = (segment, rotation)

    def hasWon(self):
        return self.level1.checkWin(self._moves)

    def getMove(self, coords):
        return self._moves[Point(coords)]

    def allMoves(self):
        return [(coords, item[0], item[1]) for coords, item in self._moves.items()]

    def nextSegment(self):
        return GameCore.StraightSegment



class MainGameUI(SceneBase):
    electric_blue = (192, 192, 255)
    black = (0, 0, 0)
    grey = (0x88, 0x88, 0x88)

    bg_colour = electric_blue

    top_coord = 50

    game_rect_colour = black
    game_rect = pygame.Rect(170, top_coord, 300, 300)

    segments = {GameCore.StraightSegment: pygame.image.load("StraightLine.png")}

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

    def _renderMoves(self):
        for coords, move, rotation in self._core.allMoves():
            segment = self.segments[move]
            coords = self.fromCoreGrid(coords)
            self._screen.blit(segment, pygame.Rect(coords, (self.grid_size, self.grid_size)))

    def _render(self):
        self._screen.fill(self.bg_colour)
        self._rect(self.game_rect_colour, self.game_rect)
        self._rect(self.next_item_colour, self.next_item_rect)

        self._draw_grid()

        self._screen.blit(self.segments[self._core.nextSegment()], self.next_item_rect)

        self._renderMoves()
        pygame.display.flip()

    def toCoreGrid(self, pos):
        """Given a position, convert to game core grid coords"""
        return (Point(pos) - Point(self.game_rect.topleft)) / self.grid_size

    def fromCoreGrid(self, pos):
        """Given a core grid coord, convert to ui position"""
        return (Point(pos) + Point(self.game_rect.topleft)) * self.grid_size

    def _playMove(self, pos):
        if self.game_rect.collidepoint(pos):
            print "Played in rect at point %s" % (str(pos),)
            pos = self.toCoreGrid(pos)
            print "Core grid is point %s" % (str(pos),)
            self._core.playMove(pos, self._core.nextSegment(), 0)
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
