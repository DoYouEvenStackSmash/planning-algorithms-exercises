#!/usr/bin/python3


class Vertex:
    """
    An abstraction for a point [x, y] in R2
    """

    def __init__(self, point=None, _half_edge=None):
        self.point = point if point != None else [0, 0]
        self._half_edge = _half_edge
        self.rank = -1

    def get_point_coordinate(self):
        """
        Accessor for components of a vertex
        """
        return self.point

    def get_half_edge(self):
        """
        Accessor for half edge for which this vertex is a source
        """
        return self._half_edge
