#!/usr/bin/python3
import pygame
from pygame_rendering.render_support import *
from support.unit_norms import *
from support.star_algorithm import *

def mark_vertex_clear(v, screen):
  '''
  '''
  frame_draw_dot(screen, v.get_point_coordinates(), colors["tangerine"], 1)
  pygame.display.update()

def mark_edge_clear(edge, screen):
  '''
  '''
  e_p1 = edge.source_vertex.get_point_coordinate()
  e_p2 = edge._next.source_vertex.get_point_coordinate()
  frame_draw_line(screen, [e_p1, e_p2], colors["tangerine"])
  pygame.display.update()

def VV_found(v1,v2, screen):
  '''
  Draws a bold line between two vertices
  Does not return
  '''
  p1 = v1.get_point_coordinate()
  p2 = v2.get_point_coordinate()
  frame_draw_bold_line(screen,[p1,p2], colors["magenta"])
  # pygame.display.update()

def EV_found(edge, v1, screen):
  '''
  Draws a bold line between an edge and a vertex
  Does not return
  '''
  v_p = v1.get_point_coordinate()
  mp = calc_line_point(edge, v1)
  frame_draw_bold_line(screen, [mp, v_p], colors["cyan"])
  # pygame.display.update()
  

def calc_line_point(edge, v1):
  '''
  Calculates the nearest point on an edge to vertex v1
  Returns a (x,y) point
  '''
  a = edge.source_vertex.get_point_coordinate()
  b = edge._next.source_vertex.get_point_coordinate()
  t = v1.get_point_coordinate()
  theta_ab = get_ray_angle(a,b)
  theta_at = get_ray_angle(a,t)
  if theta_ab < -np.pi / 2:
    theta_ab = 2 * np.pi + theta_ab
    if theta_at < 0:
      theta_at = 2 * np.pi + theta_at
  theta_E = abs(theta_ab - theta_at)
  rho_at = distance_between_points(a, t)
  r = np.cos(theta_E) * rho_at
  x = r * np.cos(theta_ab) + a[0]
  y = r * np.sin(theta_ab) + a[1]
  return (x,y)
