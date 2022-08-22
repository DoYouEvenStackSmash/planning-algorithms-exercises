#!/usr/bin/python3
from doubly_connected_edge_list import *

class Polygon:
  def __init__(self, point_list = []):
    self._id = None
    self.data_structure = DoublyConnectedEdgeList()
    self.init_face(point_list)

  def init_face(self, point_list):
    if len(point_list) < 3:
      print(f"cannot make a face with fewer than 3 points!")
      return -1
    p1_x, p1_y = point_list[0]
    p2_x, p2_y = point_list[1]
    p3_x, p3_y = point_list[2]
    
    if ((p2_x - p1_x) * (p3_y - p1_y)) - ((p2_y - p1_y) * (p3_x - p1_x)) < 0:
      point_list = [i for i in reversed(point_list)]

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
    point_list = [pt.get_point_coordinate() for pt in v]
    return point_list


