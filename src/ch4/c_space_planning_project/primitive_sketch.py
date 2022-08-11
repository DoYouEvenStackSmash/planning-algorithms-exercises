#!/usr/bin/python3

# plane

# primitive
'''
  half plane
    linear equation
    h = {(x,y) in W | f(x,y) <= 0}

   point-slope form
  
  slope = m = y2 - y1 / x2 - x1
  point slope = y - y1 = m(x - x1)
  
  slope intercept form:

  solve for y to get y = mx + b

  standard form Ax + By = C

'''
from operator import ge
import pygame
import numpy as np
import sys
import time
from coord_conv import create_edge
from half_plane import *
from polygon_support import *


colors = {
  "black" : (0,0,0),
  "yellow" : (255,255,0),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255),
  "red" : (255, 0, 0),
  "white" : (255,255,255),
  "indigo" : (48,79,254)
}

def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_polygon(screen, point_set, color = (0,0,0)):
  pygame.draw.polygon(screen, color, point_set, width = 1)
  pygame.display.update()

def draw_dot(screen, point, color = (0,0,0)):
  pygame.draw.circle(screen, color, point, 4 , 4)
  pygame.display.update()

def draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)
  pygame.display.update()

def frame_draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)


def get_single_edge(o, pt1, pt2):
  l = create_edge(o,pt1,pt2)
  hp = HalfPlane(l)
  return hp


def test_single_down_left_edge(w = 0, h = 0):
  origin = [w/2,h/2]
  
  o = Point(origin[0], origin[1])
  # screen = create_display(w,h)

  pt1 = Point(400,600)
  pt2 = Point(300,400)
  return get_single_edge(o, pt1, pt2)

def test_single_up_left_edge(w = 0,h = 0):
  origin = [w/2,h/2]
  
  o = Point(origin[0], origin[1])
  # screen = create_display(w,h)

  pt1 = Point(520,520)
  pt2 = Point(420,620)
  return get_single_edge(o, pt1, pt2)

def test_single_right_cross_edge(w = 0, h = 0):
  origin = [w/2,h/2]
  
  o = Point(origin[0], origin[1])
  # screen = create_display(w,h)

  pt1 = Point(520,520)
  pt2 = Point(420,520)
  return get_single_edge(o, pt1, pt2)

def test_single_left_cross_edge(w = 0, h = 0):
  origin = [w/2,h/2]
  
  o = Point(origin[0], origin[1])
  # screen = create_display(w,h)
  pt1 = Point(420,520)
  pt2 = Point(520,520)
  
  return get_single_edge(o, pt1, pt2)

def test_rectangular_polygon(w = 0, h = 0):
  origin = [w/2,h/2]
  # origin = [700,700]
  o = Point(origin[0], origin[1])
  pt1 = Point(590,590)
  pt2 = Point(770,590)
  pt3 = Point(770,710)
  pt4 = Point(590,710)
  h1 = get_single_edge(o,pt1,pt2)
  h2 = get_single_edge(o,pt2,pt3)
  h3 = get_single_edge(o,pt3,pt4)
  h4 = get_single_edge(o,pt4,pt1)
  e1 = Edge(h1)
  e2 = Edge(h2)
  e3 = Edge(h3)
  e4 = Edge(h4)
  e1.m_next = e2
  e2.m_next = e3
  e3.m_next = e4
  e4.m_next = e1
  p = Polygon()
  p.half_planes_head = e1
  return p

def test_offset_triangle_polygon(w = 0, h = 0):
  origin = [w/2,h/2]
  # origin = [700,700]
  o = Point(origin[0], origin[1])
  # screen = create_display(w,h)
  #(-1,3),(-5,1),(-4,-1) scaled by 30, from origin 500,500
  pt1 = Point(470,590)
  pt2 = Point(350,530)
  pt3 = Point(380,470)
  h1 = get_single_edge(o,pt1,pt2)
  h2 = get_single_edge(o,pt2,pt3)
  h3 = get_single_edge(o,pt3,pt1)
  e1 = Edge(h1)
  e2 = Edge(h2)
  e3 = Edge(h3)
  e1.m_next = e2
  e2.m_next = e3
  e3.m_next = e1
  p = Polygon()
  p.half_planes_head = e1
  return p

def test_right_triangle_polygon(w = 0, h = 0):
  origin = [w/2,h/2]
  # origin = [700,700]
  o = Point(origin[0], origin[1])
  # screen = create_display(w,h)
  pt1 = Point(600,600)
  pt2 = Point(400,600)
  pt3 = Point(400,400)
  h1 = get_single_edge(o,pt1,pt2)
  h2 = get_single_edge(o,pt2,pt3)
  h3 = get_single_edge(o,pt3,pt1)
  e1 = Edge(h1)
  e2 = Edge(h2)
  e3 = Edge(h3)
  e1.m_next = e2
  e2.m_next = e3
  e3.m_next = e1
  p = Polygon()
  p.half_planes_head = e1
  return p

