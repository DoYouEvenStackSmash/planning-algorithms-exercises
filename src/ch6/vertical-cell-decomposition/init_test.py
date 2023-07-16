#!/usr/bin/python3
import sys
sys.path.append(".")
from env_init import *
v = Vertex((0,0))
he = HalfEdge(v)
bv = BoundaryVertex(v)
print(bv.get_adjacent_edge_segments())