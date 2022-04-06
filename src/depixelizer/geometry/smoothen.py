import random
from math import sin, cos, pi
from .point import Point


class SplineSmoother(
    object
):  # This class contains the functionality for optimization of the B-splines
    # Some constants to guide the optimization
    INTERVALS_PER_SPAN = 20
    POINT_GUESSES = 20
    GUESS_OFFSET = 0.05
    ITERATIONS = 20
    POSITIONAL_ENERGY_MULTIPLIER = 1

    def __init__(self, spline):
        # Initialization function and stores the spline to be optimized
        self.orig = spline
        self.spline = spline.copy()

    def E_C(self, index):
        # Energy due to curvature (formula directly used from paper)
        return self.spline.Energy_C(index, self.INTERVALS_PER_SPAN)

    def E_P(self, index):
        # Energy due to change in position (formula directly used from paper)
        orig = self.orig.points[index]
        point = self.spline.points[index]
        e_positional = abs(point - orig) ** 4
        return e_positional * self.POSITIONAL_ENERGY_MULTIPLIER

    def point_energy(self, index):
        # Total energy of a point = energy_curvature + energy_positional
        E1 = self.E_C(index)
        E2 = self.E_P(index)
        return E1 + E2

    def rand(self):
        # A random offset generator
        offset = random.random() * self.GUESS_OFFSET
        angle = random.random() * 2 * pi
        return offset * Point((cos(angle), sin(angle)))

    def smooth_point(self, index, start):
        # The function which is used to optimize the position of a point
        energies = [(self.point_energy(index), start)]
        for _ in range(
            self.POINT_GUESSES
        ):  # Around 20 guesses are made and the minimum energy one is chosen
            point = start + self.rand()
            self.spline.Move(index, point)
            energies.append((self.point_energy(index), point))
        self.spline.Move(index, min(energies)[1])  # Move the spline appropriately

    def smooth(self):
        # The function to smooth the spline
        for _it in range(self.ITERATIONS):
            for i, point in enumerate(self.spline.useful_points):
                self.smooth_point(i, point)


def smooth_spline(spline):
    # External function which creates an instance of the optimizer class
    smoother = SplineSmoother(spline)
    smoother.smooth()
    return smoother.spline
