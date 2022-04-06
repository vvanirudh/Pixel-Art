# Returns the tuple containing the vertices of the edge in sorted order
def get_sorted_vertices(edge):
    return tuple(sorted(edge[:2]))


# This function checks whether the given coordinates lie inside the image. If it is outside the dimensions of the image, then we return false.
def check_bounds(coordinate, size, offset=(0, 0)):
    x, y = map(
        sum, zip(coordinate, offset)
    )  # Add the coordinates of the given coordinate to the offset
    width, height = size
    return (
        0 <= x < width and 0 <= y < height
    )  # If the coordinates lie outside the dimensions of the image then return false


class Heuristics(object):
    sparse_window = (
        8,
        8,
    )  # The window around the edge which we examine for sparse heuristic

    def __init__(
        self, pixel_graph
    ):  # The pixel data of the image is loaded into the heuristic
        self.pixel_graph = pixel_graph

    def sparse_offset(
        self, edge
    ):  # This returns the boundaries of the window that must be examined in the sparse heuristic
        return (
            self.sparse_window[0] / 2 - 1 - min((edge[0][0], edge[1][0])),
            self.sparse_window[1] / 2 - 1 - min((edge[0][1], edge[1][1])),
        )

    def apply_heuristics(self, ambiguous_diagonal_pairs):
        # This function takes a list of ambiguous diagonal pairs and applies heuristics on them to resolve the diagonal
        # to remove and the diagonal to keep
        for edges in ambiguous_diagonal_pairs:
            self.weight_diagonals(
                *edges
            )  # Evaluate the heuristic value on each diagonal

        for edges in ambiguous_diagonal_pairs:
            min_weight = min(e[2]["weight"] for e in edges)
            for edge in edges:
                if edge[2]["weight"] == min_weight:
                    self.pixel_graph.remove_edge(
                        *edge[:2]
                    )  # Remove the edge which has minimum weight among the pair
                else:
                    edge[2].pop(
                        "weight"
                    )  # If it is not the diagonal removed, then the attribute weight is removed

    def weight_diagonals(self, edge1, edge2):
        # This function returns the weight for the pair of diagonals
        for edge in (edge1, edge2):
            self.weight_diagonal(edge)

    def weight_diagonal(self, edge):
        # This function returns the weight of the diagonal
        weights = [
            self.weight_curve(edge),
            self.weight_sparse(edge),
            self.weight_island(edge),
        ]
        edge[2]["weight"] = sum(weights)

    # This heuristic differs from the one in the paper slightly,
    # in the way that the paper suggests us to vote the longer edge with a weight equal to
    # difference in the lengths of the curves
    def weight_curve(self, edge):
        # This function returns the weight of the edge wrt the CURVE heuristic
        edges_in_the_curve = set([get_sorted_vertices(edge)])
        nodes_in_the_curve = list(edge[:2])

        while nodes_in_the_curve:
            node = nodes_in_the_curve.pop()
            edges = self.pixel_graph.edges(node, data=True)

            if (
                len(edges) != 2
            ):  # If the node is not a valence-2 node then it can't be part of a curve
                continue

            for edge in edges:
                edge = get_sorted_vertices(edge)
                if edge not in edges_in_the_curve:  # If edge not already seen
                    edges_in_the_curve.add(edge)  # Add the edge to the list
                    nodes_in_the_curve.extend(
                        n for n in edge if n != node
                    )  # Add the new nodes to the seen nodes
        return len(edges_in_the_curve)  # Return the length of the curve as the weight

    def weight_sparse(self, edge):
        # This function returns the weight of the edge wrt SPARSE heuristic
        nodes = list(edge[:2])
        nodes_in_the_sparse_window = set(nodes)
        offset = self.sparse_offset(edge)

        while nodes:
            node = nodes.pop()
            for n in self.pixel_graph.neighbors(node):
                if n in nodes_in_the_sparse_window:
                    continue
                if check_bounds(n, self.sparse_window, offset=offset):
                    nodes_in_the_sparse_window.add(n)
                    nodes.append(n)

        return -len(
            nodes_in_the_sparse_window
        )  # Returns the negative of the nodes found

    def weight_island(self, edge):
        # This function returns the weight of the edge wrt ISLAND heuristic
        # If any of teh two endpoints of the edge are valence-1 then removing the edge might
        # create an island
        if len(self.pixel_graph[edge[0]]) == 1 or len(self.pixel_graph[edge[1]]) == 1:
            return 5
        return 0
