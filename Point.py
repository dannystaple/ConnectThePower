__author__ = 'stapled'

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
