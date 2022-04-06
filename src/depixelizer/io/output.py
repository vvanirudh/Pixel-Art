import os.path
from math import sqrt
from svgwrite import Drawing


def distance(p0, p1):
    return sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)


def color(rgb_value_tuple):
    return "rgb(%s,%s,%s)" % rgb_value_tuple


def get_writer(data, filename):
    return SVGWriter(data, filename)


class SVGWriter(object):
    PIXEL_SCALE = 40
    CURVE_COLOR = (255, 127, 0)

    def __init__(self, data, filename, scale=None, color=None):
        self.name = filename
        self.pixel_data = data
        if scale:
            self.PIXEL_SCALE = scale
        if color:
            self.CURVE_COLOR = color

    def scale_pt(self, pt, offset=(0, 0)):
        return tuple(int((n + o) * self.PIXEL_SCALE) for n, o in zip(pt, offset))

    def output_image(self):
        filename = self.name
        # filename = filename+".svg"
        filename = os.path.join("outputs", "%s.%s" % (filename, "svg"))
        drawing = self.make_drawing(filename)
        self.draw_shapes(drawing)
        # self.insert_color(drawing)
        self.save_drawing(drawing, filename)

    def make_drawing(self, filename):
        return Drawing(filename)

    def save_drawing(self, drawing, filename):
        drawing.save()

    def draw_shapes(self, drawing):
        for shape in self.pixel_data.shapes:
            paths = getattr(shape, "smooth_splines")
            self.draw_spline(drawing, paths, shape.value)

    def draw_spline(self, drawing, splines, fill):
        if fill == (255, 255, 255):
            return
        path = []
        # points = []
        for spline in splines:
            curves = list(spline.Quadratic_Bezier_Fit())
            path.append("M")
            path.append(self.scale_pt(curves[0][0]))
            for curve in curves:
                path.append("Q")
                path.append(self.scale_pt(curve[1]))
                path.append(self.scale_pt(curve[2]))
                p0 = self.scale_pt(curve[0])
                p1 = self.scale_pt(curve[2])
            path.append("Z")
        drawing.add(drawing.path(path, stroke=color(fill), fill=color(fill)))
