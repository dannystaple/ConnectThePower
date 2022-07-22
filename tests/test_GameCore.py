from unittest import TestCase
from pygame.math import Vector2

from game_core import (
    GameCore,
    Directions,
    get_grid_places_for_terminals,
    StraightSegment,
    CornerSegment,
    get_segments_for_grid_places,
    filter_used_moves,
    get_new_terminal_groups,
    hash_vector2,
)


class TestGameCore(TestCase):
    """Test the basic stuff in the game core"""

    def helper_playMove(self, gc: GameCore, coord: Vector2, segment):
        """This helper will override the stuff in the game core,
        but is not the normal use case - so stays in a test helper"""
        gc._nextSegment = segment
        gc.playMove(coord)

    def test_notWonWhenOnlyOneStraightSegmentPlayed(self):
        gc = GameCore()
        self.helper_playMove(gc, hash_vector2(Vector2(0, 0)), StraightSegment(0))
        game_won = gc.hasWon()
        self.assertEquals(False, game_won)

    def test_notWonWithFewerThanGridCells(self):
        """If we have 6 grid cells, then 5 moves should not win the level"""
        gc = GameCore()
        toPlay = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        toPlay = [Vector2(c) for c in toPlay]
        [self.helper_playMove(gc, c, StraightSegment(0)) for c in toPlay]
        game_won = gc.hasWon()
        self.assertFalse(game_won)

    def test_wonWithStraightLine(self):
        """If we play a straight row across the top - we should win"""
        gc = GameCore()
        toPlay = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
        toPlay = [Vector2(c) for c in toPlay]
        [self.helper_playMove(gc, c, StraightSegment(0)) for c in toPlay]
        game_won = gc.hasWon()
        self.assertTrue(game_won)


class TestDirections(TestCase):
    def test_leftNotEqualToRight(self):
        self.assertTrue(Directions.left != Directions.right)
        self.assertEqual(
            Directions.left != Directions.right, not Directions.left == Directions.right
        )


class TestGetGridForTerminals(TestCase):
    def test_itShouldGetTheNextPositionForEachInputTerminal(self):
        start_terminals = [(Vector2(0, 0), Directions.right)]
        end_grid = get_grid_places_for_terminals(start_terminals)
        self.assertEqual(end_grid, [(Vector2(1, 0), Directions.left)])

    def test_SegmentsForGridSegments(self):
        sg = StraightSegment()
        usable_moves = {hash_vector2(Vector2(1, 0)): sg}
        grid_places = [(Vector2(1, 0), Directions.left)]
        expected = [(sg, Directions.left, Vector2(1, 0))]
        self.assertEqual(
            expected, get_segments_for_grid_places(grid_places, usable_moves)
        )

    def test_filterUsedMoves(self):
        sg1 = StraightSegment()
        sg2 = CornerSegment()
        usable_moves = {
            hash_vector2(Vector2(1, 0)): sg1,
            hash_vector2(Vector2(2, 0)): sg2,
        }
        filter_used_moves([(sg1, Directions.left, Vector2(1, 0))], usable_moves)
        self.assertFalse(hash_vector2(Vector2(1, 0)) in usable_moves)

    def test_getNewTerminalGroups(self):
        sg = StraightSegment()
        segments = [(sg, Directions.left, Vector2(2, 0))]
        expected_terminals = [[(Vector2(2, 0), Directions.right)]]
        output = get_new_terminal_groups(segments)
        self.assertEqual(expected_terminals, output)


class Test_straightSegment(TestCase):
    def test_straightSegmentWithoutRotationShouldBeRightToLeft(self):
        sg = StraightSegment()
        self.assertEqual(sg.terminals, [Directions.left, Directions.right])

    def test_straightSegmentShouldGetOppositeTerminalForPassedInTerminal(self):
        sg = StraightSegment()
        input_dir = Directions.left
        output = [terminal for terminal in sg.terminals if (terminal != input_dir)]
        expected = [Directions.right]
        self.assertEqual(expected, output)
