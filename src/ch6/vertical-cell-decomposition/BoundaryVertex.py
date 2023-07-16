# from doubly_connected_edge_list import *
from env_init import *

# from DCEL import *
from render_support import MathFxns as mfn


class BoundaryVertex:
    """
    Abstraction for an event as part of Vertical Cell Decomposition
    """

    def __init__(self, vertex, angles=None):
        self.vertex = vertex
        self.angles = angles if angles != None else []

    def get_vertical_vectors(self, radius=500):
        """
        Returns vectors of length radius at self.angles
        """
        src = self.vertex.get_point_coordinate()
        segments = []
        for a in self.angles:
            endpt = mfn.pol2car(src, radius, a)
            segments.append((src, endpt))
        return segments

    def get_adjacent_edge_segments(self):
        """
        Accessor for neighboring edges as line segments as pairs of points
        Returns a list of pairs of (x,y) points
        """
        prv = lambda v: v._half_edge._prev.get_source_vertex()
        nxt = lambda v: v._half_edge._next.get_source_vertex()
        edges = [
            (
                prv(self.vertex).get_point_coordinate(),
                self.vertex.get_point_coordinate(),
            ),
            (
                self.vertex.get_point_coordinate(),
                nxt(self.vertex).get_point_coordinate(),
            ),
        ]

        return edges

    def get_segment_if_rank(self, curr_rank):
        """
        Accessor for segments if rank interval contains curr_rank
        Returns a list of pairs of (x,y) points
        """

        he = self.vertex._half_edge
        prv = lambda v: v._half_edge._prev.get_source_vertex()
        nxt = lambda v: v._half_edge._next.get_source_vertex()
        edges = [(prv(self.vertex), self.vertex), (self.vertex, nxt(self.vertex))]
        maxrank = lambda vpair: max(vpair[0].rank, vpair[1].rank)
        minrank = lambda vpair: min(vpair[0].rank, vpair[1].rank)
        valid_edges = []
        for e in edges:
            if minrank(e) <= curr_rank and maxrank(e) >= curr_rank:
                valid_edges.append([v.get_point_coordinate() for v in e])
        return valid_edges
