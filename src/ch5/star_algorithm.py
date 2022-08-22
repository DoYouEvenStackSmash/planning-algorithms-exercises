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

def build_star(A, O):
  star_list = []
  ha = A.get_front_edge()
  ho = O.get_front_edge()
  load_edge_normal_vectors(ha, star_list, True)
  load_edge_normal_vectors(ho, star_list, False)
  sort_edge_normal_vectors(star_list)

  
  


  

