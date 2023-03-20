#!/usr/bin/python3

import pygame
# from pygame_rendering.render_support import *
from pygame_rendering.render_support import PygameArtFxns as pafn

from region_tests import *
from support.Polygon import *

def build_polygon(filename):
  '''
  Builds a polygon object from a file
  Returns a Polygon object
  '''
  pts = load_point_set(filename)
  if not len(pts):
    print("no polygon can be built.")
    return None
  P = Polygon(pts)
  return P


def sanity_check_polygon(screen, P):
  '''
  Draws a single polygon
  Does not return
  '''
  pafn.draw_lines_between_points(screen, P.dump_points(), P.color)
  #pygame.display.update()


def sanity_check_edge(screen, edge):
  '''
  Draws a single Half Edge  
  Does not return
  '''
  he_curr = edge
  
  p1 = he_curr.source_vertex.get_point_coordinate()
  p2 = he_curr._next.source_vertex.get_point_coordinate()
  pafn.frame_draw_line(screen,[p1,p2],pafn.colors["white"])
  pafn.frame_draw_dot(screen,p1,pafn.colors["white"])
  pafn.frame_draw_dot(screen,p2,pafn.colors["indigo"])
  #pygame.display.update()


def find_vertex_region(P, t, screen):
  '''
  Draws a line between point t and its corresponding voronoi vertex region in P
  Does not return
  '''
  h = P.get_front_edge()
  
  e_fov = t_in_V_region(h.source_vertex, t)
  if e_fov:
    pt = h.source_vertex.get_point_coordinate()
    pafn.frame_draw_line(screen, [pt,t], P.color)
    #pygame.display.update()
  else:
    print(f"{t} not in half plane")
  h = h._next
  while h != P.get_front_edge():
    e_fov = t_in_V_region(h.source_vertex, t)
    if e_fov:
      pt = h.source_vertex.get_point_coordinate()
      pafn.frame_draw_line(screen, [pt,t], P.color)
      #pygame.display.update()
    else:
      print(f"{t} not in half plane")
    h = h._next


def find_edge_region(P, t, screen):
  '''
  Draws a line between point t and its corresponding voronoi edge region in P
  Does not return
  '''
  h = P.get_front_edge()
  e_reg = t_in_E_region(h, t)
  if e_reg:
    pt1 = h.source_vertex.get_point_coordinate()
    pt2 = h._next.source_vertex.get_point_coordinate()
    l = get_unit_norm(pt1, pt2)
    mid = l.get_origin()
    pafn.frame_draw_line(screen, [mid,t], P.color)
    #pygame.display.update()
  else:
    print(f"{t} not in edge {h._id} region")
  h = h._next
  while h != P.get_front_edge():
    e_reg = t_in_E_region(h, t)
    if e_reg:
      pt1 = h.source_vertex.get_point_coordinate()
      pt2 = h._next.source_vertex.get_point_coordinate()
      l = get_unit_norm(pt1, pt2)
      mid = l.get_origin()
      pafn.frame_draw_line(screen, [mid,t], P.color)
      #pygame.display.update()
    else:
      print(f"{t} not in edge {h._id} region")
    h = h._next


def find_all_region(P, t, screen):
  '''
  Draws a line between point t and its corresponding voronoi region in P
  Combination of find_edge_region and find_vertex_region.
  
  Does not return
  '''
  h = P.get_front_edge()
  e_reg = t_in_E_region(h, t)
  v_reg = t_in_V_region(h.source_vertex, t)
  if v_reg:
    pt = h.source_vertex.get_point_coordinate()
    pafn.frame_draw_line(screen, [pt,t], P.v_color)
    #pygame.display.update()
  else:
    print(f"{t} not in v_reg")
  if e_reg:
    pt1 = h.source_vertex.get_point_coordinate()
    pt2 = h._next.source_vertex.get_point_coordinate()
    l = get_unit_norm(pt1, pt2)
    mid = l.get_origin()
    pafn.frame_draw_line(screen, [mid,t], P.e_color)
    #pygame.display.update()
  else:
    print(f"{t} not in edge {h._id} region")
  if v_reg and e_reg:
      print("what?")
  
  # loop around doubly connected edge list
  h = h._next
  while h != P.get_front_edge():
    e_reg = t_in_E_region(h, t)
    v_reg = t_in_V_region(h.source_vertex, t)
    if v_reg:
      pt = h.source_vertex.get_point_coordinate()
      pafn.frame_draw_line(screen, [pt,t], P.v_color)
      #pygame.display.update()
    else:
      print(f"{t} not in v_reg")
    if e_reg:
      pt1 = h.source_vertex.get_point_coordinate()
      pt2 = h._next.source_vertex.get_point_coordinate()
      l = get_unit_norm(pt1, pt2)
      mid = l.get_origin()
      pafn.frame_draw_line(screen, [mid,t], P.e_color)
      #pygame.display.update()
    else:
      print(f"{t} not in edge {h._id} region")
    if v_reg and e_reg:
      print("what?")
    h = h._next

def find_hp_region(P, t, screen):
  '''
  Draws a line between t and its enclosing half plane in P
  
  Does not return
  '''
  h = P.get_front_edge()
  pt1 = h.source_vertex.get_point_coordinate()
  pt2 = h._next.source_vertex.get_point_coordinate()
  h1 = check_half_plane(pt1, pt2, t)
  if h1:
    l = get_unit_norm(pt1,pt2)
    mid = l.get_origin()
    pafn.frame_draw_line(screen, [mid,t], P.color)
    #pygame.display.update()
  else:
    print(f"{t} not in half plane")
  h = h._next
  while h != P.get_front_edge():
    pt1 = h.source_vertex.get_point_coordinate()
    pt2 = h._next.source_vertex.get_point_coordinate()
    h1 = check_half_plane(pt1, pt2, t)
    if h1:
      l = get_unit_norm(pt1,pt2)
      mid = l.get_origin()
      pafn.frame_draw_line(screen, [mid,t], P.color)
      #pygame.display.update()
    else:
      print(f"{t} not in half plane")
    h = h._next
