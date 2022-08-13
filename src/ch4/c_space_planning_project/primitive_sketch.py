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
# from coord_conv import create_edge
from half_plane import *
from polygon_support import *
from render_support import *


def create_display(width, height):
  return pygame.display.set_mode((width, height))


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

def solve_cross_angle(cross_angle):
  theta_0 = cross_angle
  if theta_0 < np.pi / 2:
    theta_1 = theta_0 + np.pi / 2
  else:
    theta_1 = -2 * np.pi + theta_0 + np.pi / 2
  return theta_1

def compute_end_point(origin, length, rad_angle):
  ox,oy = origin
  r = length
  x = r * np.cos(rad_angle)
  y = r * np.sin(rad_angle)
  return Point(ox + x, oy + y)

def triangle_robot(screen):
  w,h = 1000,1000
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
  sorted_edge_tuple_list = sort_edge_vectors(edge_list)
  e,r = sorted_edge_tuple_list[0]
  print(f"first_edge\t{r.get_rad_angle()}")
  x1,y1 = e.H.line.get_endpoint()
  first_point = Point(x1,y1)
  print(f"first point\t{first_point.get_point()}")
  point_list = [first_point]
  c = 1
  for i,j in sorted_edge_tuple_list[1:]:
    edge_object = i
    norm_v = j
    rad_angle = solve_cross_angle(norm_v.get_rad_angle())
    
    print(norm_v.get_rad_angle())
    length = i.H.line.get_length()
    # print(length)
    # print(rad_angle * 180 / np.pi)
    point_list.append(compute_end_point(point_list[-1].get_point(),length, rad_angle))
    print(f"pt {c}:\t{point_list[-1].get_point()}")
    c+=1
    # point_list.append(compute_end_point(point_list[-1].get_point(),length, rad_angle))

  c_obs = points_to_polygon((500,500),point_list)
  display_polygon_attr(screen,c_obs,colors["magenta"])
  display_polygon_attr(screen, rectangle_p, colors["white"])
  display_polygon_attr(screen, offset_triangle_p, colors["green"])
  polygon_pygame_loop(screen, offset_triangle_p)

def triangle_obstacle(screen):
  w,h = 1000,1000
  draw_dot(screen, (500,500), colors["indigo"])
  # p = test_offset_triangle_polygon(w,h)
  rectangle_p = test_right_triangle_polygon(w,h)
  # test_right_triangle_polygon(w,h)
  # test_rectangular_polygon(w,h)
  offset_triangle_p = test_rectangular_polygon(w,h)
  offset_triangle_p = test_offset_triangle_polygon(w,h)
  edge_list = []
  # obs_el = rectangle_p.get_edge_list()
  # rob_el = offset_triangle_p.get_edge_list()
  add_robot_vectors(offset_triangle_p, edge_list)
  add_obstacle_vectors(rectangle_p, edge_list)
  print(len(edge_list))
  # sel = tuples (Edge, radian key)
  sorted_edge_tuple_list = sort_edge_vectors(edge_list)
  e,r = sorted_edge_tuple_list[0]
  print(f"first_edge\t{r.get_rad_angle()}")
  x1,y1 = e.H.line.get_endpoint()
  first_point = Point(x1,y1)
  print(f"first point\t{first_point.get_point()}")
  point_list = [first_point]
  c = 1
  for i,j in sorted_edge_tuple_list[1:]:
    edge_object = i
    norm_v = j
    rad_angle = solve_cross_angle(norm_v.get_rad_angle())
    
    print(norm_v.get_rad_angle())
    length = i.H.line.get_length()
    # print(length)
    # print(rad_angle * 180 / np.pi)
    point_list.append(compute_end_point(point_list[-1].get_point(),length, rad_angle))
    print(f"pt {c}:\t{point_list[-1].get_point()}")
    c+=1
    # point_list.append(compute_end_point(point_list[-1].get_point(),length, rad_angle))

  c_obs = points_to_polygon((500,500),point_list)
  display_polygon_attr(screen,c_obs,colors["magenta"])
  display_polygon_attr(screen, rectangle_p, colors["white"])
  display_polygon_attr(screen, offset_triangle_p, colors["green"])
  polygon_pygame_loop(screen, offset_triangle_p)
  

def main():
  w,h = 1000,1000
  pygame.init()

  lalt = 256
  lshift = 1
  ctrl = 64

  screen = create_display(w,h)
  
  triangle_robot(screen)

      
main()