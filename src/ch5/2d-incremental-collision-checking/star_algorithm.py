#!/usr/bin/python3

from doubly_connected_edge_list import *
from polygon import *
from world import *
from norms import *
from primitive_support import *


'''
  Minkowski
'''

def load_edge_normal_vectors(head, star_list, switch = False):
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
  if theta < 0:
    return 2 * np.pi + theta
  return theta

def edge_normal_tuple_key(edge_tuple):
  return conv_func(edge_tuple[0])

def sort_edge_normal_vectors(star_list):
  angle_sort_key = lambda edge_normal_tuple: edge_normal_tuple_key(edge_normal_tuple)
  star_list = sorted(star_list,key=angle_sort_key)
  return star_list

def build_star(A, O):
  star_list = []
  ha = A.get_front_edge()
  ho = O.get_front_edge()
  load_edge_normal_vectors(ha, star_list, True)
  load_edge_normal_vectors(ho, star_list, False)
  star_list = sort_edge_normal_vectors(star_list)
  return star_list

def distance_between_points(a, b):
  x1,y1 = a
  x2,y2 = b
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  return dist

def derive_obstacle_space_points(star_list):
  origin_pts = []
  # ox,oy = star_list[0][1].source_vertex.get_point_coordinate()
  # origin_pts.append((ox,oy))
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
  segments = []
  r = 60
  ox,oy = origin
  for edge_tuple in star_list:
    segments.append(((ox,oy),(r * np.cos(edge_tuple[0]) + ox, r * np.sin(edge_tuple[0]) + oy)))
  return segments



  

