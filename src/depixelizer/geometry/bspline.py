from math import sqrt
from .point import Point


class BSpline(object):
    # Class for B-Spline Curve
    def __init__(self, KnotVector, points, degree=None):
        # The initialization function which takes Knotvector, Control Points and degree(can be excluded) of the B-Spline
        self.KnotVector = tuple(KnotVector)
        self._points = [Point(p) for p in points]
        # Expected degree, if not specified in the constructor
        expected_degree = len(self.KnotVector) - len(self._points) - 1
        if degree is None:
            degree = expected_degree
        if degree != expected_degree:
            raise ValueError(
                "Degree expected is %s, got %s instead as Input."
                % (expected_degree, degree)
            )
        self.degree = degree
        self.remove_stored()

    def remove_stored(self):
        #   This removes the stored derivative value of the curve.
        self.storedvalue = {}

    def Move(self, i, value):
        #   This function moves a specific control point to a new location
        self._points[i] = value
        self.remove_stored()

    def __str__(self):
        return "<%s degree=%s, points=%s, KnotVector=%s>" % (
            type(self).__name__,
            self.degree,
            len(self.points),
            len(self.KnotVector),
        )

    def copy(self):
        #   Copy Constructor
        return type(self)(self.KnotVector, self.points, self.degree)

    # Few properties to ease syntax
    @property
    def domain(self):
        return (
            self.KnotVector[self.degree],
            self.KnotVector[len(self.KnotVector) - self.degree - 1],
        )

    @property
    def points(self):
        return tuple(self._points)

    @property
    def useful_points(self):
        return self.points

    # Overloading the call function of this class
    def __call__(self, u):
        # This function implements the DeBoor's algorithm
        s = len([uk for uk in self.KnotVector if uk == u])
        for k, uk in enumerate(self.KnotVector):
            if uk >= u:
                break
        if s == 0:
            k -= 1
        if self.degree == 0:
            if k == len(self.points):
                k -= 1
            return self.points[k]
        ps = [
            dict(
                zip(
                    range(k - self.degree, k - s + 1),
                    self.points[k - self.degree : k - s + 1],
                )
            )
        ]

        for r in range(1, self.degree - s + 1):
            ps.append({})
            for i in range(k - self.degree + r, k - s + 1):
                a = (u - self.KnotVector[i]) / (
                    self.KnotVector[i + self.degree - r + 1] - self.KnotVector[i]
                )
                ps[r][i] = (1 - a) * ps[r - 1][i - 1] + a * ps[r - 1][i]
        return ps[-1][k - s]

    def Quadratic_Bezier_Fit(self):
        # 	Finding a series of quadratic Beziers making up this spline.
        assert self.degree == 2
        control_points = self.points[1:-1]
        on_curve_points = [self(u) for u in self.KnotVector[2:-2]]
        ocp0 = on_curve_points[0]
        for cp, ocp1 in zip(control_points, on_curve_points[1:]):
            # Yield the starting point of the curve, control point and end point
            yield (ocp0.tuple, cp.tuple, ocp1.tuple)
            ocp0 = ocp1

    def Derivative(self):
        #   Returns the derivative of the curve, more Math!
        cached = self.storedvalue.get("1")
        if cached:
            return cached

        new_points = []
        p = self.degree
        for i in range(0, len(self.points) - 1):
            coeff = p / (self.KnotVector[i + 1 + p] - self.KnotVector[i + 1])
            new_points.append(coeff * (self.points[i + 1] - self.points[i]))

        cached = BSpline(self.KnotVector[1:-1], new_points, p - 1)
        self.storedvalue["1"] = cached
        return cached

    def Clamp(self, value):
        return max(self.domain[0], min(self.domain[1], value))

    def Span(self, index):
        return (
            self.Clamp(self.KnotVector[index]),
            self.Clamp(self.KnotVector[index + 1]),
        )

    def Points_In_Span(self, index):
        return [self.Span(index + i) for i in range(self.degree)]

    def Integrate_part(self, func, span, intervals):
        #   Integrates the given function on the Interval and returns value
        if span[0] == span[1]:
            return 0

        interval = (span[1] - span[0]) / intervals
        result = (func(span[0]) + func(span[1])) / 2
        for i in range(1, intervals):
            result += func(span[0] + i * interval)
        result *= interval

        return result

    def Integrate(self, index, func, intervals):
        # Integrates the function in intervals
        spans_ = self.Points_In_Span(index)
        spans = [span for span in spans_ if span[0] != span[1]]
        return sum(self.Integrate_part(func, span, intervals) for span in spans)

    def Curvature(self, u):
        #   Returns the curvature of the spline at a point
        d1 = self.Derivative()(u)
        d2 = self.Derivative().Derivative()(u)
        numerator = d1.x * d2.y - d1.y * d2.x
        denominator = sqrt(d1.x**2 + d1.y**2) ** 3
        if denominator == 0:
            return 0
        return abs(numerator / denominator)

    def Energy_C(self, index, intervals_per_span):
        #   Energy due to curvature at a point
        return self.Integrate(index, self.Curvature, intervals_per_span)

    def reversed(self):
        return type(self)(
            (1 - k for k in reversed(self.KnotVector)),
            reversed(self._points),
            self.degree,
        )


class Closed_BSpline(BSpline):
    # Class for representing closed b-pline curves where the start and edn point coincide
    def __init__(self, KnotVector, points, degree=None):
        super(Closed_BSpline, self).__init__(KnotVector, points, degree)
        self._unwrapped_len = len(self._points) - self.degree
        self.Wrap_check()

    def Wrap_check(self):
        # Checks the closed-ness of the spline
        if self._points[: self.degree] != self._points[-self.degree :]:
            raise ValueError("Points not wrapped at degree %s." % (self.degree,))

    def Move(self, index, value):
        # Moves the spline according to the change in position of a control point
        if not 0 <= index < len(self._points):
            raise IndexError(index)
        index = index % self._unwrapped_len
        super(Closed_BSpline, self).Move(index, value)
        if index < self.degree:
            super(Closed_BSpline, self).Move(index + self._unwrapped_len, value)

    @property
    def useful_points(self):
        return self.points[: -self.degree]

    def Span(self, index):
        def span(i):
            return (self.KnotVector[i], self.KnotVector[i + 1])

        d0, d1 = span(index)
        if d0 < self.domain[0]:
            d0, d1 = span(index + len(self.points) - self.degree)
        elif d1 > self.domain[1]:
            d0, d1 = span(index + self.degree - len(self.points))
        return self.Clamp(d0), self.Clamp(d1)


def Curve2Closed_BSpline(path, degree=2):
    # Returns the closed b-pline that is fit to the path given
    points = path + path[:degree]
    m = len(points) + degree
    KnotVector = [float(i) / m for i in range(m + 1)]

    return Closed_BSpline(KnotVector, points, degree)


def magnitude(point):
    return sqrt(point[0] ** 2 + point[2] ** 2)
