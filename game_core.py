import itertools
import random
import typing

from pygame.math import Vector2

Vector2Hash = typing.Tuple[float, float]


def hash_vector2(vector: Vector2):
    return (vector.x, vector.y)


def get_grid_places_for_terminals(terminals):
    return [(pos + direction, -direction) for pos, direction in terminals]


def get_segments_for_grid_places(grid_places, usable_moves):
    """For each position, it will use the usable moves list,
    to get the segment, input direction and position"""
    segments = [
        (usable_moves[hash_vector2(pos)], input_dir, pos)
        for pos, input_dir in grid_places
        if hash_vector2(pos) in usable_moves
    ]
    return segments


def filter_used_moves(segments, usable_moves):
    [usable_moves.pop(hash_vector2(pos)) for seg, direction, pos in segments]


def get_new_terminal_groups(segments):
    groups = [
        segment.get_terminals(input_dir, pos) for segment, input_dir, pos in segments
    ]
    groups = [group for group in groups if group]
    return groups


class Directions:
    # Directions - offsets on grid system
    top = up = Vector2(0, -1)
    right = Vector2(1, 0)
    bottom = down = Vector2(0, 1)
    left = Vector2(-1, 0)


class SegmentBase:
    orig_terminals: typing.List[typing.Tuple[Vector2Hash, int]] = []

    def get_terminals(self, input_direction, pos: Vector2):
        if input_direction not in self.terminals:
            return None
        terminals = [
            (hash_vector2(pos), n) for n in self.terminals if n != input_direction
        ]
        return terminals

    def get_connections_for_direction(self, input_direction):
        """Return the valid connections for the current connection"""
        if input_direction not in self.terminals:
            return None
        directions = [n for n in self.terminals if n != input_direction]
        self.used_terminals = directions
        return directions

    def reset(self):
        self.used_terminals = None

    def __init__(self, rotation=0):
        """Rotation is in terms of multiples of 90"""
        self.used_terminals = None
        self.rotation = rotation
        self.terminals = [terminal.rotate(rotation) for terminal in self.orig_terminals]


class StraightSegment(SegmentBase):
    orig_terminals = [Directions.left, Directions.right]


class CornerSegment(SegmentBase):
    orig_terminals = [Directions.left, Directions.top]


class SimpleLevel:
    __slots__ = ["available_segments", "input", "output"]


class GameCore:
    """Core game play system"""

    grid_count = 6
    segments = [StraightSegment, CornerSegment]

    class SimpleLevel:
        def __init__(self, supply_position, output_position):
            """Positions - a tuple - ((-1,0), right) -
            meaning it is at that coord, supplying to the right."""
            self._supply_position = supply_position
            self._output_position = output_position

        def checkWin(self, moves):
            """Check the set of moves to see if there is a win condition"""
            if len(moves) < GameCore.grid_count:
                return False
            terminals = [self._supply_position]
            usable_moves = dict(moves)
            while terminals:
                grid_places = get_grid_places_for_terminals(terminals)
                if self._output_position in grid_places:
                    return True
                segments = get_segments_for_grid_places(grid_places, usable_moves)
                filter_used_moves(segments, usable_moves)
                new_terminal_groups = get_new_terminal_groups(segments)
                terminals = list(itertools.chain(*new_terminal_groups))
            return False

    level1 = SimpleLevel(
        (Vector2(-1, 0), Directions.right), (Vector2(6, 0), Directions.left)
    )

    def __init__(self):
        self._moves = {}
        self._nextSegment = StraightSegment()

    def playMove(self, coords: Vector2):
        self._moves[hash_vector2(coords)] = self._nextSegment
        self._newSegment()

    def _newSegment(self):
        """Choose a new segment"""
        self._nextSegment = random.choice(self.segments)(random.choice(range(0, 4)))

    def hasWon(self):
        return self.level1.checkWin(self._moves)

    def getMove(self, coords: Vector2):
        return self._moves[hash_vector2(coords)]

    def allMoves(self):
        return [(coords, segment) for coords, segment in self._moves.items()]

    def nextSegment(self):
        return self._nextSegment
