class Shape(object):
    def __init__(self, pixels, value, corners):
        # This function initializes the Shape instance with pixel data, color and corners
        self.pixels = pixels
        self.value = value
        self.corners = corners
        self._outside_path = None  # The splines describing the boundary of the shape
        self._inside_paths = []  # The splines describing the inside of the shape

    # def _paths_attr(self, attr):
    # 	 paths = [list(reversed(getattr(self._outside_path, attr)))]
    # 	 paths.extend(getattr(path, attr) for path in self._inside_paths)

    # We define the following functions as property as we dont pass them any parameters and these are used in many
    # places. So, calling shape.paths is easier than shape.paths()
    @property
    def paths(self):
        # This function  returns the paths in the shape
        paths = [list(reversed(self._outside_path.path))]
        paths.extend(path.path for path in self._inside_paths)
        return paths

    @property
    def splines(self):
        # This function returns the splines in the shape
        paths = [self._outside_path.spline.reversed()]
        paths.extend(path.spline for path in self._inside_paths)
        return paths

    @property
    def smooth_splines(self):
        # This function returns the optimised splines in the shape
        paths = [self._outside_path.smooth.reversed()]
        paths.extend(path.smooth for path in self._inside_paths)
        return paths

    def add_outline(self, path, outside=False):
        # This function adds a boundary to the shape / an inside edge can also be added
        if outside:
            self._outside_path = path
        else:
            self._inside_paths.append(path)
        path.shapes.add(self)
