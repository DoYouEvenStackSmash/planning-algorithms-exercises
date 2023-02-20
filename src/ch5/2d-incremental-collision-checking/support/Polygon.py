#!/usr/bin/python3
from support.doubly_connected_edge_list import *

class Polygon:
  '''
  2D Polygon object, made up by an ordered list of points
  Internally represented as a doubly connected edge list
  '''
  def __init__(self, point_list = []):
    '''
    Initialize polygon object from a set of points
    '''
    self._id = None
    self.data_structure = DoublyConnectedEdgeList()
    self.init_face(point_list)
    self.color = None
    self.v_color = None
    self.e_color = None

  def init_face(self, point_list):
    '''
    Initialize a polygon using an ordered list of points
    Returns the id of the created polygon face
    '''
    if len(point_list) < 3:
      print(f"cannot make a face with fewer than 3 points!")
      return -1
    
    # make sure points are in counterclockwise order
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
    '''
    Accessor for all points in the underlying doubly connected edge list
    Returns a list of (x,y) points
    '''
    if self._id == None:
      print(f"WARN: no points to dump!")
      return []

    point_list = self.data_structure.get_face_points(self._id)
    return point_list

  
  def dump_segments(self):
    '''
    Accessor for pairs of points representing valid segments
    Returns a list of point pairs [((x1,y1), (x2,y2))]
    '''
    if self._id == None:
      print(f"WARN: no segments to dump!")
      return []
    point_list = self.data_structure.get_face_points(self._id)
    
    segment_list = []
    for i in range(1,len(point_list)):
      segment_list.append((point_list[i - 1], point_list[i]))
    
    segment_list.append((point_list[-1], point_list[0]))
    return segment_list


  def get_front_edge(self):
    '''
    Accessor for a representative edge of the polygon from the underlying
    doubly connected edge list.
    Returns a Half Edge
    '''
    if self._id == None:
      print(f"No front edge!")
      return None
    return self.data_structure.get_face_half_edge(self._id)


