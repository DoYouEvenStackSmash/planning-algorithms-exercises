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
import pygame
import numpy as np
import sys
import time
from coord_conv import create_edge, two_point_slope
from half_plane import *


colors = {
  "black" : (0,0,0),
  "yellow" : (255,255,0),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255),
  "red" : (255, 0, 0),
  "white" : (255,255,255)
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
  

  # broken
  hp = test_single_left_cross_edge(w,h)

  pygame_loop(screen, hp)
  # a,b = Point(400,400),Point(300,600)
  # l = two_point_slope(o, b, a)
  # hp = HalfPlane(l)
  # print(hp.line.get_rad_angle())
  # draw_polygon(screen, l.get_segment(), colors["white"])
  # s,e = l.get_segment()
  # draw_dot(screen, s, colors["green"])
  # draw_dot(screen, e, colors["red"])
  # # hp = HalfPlane(o, [l, r])
  # # print(hp.set_rad_angle())
  
  # # draw_line(screen, hp.get_end_points(), colors["magenta"])
  
  # while 1:
  #   for event in pygame.event.get():
  #     if event.type == pygame.QUIT:
  #       sys.exit()
  #     if event.type == pygame.MOUSEBUTTONUP:
  #       p = pygame.mouse.get_pos()
  #       val = hp.test_point(p)
  #       if val < 0:
  #         print(f"{p} is right of the line")
  #         draw_dot(screen, p, colors["cyan"])
  #       elif val > 0:
  #         print(f"{p} is left of the line")
  #         draw_dot(screen, p, colors["magenta"])
  #       else:
  #         print(f"{p} is unknown?")
  #       # print(hp.test_point(p))
  #       print(p)
      
main()