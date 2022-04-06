class Point(object):
    # A class to efficiently represent points. Value is stored as an imaginary number as it is easier in the caluculation relevant
    # to B-splines.
    def __init__(self, value):
        if isinstance(value, complex):
            self.value = value
        elif isinstance(value, (tuple, list)):
            self.value = value[0] + value[1] * 1j
        elif isinstance(value, Point):
            self.value = value.value
        else:
            pass

    # Some properties of the point
    @property
    def x(self):
        return self.value.real

    @property
    def y(self):
        return self.value.imag

    @property
    def tuple(self):
        return (self.x, self.y)

    def _op(self, op, other):
        if isinstance(other, Point):
            other = other.value
        return Point(getattr(self.value, op)(other))

    def __eq__(self, other):
        try:
            other = Point(other).value
        except ValueError:
            pass
        return self.value.__eq__(other)

    # Basic operators overloaded
    def __add__(self, other):
        return self._op("__add__", other)

    def __radd__(self, other):
        return self._op("__radd__", other)

    def __sub__(self, other):
        return self._op("__sub__", other)

    def __rsub__(self, other):
        return self._op("__rsub__", other)

    def __mul__(self, other):
        return self._op("__mul__", other)

    def __rmul__(self, other):
        return self._op("__rmul__", other)

    def __div__(self, other):
        return self._op("__div__", other)

    def __rdiv__(self, other):
        return self._op("__rdiv__", other)

    def __abs__(self):
        return abs(self.value)

    def round(self, places=5):
        return Point((round(self.x, places), round(self.y, places)))
