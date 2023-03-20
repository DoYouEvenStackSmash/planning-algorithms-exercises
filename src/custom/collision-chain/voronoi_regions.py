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

DEBUG = False

def find_contact(SL, screen = None, VERBOSE = False):
  '''
  Algorithm for finding overlapping voronoi regions
  Returns a scalar distance between the closest pair of points
  '''
  i1,i2 = 0,0
  end_marker = 0
  while SL[i1][1]._bounded_face == SL[i2][1]._bounded_face and i2 < len(SL):
    i2+=1
  # this is the wrapper position when we terminate the first while loop
  end_marker = i2
  wrap = lambda x : x % len(SL)

  T_OOB_HYPOTENUSE = -3
  T_OOB_NORM = -1
  T_OOB_EDGE = -2
  T_IN_VOR_EDGE = 1
  END_FIRST_FLAG = False
  '''
    i is chasing j
  '''
  ev_records = []
  vv_records = []
  while 1:
    E = SL[wrap(i1)][1]
    V = SL[wrap(i2)][1].source_vertex
    val = t_in_vor_edge(E, V.get_point_coordinate())
    if val == T_IN_VOR_EDGE:
      if t_in_V_region(V, calc_line_point(E, V)):
        if DEBUG:
          print("EV found!")
        ev_records.append((E,V))
        return EV_found(E, V, screen, VERBOSE)
        
    if val == T_OOB_NORM: # candidate for VV, seeking symmetry
      if t_in_V_region(E.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E.source_vertex.get_point_coordinate()):
        if DEBUG:
          print("VV found")
        vv_records.append((E.source_vertex, V))
        return VV_found(E.source_vertex, V, screen, VERBOSE)
        
    if val == T_OOB_HYPOTENUSE:
      E2 = E._next
      if t_in_V_region(E2.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E2.source_vertex.get_point_coordinate()):
        if DEBUG:
          print("VV found")
        vv_records.append((E2.source_vertex, V))
        return VV_found(E2.source_vertex, V, screen, VERBOSE)
    e_hold = E._next
    while SL[wrap(i1)][1] != e_hold:
      i1+=1
    if i1 > i2:
      temp = i1
      i1 = i2
      i2 = temp
      if i2 == end_marker:
        break
  
  END_SECOND_FLAG = False
  while wrap(i1) != 0:
    E = SL[wrap(i1)][1]
    V = SL[wrap(i2)][1].source_vertex
    val = t_in_vor_edge(E, V.get_point_coordinate())
    if val == T_IN_VOR_EDGE:
      if t_in_V_region(V, calc_line_point(E, V)):
        if DEBUG:
          print("EV found!")
        ev_records.append((E,V))
        return EV_found(E, V, screen, VERBOSE)
        
    if val == T_OOB_NORM: # candidate for VV, seeking symmetry
      if t_in_V_region(E.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E.source_vertex.get_point_coordinate()):
        if DEBUG:
          print("VV found")
        vv_records.append((E.source_vertex, V))
        return VV_found(E.source_vertex, V, screen, VERBOSE)
        
    if val == T_OOB_HYPOTENUSE:
      E2 = E._next
      if t_in_V_region(E2.source_vertex, V.get_point_coordinate()) and t_in_V_region(V, E2.source_vertex.get_point_coordinate()):
        if DEBUG:
          print("VV found")
        vv_records.append((E2.source_vertex, V))
        return VV_found(E2.source_vertex, V, screen, VERBOSE)
    i1+=1

