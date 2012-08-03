import math

__author__ = 'stapled'

class Point(object):
    __slots__=['x', 'y']

    def __init__(self, x, y = None):
        if y is not None:
            self.x = x
            self.y = y
        else:
            self.x, self.y = x

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(- self.x, -self.y)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y

    def __mul__(self, other):
        """Other must be numeric"""
        return Point(self.x * other, self.y * other)

    def __div__(self, other):
        """Other must be numeric"""
        return Point(self.x / other, self.y / other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, item):
        if item is 0:
            return self.x
        if item == 1:
            return self.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return "Point%s" % (str(self),)

    def __str__(self):
        return "(%s, %s)" % (str(self.x), str(self.y))

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = round(self.x*cos - self.y*sin, 2)
        y = round(self.x*sin + self.y*cos, 2)
        return Point(x, y)