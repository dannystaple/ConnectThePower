import unittest
from ConnectThePower import GameCore, Point

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

class TestGameCore(unittest.TestCase):
    """Test the basic stuff in the game core"""

    def test_gameCoreNotWonWhenOnlyOneStraightSegmentPlayed(self):
        gc = GameCore()
        gc.playMove(Point(0,0), gc.StraightSegment, 0)
        game_won = gc.hasWon()
        self.assertEquals(False, game_won)