import networkx
from math import sqrt

from .heuristic import Heuristics, check_bounds
from depixelizer.geometry import Shape, Path

# This generates all the coordinates from 0 to width and 0 to height i.e. it creates a walk over all pixels
def coordinates(size):
    # We use range as we don't want all the numbers from 0 to width in memory
    for y in range(size[1]):
        for x in range(size[0]):
            # We use yield because this number might be too large to store in memory. We are better off, generating it as we need them
            yield (x, y)


# Returns distance between two points
def distance(p0, p1):
    return sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)


# Removes the given elements from a collection of elements as a set
def remove(set_given, element):
    set_given.add(element)  # Add the element in case it isn't there
    # Remove both/the only copy of element in the set
    set_given.remove(element)


class PixelData(object):
    # The heuristics attribute of the pixeldata class
    HEURISTICS = Heuristics

    # Initialize with the pixel data
    def __init__(self, pixels):
        self.pixels = pixels
        self.width = len(pixels[0])
        self.height = len(pixels)
        self.size = (self.width, self.height)

    # The main function which contains all the procedures required for depixelizing the image
    def depixelize(self):

        self.create_pixel_graph()
        print("graph done")
        self.remove_diagonals()
        print("removed diagonals")
        self.create_grid_graph()
        print("grid graph done")
        self.deform_grid()
        print("deformed graph done")
        self.create_shapes()
        print("made shapes")
        self.get_boundaries()
        print("Obtained boundaries")
        self.add_shape_boundaries()
        print("shaped boundaries")
        self.smooth_splines()
        print("smoothed splines")

    def pixel(self, x, y):
        # The pixel data is loaded in the [y][x] format and not the [x][y]. Careful, while coding.
        return self.pixels[y][x]

    def create_grid_graph(self):
        # This function creates the grid graph of size (w+1)x(h+1) as described in the paper
        self.grid_graph = networkx.grid_2d_graph(self.width + 1, self.height + 1)

    def create_pixel_graph(self):
        # This function creates the pixel graph
        self.pixel_graph = networkx.Graph()
        # Add all the nodes and edges between them
        for x, y in coordinates(self.size):
            # Set the corners and connect the edges
            corners = set([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)])
            self.pixel_graph.add_node((x, y), value=self.pixel(x, y), corners=corners)
            self.add_pixel_edge((x, y), (x + 1, y))
            self.add_pixel_edge((x, y), (x, y + 1))
            self.add_pixel_edge((x, y), (x + 1, y - 1))
            self.add_pixel_edge((x, y), (x + 1, y + 1))

    def add_pixel_edge(self, pix0, pix1):
        # Adds a pixel edge in the graph iff it connects two similar colored pixels
        if check_bounds(pix1, self.size) and self.equal(pix0, pix1):
            attrs = {"diagonal": pix0[0] != pix1[0] and pix0[1] != pix1[1]}
            # Set the attributes appropriately
            self.pixel_graph.add_edge(pix0, pix1, **attrs)

    def equal(self, pix0, pix1):
        # Returns true if the color value in both pixels is same. Need to change this to have YUV channels.
        color0 = self.pixel(*pix0)
        color1 = self.pixel(*pix1)

        y0 = 0.299 * color0[0] + 0.587 * color0[1] + 0.114 * color0[2]
        u0 = 0.492 * (color0[2] - y0)
        v0 = 0.877 * (color0[0] - y0)

        y1 = 0.299 * color1[0] + 0.587 * color1[1] + 0.114 * color1[2]
        u1 = 0.492 * (color1[2] - y1)
        v1 = 0.877 * (color1[0] - y1)

        ydiff = abs(y0 - y1)
        udiff = abs(u0 - u1)
        vdiff = abs(v0 - v1)

        if ydiff > 48 or udiff > 7 or vdiff > 6:
            return False
        else:
            return True

        # return self.pixel(*pix0) == self.pixel(*pix1)

    def equal1(self, pix0, pix1):
        return self.pixel(*pix0) == self.pixel(*pix1)

    def remove_diagonals(self):
        # This function removes the diagonals from the graph
        ambiguous_diagonal_pairs = []

        for nodes in self.enumerate_blocks(2):
            edges = [
                e
                for e in self.pixel_graph.edges(nodes, data=True)
                if e[0] in nodes and e[1] in nodes
            ]  # Get all the edges which contain these nodes

            # Extract only the diagonals
            diagonals = [e for e in edges if e[2]["diagonal"]]
            if len(diagonals) == 2:
                if len(edges) == 6:
                    # We have a fully-connected block, so remove all diagonals.
                    for edge in diagonals:
                        self.pixel_graph.remove_edge(edge[0], edge[1])
                elif len(edges) == 2:
                    # We have an ambiguous pair to resolve.
                    ambiguous_diagonal_pairs.append(edges)
                else:
                    assert False, "Unexpected diagonal format"

        self.apply_diagonal_heuristics(ambiguous_diagonal_pairs)

    def apply_diagonal_heuristics(self, ambiguous_diagonal_pairs):
        self.HEURISTICS(self.pixel_graph).apply_heuristics(ambiguous_diagonal_pairs)

    def enumerate_blocks(self, size):
        # This function enumerates all the size x size blocks in a lazy manner
        for x, y in coordinates((self.width - size + 1, self.height - size + 1)):
            yield [(x + dx, y + dy) for dx in range(size) for dy in range(size)]

    def deform_grid(self):
        # This function deforms the grid as per the algorithm
        for node in self.pixel_graph.nodes():
            # Iterate through all the nodes in the graph and deform each of them
            self.deform_cell(node)

        # Collapse all valence-2 nodes to get a more smoother image
        removals = []
        for node in self.grid_graph.nodes():
            if node in ((0, 0), (0, self.size[1]), (self.size[0], 0), self.size):
                # Skip corner nodes of teh image as they shouldn't be collapsed, obviously!
                continue
            neighbors = list(self.grid_graph.neighbors(node))
            if (
                len(neighbors) == 2
            ):  # Connect the neighbors of the valence-2 node by an edge
                self.grid_graph.add_edge(*neighbors)
            if len(neighbors) <= 2:
                removals.append(node)

        # Remove all the valence-2 nodes
        for node in removals:
            self.grid_graph.remove_node(node)

        # Update pixel corner sets.
        for node, attrs in self.pixel_graph.nodes(data=True):
            corners = attrs["corners"]
            for corner in corners.copy():
                if corner not in self.grid_graph:
                    corners.remove(corner)

    def deform_cell(self, node):
        # This function deforms each cell as per the algorithm in the paper
        for neighbor in self.pixel_graph.neighbors(node):
            if node[0] == neighbor[0] or node[1] == neighbor[1]:
                # We only consider diagonals
                continue
            px_x = max(neighbor[0], node[0])
            px_y = max(neighbor[1], node[1])
            pixnode = (px_x, px_y)
            offset_x = neighbor[0] - node[0]
            offset_y = neighbor[1] - node[1]
            adj_node = (neighbor[0], node[1])
            if not self.equal1(node, adj_node):
                pn = (px_x, px_y - offset_y)
                mpn = (px_x, px_y - 0.5 * offset_y)
                npn = (px_x + 0.25 * offset_x, px_y - 0.25 * offset_y)
                remove(self.pixel_corners(adj_node), pixnode)
                self.pixel_corners(adj_node).add(npn)
                self.pixel_corners(node).add(npn)
                self.deform(pixnode, pn, mpn, npn)
            adj_node = (node[0], neighbor[1])
            if not self.equal1(node, adj_node):
                pn = (px_x - offset_x, px_y)
                mpn = (px_x - 0.5 * offset_x, px_y)
                npn = (px_x - 0.25 * offset_x, px_y + 0.25 * offset_y)
                remove(self.pixel_corners(adj_node), pixnode)
                self.pixel_corners(adj_node).add(npn)
                self.pixel_corners(node).add(npn)
                self.deform(pixnode, pn, mpn, npn)

    def pixel_corners(self, pixel):
        # This function returns the corners corresponding to the cell representing the given pixel
        return self.pixel_graph.nodes[pixel]["corners"]

    def deform(self, pixnode, pn, mpn, npn):
        # This function deforms the edge and connects other points which are offsetted by a constant from the
        # original position
        if mpn in self.grid_graph:
            self.grid_graph.remove_edge(mpn, pixnode)
        else:
            self.grid_graph.remove_edge(pn, pixnode)
            self.grid_graph.add_edge(pn, mpn)
        self.grid_graph.add_edge(mpn, npn)
        self.grid_graph.add_edge(npn, pixnode)

    def create_shapes(self):
        self.shapes = set()
        # Identify shapes in the graph by identifying the connected component subgraphs
        for pcg in (
            self.pixel_graph.subgraph(c).copy()
            for c in networkx.connected_components(self.pixel_graph)
        ):
            pixels = set()
            value = None
            corners = set()
            for pixel, attrs in pcg.nodes(data=True):
                pixels.add(pixel)
                corners.update(attrs["corners"])
                value = attrs["value"]
            self.shapes.add(Shape(pixels, value, corners))
            # Create a separate shape for each connected component subgraph and store all the pixels of the subgraph
            # in it

    def get_boundaries(self):
        # Remove internal edges from a copy of our pixgrid graph and just get the boundaries
        self.outlines_graph = networkx.Graph(self.grid_graph)
        for pixel, attrs in self.pixel_graph.nodes(data=True):
            corners = attrs["corners"]
            for neighbor in self.pixel_graph.neighbors(pixel):
                edge = corners & self.pixel_graph.nodes[neighbor]["corners"]
                if len(edge) != 2:  # If the number of edges is not 2
                    print(edge)
                # Remove the internal edges in the outlines graph
                elif self.outlines_graph.has_edge(*edge):
                    self.outlines_graph.remove_edge(*edge)
        for node in list(networkx.isolates(self.outlines_graph)):
            # Remove the nodes from the outline graph too
            self.outlines_graph.remove_node(node)

    def make_path(self, graph):
        # This function will create a path for a given subgraph
        path = Path(graph)
        key = path.key()
        if key not in self.paths:
            self.paths[key] = path
            path.make_spline()  # and also fit a spline to the path
        return self.paths[key]

    def add_shape_boundaries(self):
        self.paths = {}
        # Add the obtained boundaries to the corresponding shapes
        for shape in self.shapes:
            sg = self.outlines_graph.subgraph(shape.corners)
            for graph in (
                sg.subgraph(c).copy() for c in networkx.connected_components(sg)
            ):
                path = self.make_path(graph)
                if min(graph.nodes()) == min(sg.nodes()):
                    shape.add_outline(path, True)
                else:
                    shape.add_outline(path)

    def smooth_splines(self):
        # This function iterates through all the paths and tries to smooth each of them.
        print("Smoothing splines...")
        for i, path in enumerate(self.paths.values()):
            print(
                " * %s/%s (%s, %s)..."
                % (i + 1, len(self.paths), len(path.shapes), len(path.path))
            )
            if len(path.shapes) == 1:
                path.smooth = path.spline.copy()
                continue
            path.smooth_spline()  # Smooth each path which was previosuly fit with a spline
