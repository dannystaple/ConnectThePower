import unittest
from GameCore import GameCore, Directions, getGridPlacesForTerminals, StraightSegment, CornerSegment, getSegmentsForGridPlaces
from Point import Point

__author__ = 'stapled'

class TestGameCore(unittest.TestCase):
    """Test the basic stuff in the game core"""

    def helper_playMove(self, gc, coord, segment):
        """This helper will override the stuff in the game core,
        but is not the normal use case - so stays in a test helper"""
        gc._nextSegment = segment
        gc.playMove(coord)

    def test_notWonWhenOnlyOneStraightSegmentPlayed(self):
        gc = GameCore()
        self.helper_playMove(gc, Point(0,0), StraightSegment(0))
        game_won = gc.hasWon()
        self.assertEquals(False, game_won)

    def test_notWonWithFewerThanGridCells(self):
        """If we have 6 grid cells, then 5 moves should not win the level"""
        gc = GameCore()
        toPlay = [(0,0), (1,0), (2,0), (3,0), (4, 0)]
        toPlay = [Point(c) for c in toPlay]
        [self.helper_playMove(gc, c, StraightSegment(0)) for c in toPlay]
        game_won = gc.hasWon()
        self.assertFalse(game_won)

    def test_wonWithStraightLine(self):
        """If we play a straight row across the top - we should win"""
        gc = GameCore()
        toPlay  = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
        toPlay = [Point(c) for c in toPlay]
        [self.helper_playMove(gc, c, gc.StraightSegment(0)) for c in toPlay]
        game_won = gc.hasWon()
        self.assertTrue(game_won)


class TestDirections(unittest.TestCase):
    def test_leftNotEqualToRight(self):
        self.assertTrue(Directions.left != Directions.right)
        self.assertEqual(Directions.left != Directions.right, not Directions.left == Directions.right)


class TestGetGridForTerminals(unittest.TestCase):
    def test_itShouldGetTheNextPositionForEachInputTerminal(self):
        start_terminals = [(Point(0,0), Directions.right)]
        end_grid = getGridPlacesForTerminals(start_terminals)
        self.assertEqual(end_grid, [(Point(1,0), Directions.left)])

    def test_SegmentsForGridSegments(self):
        sg = GameCore.StraightSegment()
        usable_moves = {Point(1,0): sg}
        grid_places = [(Point(1,0), Directions.left)]
        expected = [(sg, Directions.left, Point(1,0))]
        self.assertEqual(expected, getSegmentsForGridPlaces(grid_places, usable_moves))

    def test_filterUsedMoves(self):
        sg1 = GameCore.StraightSegment()
        sg2 = GameCore.CornerSegment()
        usable_moves = {Point(1,0): sg1, Point(2,0): sg2}
        filterUsedMoves([(sg1,Directions.left, Point(1,0))], usable_moves)
        self.assertFalse(usable_moves.has_key(Point(1,0)))

    def test_getNewTerminalGroups(self):
        sg = GameCore.StraightSegment()
        segments = [(sg, Directions.left, Point(2,0))]
        expected_terminals = [[(Point(2,0), Directions.right)]]
        output = getNewTerminalGroups(segments)
        self.assertEqual(expected_terminals, output)


class Test_straightSegment(unittest.TestCase):
    def test_straightSegmentWithoutRotationShouldBeRightToLeft(self):
        sg = GameCore.StraightSegment()
        self.assertEqual(sg.terminals, [Directions.left, Directions.right])

    def test_straightSegmentShouldGetOppositeTerminalForPassedInTerminal(self):
        sg = GameCore.StraightSegment()
        input_dir = Directions.left
        output = [terminal for terminal in sg.terminals if (terminal != input_dir)]
        expected = [Directions.right]
        self.assertEqual(expected, output)