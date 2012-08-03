import unittest
import mock
from ConnectThePower import GameCore, Point, MainGameUI

class TestPoint(unittest.TestCase):
    """Test the point class"""
    def test_hashOfPointsAreTheSame(self):
        """Given two points of 0,0 - they should have same hash"""
        a = Point(0,0)
        b = Point(1 - 1, -1 + 1)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_dictMadeWithPointsHasKey(self):
        """If I put a point in a dict, then use a point with same coords,
        does this show up as a key?"""
        a = Point(0,0)
        b = Point(1 - 1, -1 + 1)
        d = {a: 23}
        self.assertTrue(d.has_key(b))

    def test_rotatePointDegrees(self):
        a = Point(1, 0)
        b = a.rotate(90)
        self.assertEqual(b, Point(0, 1))

class TestGameCore(unittest.TestCase):
    """Test the basic stuff in the game core"""

    def helper_playMove(self, gc, coord, segment):
        """This helper will override the stuff in the game core,
        but is not the normal use case - so stays in a test helper"""
        gc._nextSegment = segment
        gc.playMove(coord)

    def test_gameCoreNotWonWhenOnlyOneStraightSegmentPlayed(self):
        gc = GameCore()
        self.helper_playMove(gc, Point(0,0), gc.StraightSegment(0))
        game_won = gc.hasWon()
        self.assertEquals(False, game_won)

    def test_gameCoreNotWonWithFewerThanGridCells(self):
        """If we have 6 grid cells, then 5 moves should not win the level"""
        gc = GameCore()
        toPlay = [(0,0), (1,0), (2,0), (3,0), (4, 0)]
        toPlay = [Point(c) for c in toPlay]
        [self.helper_playMove(gc, c, gc.StraightSegment(0)) for c in toPlay]
        game_won = gc.hasWon()
        self.assertFalse(game_won)

class TestGameUI(unittest.TestCase):
    """Test Game UI features"""

    def test_testGridCoordsShouldMapToScreenCoords(self):
        """
        Given a set of grid coordinates, it should be able to map them
        to sensible screen coordinates.
        """
        grid_coord = Point(0, 0)
        expected_coords = Point(MainGameUI.grid_left, MainGameUI.grid_top)
        fakeDisplay = mock.Mock()
        ui = MainGameUI(fakeDisplay)
        self.assertEqual(expected_coords, ui.fromCoreGrid(grid_coord))