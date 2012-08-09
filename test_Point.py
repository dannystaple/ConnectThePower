import unittest

from Point import Point

class TestPoint(unittest.TestCase):
    """Test the point class"""
    def test_hashOfPointsAreTheSame(self):
        """Given two points of 0,0 - they should have same hash"""
        a = Point(0,0)
        b = Point(1 - 1, -1 + 1)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_PointAndPointWithDecimalsAreEqual(self):
        a = Point(1, 2)
        b = Point(1.0, 2.0)
        self.assertEqual(a, b)

    def test_twoDifferentPointsAreNotEqual(self):
        a = Point(0, 1)
        b = Point(2, 0)
        state = a != b
        self.assertTrue(state)
        self.assertNotEqual(a, b)

    def test_xy(self):
        a=  Point(22, 53)
        self.assertEqual(a.x, 22)
        self.assertEqual(a.y, 53)

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

    def test_pointNotEqualCanBeUsedInListComp(self):
        """Regression - problems were seen here.
        Try the points in a list, then with a filter based
        on != operator."""
        a = Point(0,0)
        b = Point(1,0)
        c = Point(2,1)
        d = Point(3,2)
        l = [a,b,c,d,a,c,a,b,c,a,d,c,b,a]
        out = [item for item in l if item != c]
        self.assertNotIn(c, out)