def display_in_vectors(screen, polygon = None):
  x = polygon.get_in_vec_segments()
  for i in x:
    draw_line(screen, i, colors["yellow"])

def display_out_vectors(screen, polygon = None):
  x = polygon.get_out_vec_segments()
  for i in x:
    draw_line(screen, i, colors["red"])

def display_polygon_edges(screen, polygon = None, color = colors["white"]):
  x = polygon.get_segments()
  for i in x:
    draw_line(screen, i, color)

def polygon_pygame_loop(screen, polygon = None):
  # print(polygon.get_segments())
  
  # y = polygon.get_in_vec_segments()
  # for i in y:
  #   draw_line(screen, i, colors["yellow"])
  # draw_polygon(screen, polygon.get_segments(), colors["white"])
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        val = polygon.check_collision(p)
        if val == False:
          print(f"{p} is right of the line")
          draw_dot(screen, p, colors["cyan"])
        elif val == True:
          print(f"{p} is left of the line")
          draw_dot(screen, p, colors["magenta"])
        else:
          print(f"{p} is unknown?")
        # print(hp.test_point(p))
        print(p)

def pygame_loop(screen,hp = None):
  draw_polygon(screen, hp.line.get_segment(), colors["white"])
  s,e = hp.line.get_segment()
  draw_dot(screen, s, colors["green"])
  draw_dot(screen, e, colors["red"])
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        val = hp.test_point(p)
        if val < 0:
          print(f"{p} is right of the line")
          draw_dot(screen, p, colors["cyan"])
        elif val > 0:
          print(f"{p} is left of the line")
          draw_dot(screen, p, colors["magenta"])
        else:
          print(f"{p} is unknown?")
        # print(hp.test_point(p))
        print(p)

def display_polygon_attr(screen, polygon = None,color = colors["white"]):
  display_polygon_edges(screen, polygon, color)
  display_out_vectors(screen, polygon)
  display_in_vectors(screen, polygon)


def conv_func(theta):
    if theta < 0:
      return 2 * np.pi - abs(theta)
    return theta

def edge_key(e):
  return conv_func(e[1].get_rad_angle())

def sort_edge_vectors(edge_list):
  adjust = lambda edge_obj : edge_key(edge_obj)
  sorted_edge_list = sorted(edge_list, key=adjust)
  return sorted_edge_list

def add_robot_vectors(polygon, edge_vector_list):
  in_el = polygon.get_edge_list()
  for e in in_el:
    edge_vector_list.append((e,e.get_in_vec()))

def add_obstacle_vectors(polygon, edge_list):
  out_el = polygon.get_edge_list()
  for e in out_el:
    edge_list.append((e,e.get_out_vec()))


def main():
  w,h = 1000,1000
  pygame.init()

  lalt = 256
  lshift = 1
  ctrl = 64

  # origin = [w/2,h/2]
  # o = Point(origin[0], origin[1])
  screen = create_display(w,h)
  # hp = test_single_up_left_edge(w,h)
  
  # x1 -> x2 
  # hp = test_single_right_cross_edge(w,h)
  # hp = test_single_down_left_edge(w,h)
  # p = test_right_triangle_polygon(w,h)
  draw_dot(screen, (500,500), colors["indigo"])
  # p = test_offset_triangle_polygon(w,h)
  rectangle_p = test_rectangular_polygon(w,h)
  offset_triangle_p = test_offset_triangle_polygon(w,h)
  edge_list = []
  # obs_el = rectangle_p.get_edge_list()
  # rob_el = offset_triangle_p.get_edge_list()
  add_robot_vectors(offset_triangle_p, edge_list)
  add_obstacle_vectors(rectangle_p, edge_list)
  print(len(edge_list))
  # sel = tuples (Edge, radian key)
  sel = sort_edge_vectors(edge_list)
  for i,j in sel:
    draw_line(screen, i.H.line.get_segment(),colors["white"])
    time.sleep(1)
  
  # display_polygon_attr(screen, rectangle_p)
  # display_polygon_attr(screen, offset_triangle_p, colors["green"])
  # display_polygon_edges(screen, p)
  # display_out_vectors(screen, p)
  # display_in_vectors(screen, p)
  polygon_pygame_loop(screen, offset_triangle_p)

      
main()