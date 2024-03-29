"""Simple game - you have a power supply, ground and a load.
You need to connect the right terminals of the load to the power and ground
for it to work.
But - you only get different sections of cable to work with.
You place the cable sections onto the square grid, you can rotate them.
One a cable section is placed - it stays there!
You can dispose of a section without placing it, but you must take the next.
"""
import pygame
from pygame.math import Vector2
from game_core import GameCore, CornerSegment, StraightSegment

# List of tiles. Each is dictionary of asset filename, connections: [active grid list - 9 binary numbers for which allow current to pass].
tiles = (
    {"asset": "assets/straight.png", "connections": [0, 0, 0, 1, 1, 1, 0, 0, 0]},
    {"asset": "assets/left.png", "connections": [0, 0, 0, 1, 1, 0, 0, 1, 0]},
    {"asset": "assets/right.png", "connections": [0, 0, 0, 0, 1, 1, 0, 1, 0]},
    {"asset": "assets/cross.png", "connections": [0, 1, 0, 1, 1, 1, 0, 1, 0]},
    {"asset": "assets/tjunction.png", "connections": [0, 1, 0, 1, 1, 1, 0, 0, 0]},
)


class Colours:
    electric_blue = (192, 192, 255)
    black = (0, 0, 0)
    grey = (0x88, 0x88, 0x88)
    red = (0xFF, 0x00, 0x00)


class SceneBase:
    def __init__(self, screen):
        self._screen = screen

    def _rect(self, colour, rect: pygame.Rect):
        pygame.draw.rect(self._screen, colour, rect)

    def _line(self, colour, start, end):
        pygame.draw.line(self._screen, colour, start, end)


class Splash(object):
    """Picture of crazy electrician. Clicks/presses fade to menu"""

    pass


class MainGameUI(SceneBase):
    bg_colour = Colours.electric_blue

    top_coord = 50

    game_rect_colour = Colours.grey
    game_rect = pygame.Rect(170, top_coord, 300, 300)

    next_item_rect = (35, top_coord, 100, 100)
    next_item_colour = Colours.black

    grid_size = 50
    grid_colour = Colours.black
    grid_left = game_rect.left
    grid_right = game_rect.right
    grid_top = game_rect.top
    grid_bottom = game_rect.bottom
    grid_cols = tuple([col for col in range(grid_left, grid_right, grid_size)])
    grid_rows = tuple([row for row in range(grid_top, grid_bottom, grid_size)])

    power_terminal_colour = Colours.red

    def enter(self):
        """Enter the game screen"""
        self.segments = {
            StraightSegment: pygame.image.load("assets/StraightLine.png"),
            CornerSegment: pygame.image.load("assets/RightAngle.png"),
        }

        self._core = GameCore()

        self._playing = True

        while self._playing:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self._playing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self._play_move(pos)
            self._render()

    def _draw_grid(self):
        [
            self._line(self.grid_colour, (self.grid_left, row), (self.grid_right, row))
            for row in self.grid_rows
        ]
        [
            self._line(self.grid_colour, (col, self.grid_top), (col, self.grid_bottom))
            for col in self.grid_cols
        ]
        self._rect(
            self.power_terminal_colour,
            pygame.Rect(
                self.from_core_grid(self._core.current_level.supply_position[0]),
                (self.grid_size, self.grid_size),
            ),
        )
        self._rect(
            self.power_terminal_colour,
            pygame.Rect(
                self.from_core_grid(self._core.current_level.output_position[0]),
                (self.grid_size, self.grid_size),
            ),
        )

    def _render_segment(self, segment, rect):
        seg_image = self.segments[type(segment)]
        rotation = segment.rotation * 90
        rotsegment = pygame.transform.rotate(seg_image, rotation)
        self._screen.blit(rotsegment, rect)

    def _render_moves(self):
        for coords, move in self._core.allMoves():
            coords = self.from_core_grid(coords)
            rect = pygame.Rect(tuple(coords), (self.grid_size, self.grid_size))
            self._render_segment(move, rect)

    def _render(self):
        self._screen.fill(self.bg_colour)
        self._rect(self.game_rect_colour, self.game_rect)
        self._rect(self.next_item_colour, self.next_item_rect)

        self._draw_grid()

        self._render_segment(self._core.nextSegment(), self.next_item_rect)

        self._render_moves()
        pygame.display.flip()

    def to_core_grid(self, pos):
        """Given a position, convert to game core grid coords"""
        return (Vector2(pos) - Vector2(self.game_rect.topleft)) // self.grid_size

    def from_core_grid(self, pos):
        """Given a core grid coord, convert to ui position"""
        return (Vector2(pos) * self.grid_size) + Vector2(self.game_rect.topleft)

    def _play_move(self, pos):
        if self.game_rect.collidepoint(pos):
            print("Played in rect at point %s" % (str(pos),))
            pos = self.to_core_grid(pos)
            print("Core grid is point %s" % (str(pos),))
            self._core.playMove(pos)
        if self._core.hasWon():
            print("I think you won!")


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
