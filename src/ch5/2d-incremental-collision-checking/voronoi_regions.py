#!/usr/bin/python3

from support.unit_norms import *
from support.Polygon import *
from support.Line import *
from support.Point import *
from support.World import *
from support.star_algorithm import *
from support.doubly_connected_edge_list import *
from pygame_rendering.pygame_loop_support import *
from pygame_rendering.render_support import *
from feature_markers import *
from region_tests import *
from file_loader import *

def find_contact(star_list, screen):
  i1 = 0
  i2 = 0
  adj_counter = 0

  while star_list[i1][1]._bounded_face == star_list[i2][1]._bounded_face and i2 < len(star_list):
    i2+=1
  adj_counter = i2

  T_OOB_HYPOTENUSE = -3
  T_OOB_NORM = -1
  T_OOB_EDGE = -2
  T_IN_VOR_EDGE = 1
  while i1 < len(star_list):
    V = star_list[i2][1].source_vertex
    E = star_list[i1][1]
    val = t_in_vor_edge(E, V.get_point_coordinate())#, screen)
    if val == T_IN_VOR_EDGE:
      print("EV found")
      EV_found(E, V, screen)
    if val == T_OOB_NORM:
      if t_in_V_region(E.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E.source_vertex.get_point_coordinate()):
        print("VV found")
        VV_found(E.source_vertex, V, screen)
    if val == T_OOB_HYPOTENUSE:
      E2 = E._next
      if t_in_V_region(E2.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E2.source_vertex.get_point_coordinate()):
        print("VV found")
        VV_found(E2.source_vertex, V, screen)
    e_hold = star_list[i1][1]._next
    while i1 < len(star_list) and star_list[i1][1] != e_hold:
      i1+=1
    if i1 == len(star_list):
      i1 = 0
      while star_list[i1][1] != e_hold:
        i1 += 1
      print("wrap!")
      break
    
    if i1 > i2:
      temp = i1
      i1 = i2
      i2 = temp
  temp = i1
  i1 = i2
  i2 = temp
  # i3 = 0
  while i1 < len(star_list):
    V = star_list[i2][1].source_vertex
    E = star_list[i1][1]
    val = t_in_vor_edge(E, V.get_point_coordinate())#, screen)
    if val == T_IN_VOR_EDGE:
      print("EV found")
      EV_found(E, V, screen)
    if val == T_OOB_NORM:
      if t_in_V_region(E.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E.source_vertex.get_point_coordinate()):
        print("VV found")
        VV_found(E.source_vertex, V, screen)
    if val == T_OOB_HYPOTENUSE:
      E2 = E._next
      if t_in_V_region(E2.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E2.source_vertex.get_point_coordinate()):
        print("VV found")
        VV_found(E2.source_vertex, V, screen)
    e_hold = star_list[i1][1]._next
    while i1 < len(star_list) and star_list[i1][1] != e_hold:
      i1+=1
    if i1 == len(star_list):
      break
  
    
