#!/usr/bin/python3
import pygame
from pygame_rendering.render_support import *
from support.unit_norms import *

def mark_vertex_clear(v, screen):
  frame_draw_dot(screen, v.get_point_coordinates(), colors["tangerine"], 1)
  pygame.display.update()

def mark_edge_clear(edge, screen):
  e_p1 = edge.source_vertex.get_point_coordinate()
  e_p2 = edge._next.source_vertex.get_point_coordinate()
  frame_draw_line(screen, [e_p1, e_p2], colors["tangerine"])
  pygame.display.update()

def VV_found(v1,v2, screen):
  p1 = v1.get_point_coordinate()
  p2 = v2.get_point_coordinate()
  frame_draw_bold_line(screen,[p1,p2], colors["magenta"])
  pygame.display.update()

def EV_found(edge, v1, screen):
  e_p1 = edge.source_vertex.get_point_coordinate()
  e_p2 = edge._next.source_vertex.get_point_coordinate()
  l = get_unit_norm(e_p1,e_p2)
  e_mid = l.get_origin()
  v_p = v1.get_point_coordinate()
  frame_draw_bold_line(screen, [e_mid, v_p], colors["cyan"])
  pygame.display.update()
  