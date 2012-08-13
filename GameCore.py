import itertools
import random
from Point import Point

__author__ = 'stapled'

def getGridPlacesForTerminals(terminals):
    return [(pos + direction, -direction) for pos, direction in terminals]


def getSegmentsForGridPlaces(grid_places, usable_moves):
    """For each position, it will use the usable moves list,
    to get the segment, input direction and position"""
    segments = [(usable_moves[pos], input_dir, pos)
        for pos, input_dir in grid_places if usable_moves.has_key(pos)]
    return segments


class Directions(object):
    #Directions - offsets on grid system
    top = up = Point(0, -1)
    right = Point(1, 0)
    bottom = down = Point(0, 1)
    left = Point(-1, 0)


def filterUsedMoves(segments, usable_moves):
    [usable_moves.pop(pos) for seg, direction, pos in segments]


def getNewTerminalGroups(segments):
    groups = [segment.getTerminals(input_dir, pos)
                           for segment, input_dir, pos in segments]
    groups = [group for group in groups if group]
    return groups


class GameCore(object):
    """Core game play system"""

    grid_cells = 6

    class SegmentBase(object):
        def getTerminals(self, input_direction, pos):
            if input_direction not in self.terminals:
                return None
            terminals = [(pos, n) for n in self.terminals if n != input_direction]
            return terminals

        def __init__(self, rotation = 0):
            """Rotation is in terms of multiples of 90"""
            self.rotation = rotation
            self.terminals = [terminal.rotate(rotation) for terminal in self.orig_terminals]

    class StraightSegment(SegmentBase):
        orig_terminals = [Directions.left, Directions.right]

    class CornerSegment(SegmentBase):
        orig_terminals = [Directions.left, Directions.top]

    segments = [StraightSegment, CornerSegment]

    class SimpleLevel(object):
        def __init__(self, supply_position, output_position):
            """Positions - a tuple - ((-1,0), right) -
            meaning it is at that coord, supplying to the right."""
            self._supply_position = supply_position
            self._output_position = output_position

        def checkWin(self, moves):
            """Check the set of moves to see if there is a win condition"""
            if len(moves) < GameCore.grid_cells:
                return False
            terminals = [self._supply_position]
            usable_moves = dict(moves)
            while terminals:
                grid_places = getGridPlacesForTerminals(terminals)
                if self._output_position in grid_places:
                    return True
                segments = getSegmentsForGridPlaces(grid_places, usable_moves)
                filterUsedMoves(segments, usable_moves)
                new_terminal_groups = getNewTerminalGroups(segments)
                terminals = list(itertools.chain(*new_terminal_groups))
            return False

    level1 = SimpleLevel( (Point(-1, 0), Directions.right), (Point(6, 0), Directions.left))

    def __init__(self):
        self._moves = {}
        self._nextSegment = self.StraightSegment()

    def playMove(self, coords):
        self._moves[Point(coords)] = self._nextSegment
        self._newSegment()

    def _newSegment(self):
        """Choose a new segment"""
        self._nextSegment = random.choice(self.segments)(random.choice(range(0,4)))

    def hasWon(self):
        return self.level1.checkWin(self._moves)

    def getMove(self, coords):
        return self._moves[Point(coords)]

    def allMoves(self):
        return [(coords, segment) for coords, segment in self._moves.items()]

    def nextSegment(self):
        return self._nextSegment