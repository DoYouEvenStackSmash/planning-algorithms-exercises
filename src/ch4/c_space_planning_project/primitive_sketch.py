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
from coord_conv import two_point_slope
from half_plane import *


colors = {
  "black" : (0,0,0),
  "yellow" : (255,255,0),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255),
  "red" : (255, 0, 0)
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

def main():
  w,h = 1000,1000
  pygame.init()

  lalt = 256
  lshift = 1
  ctrl = 64

  origin = [w/2,h/2]
  o = Point(origin[0], origin[1])
  screen = create_display(w,h)
  a,b = Point(490,490),Point(480,510)
  l = two_point_slope(o, b, a)
  draw_polygon(screen, l.get_segment(), colors["magenta"])
  s,e = l.get_segment()
  draw_dot(screen, s, colors["green"])
  draw_dot(screen, e, colors["cyan"])
  # hp = HalfPlane(o, [l, r])
  # print(hp.set_rad_angle())
  
  # draw_line(screen, hp.get_end_points(), colors["magenta"])
  
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        # print(hp.test_point(p))
        print(p)
      
main()