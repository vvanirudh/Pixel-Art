from .bspline import Curve2Closed_BSpline
from .smoothen import smooth_spline

# Returns the slope of the line connecting two points
def slope(p0, p1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    if dx == 0:
        return (
            dy * 99999999999999
        )  # Since dx is zero, we avoid division by zero. Instead, we multiply dy by a large number
    return 1.0 * dy / dx


class Path(object):
    # The path class encodes all the splines that are fit to a shape
    def __init__(self, shape_graph):
        self.path = self.make_path(shape_graph)
        self.shapes = set()

    def key(self):
        # This is the key used in the dict stored in the pixel graph
        return tuple(self.path)

    def make_path(self, shape_graph):
        # Creates the path and returns it
        nodes = set(shape_graph.nodes())
        path = [min(nodes)]
        neighbors = sorted(
            shape_graph.neighbors(path[0]), key=lambda p: slope(path[0], p)
        )
        path.append(neighbors[0])
        nodes.difference_update(
            path
        )  # This is equivalent to set difference between nodes and path

        # Go through the rest of the nodes and add nodes appropriately to the path
        p = path[-1]
        i = 0
        while nodes:
            for neighbor in shape_graph.neighbors(path[-1]):
                if neighbor in nodes:
                    nodes.remove(neighbor)
                    path.append(neighbor)
                    break
            if p != path[-1]:
                p = path[-1]
                i = 0
            else:
                i += 1
                if i == 3:
                    break
        return path

    def make_spline(self):
        # Fit a spline to the path
        self.spline = Curve2Closed_BSpline(self.path)

    def smooth_spline(self):
        # Optimise the spline that is already fit to the path
        self.smooth = smooth_spline(self.spline)
