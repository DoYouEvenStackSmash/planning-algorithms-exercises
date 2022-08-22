#!/usr/bin/python3
from doubly_connected_edge_list import *

class Polygon:
  def __init__(self, point_list = []):
    self._id = None
    self.data_structure = DoublyConnectedEdgeList()
    self.init_face(point_list)

  def init_face(self, point_list):
    _id = self.data_structure.create_new_face(point_list)
    if _id < 0:
      print(f"no face was created.")
      return -1
    self._id = _id
    return self._id
  
  def dump_points(self):
    if self._id == None:
      print(f"WARN: no points to dump!")
      return []
    v = self.data_structure.get_face_vertices(self._id)
    pts = [pt.get_point_coordinate() for pt in v]
    return pts


