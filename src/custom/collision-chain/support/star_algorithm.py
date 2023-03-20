#!/usr/bin/python3

from support.doubly_connected_edge_list import *
# from Polygon import *
# from World import *
from support.unit_norms import *
# from primitive_support import *


'''
  Minkowski
'''

def load_edge_normal_vectors(head, star_list, switch = False):
  '''
  Calculates normal vectors for each half edge in the doubly linked list
  Places normal vectors in a preexisting list
  Does not return
  '''
  he_curr = head
  
  p1 = he_curr.source_vertex.get_point_coordinate()
  p2 = he_curr._next.source_vertex.get_point_coordinate()
  
  rad_angle = get_unit_norm_angle(p1,p2,switch)
  
  star_list.append((rad_angle, he_curr))
  he_curr = he_curr._next
  while he_curr != head:
    p1 = he_curr.source_vertex.get_point_coordinate()
    p2 = he_curr._next.source_vertex.get_point_coordinate()
  
    rad_angle = get_unit_norm_angle(p1,p2,switch)
  
    star_list.append((rad_angle, he_curr))
    he_curr = he_curr._next

def conv_func(theta):
  '''
  Conversion function for negative radians
  Returns converted angle
  '''
  if theta < 0:
    return 2 * np.pi + theta
  return theta

def edge_normal_tuple_key(edge_tuple):
  '''
  Helper function for sorting
  Returns a converted angle in radians
  '''
  return conv_func(edge_tuple[0])

def sort_edge_normal_vectors(star_list):
  '''
  Sorts a list of half edge objects by the angle of their normal vectors
  Returns a sorted list of edge objects
  '''
  angle_sort_key = lambda edge_normal_tuple: edge_normal_tuple_key(edge_normal_tuple)
  star_list = sorted(star_list,key=angle_sort_key)
  return star_list

def build_star(ha, ho):
  '''
  Builds the "star" from the half edges of robot A and obstacle O
  Returns sorted list of edges
  '''
  star_list = []
  load_edge_normal_vectors(ha, star_list, True)
  load_edge_normal_vectors(ho, star_list, False)
  star_list = sort_edge_normal_vectors(star_list)
  return star_list

def distance_between_points(a, b):
  '''
  Calculates Euclidean distance between two points
  Returns scalar distance
  '''
  x1,y1 = a
  x2,y2 = b
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  return dist

def derive_obstacle_space_points(star_list):
  '''
  Calculates obstacle region boundary
  Returns a list of points which represent the minkowski sum
  '''
  origin_pts = []
  ox,oy = star_list[0][1]._next.source_vertex.get_point_coordinate()
  origin_pts.append((ox,oy))
  for i in range(1,len(star_list)):
    p1 = star_list[i][1].source_vertex.get_point_coordinate()
    p2 = star_list[i][1]._next.source_vertex.get_point_coordinate()

    r = distance_between_points(p1,p2)

    theta = star_list[i][0] + np.pi / 2
    if theta > np.pi:
      theta = -2 * np.pi + theta
    x = r * np.cos(theta) + ox
    y = r * np.sin(theta) + oy
    origin_pts.append((x,y))
    ox,oy = origin_pts[-1]
  return origin_pts

def get_star_segments(star_list, origin):
  '''
  Constructs a "star" of segments which extend from some origin point from the sorted
  list of half edges.
  Returns a list of line segments
  '''
  segments = []
  r = 60
  ox,oy = origin
  for edge_tuple in star_list:
    segments.append(((ox,oy),(r * np.cos(edge_tuple[0]) + ox, r * np.sin(edge_tuple[0]) + oy)))
  return segments



  

