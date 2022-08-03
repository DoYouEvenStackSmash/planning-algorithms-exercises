#!/usr/bin/python3

import pygame
import numpy as np
import sys
import time
from manifold_structures import *

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
  pygame.draw.circle(screen, color, point, 2 , 2)
  pygame.display.update()

def draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)
  pygame.display.update()

def draw_plane(screen, point_set, axis_color = (0,0,0), boundary_color = (0,0,0)):
  xs, xe = point_set[0]
  axs, axe = point_set[2]
  ys, ye = point_set[1]
  ays, aye = point_set[3]
  pygame.draw.aaline(screen, axis_color, xs, xe)
  pygame.draw.aaline(screen, axis_color, ys, ye)

  pygame.draw.aaline(screen, boundary_color, axs, axe)
  pygame.draw.aaline(screen, boundary_color, ays, aye)

  pygame.display.update()


def to_rad(deg):
  return np.multiply(deg / 180, np.pi)


def create_axis(origin_pt, length, rad_angle):
  x,y = origin_pt
  return Line(Point(x,y), length, rad_angle)

def create_plane(origin_pt, x_axis, y_axis):
  x,y = origin_pt
  return Plane(Point(x,y), x_axis, y_axis)


def main():
  w,h = 1000,1000
  pygame.init()

  lalt = 256
  lshift = 1
  ctrl = 64

  # 500, 500
  
  origin = [100, 100]
  x_len, y_len = 800,800
  x_rad, y_rad = 0, np.pi / 2
  xa = create_axis(origin, x_len, x_rad)
  ya = create_axis(origin, y_len, y_rad)
  p = create_plane(origin, xa, ya)
  screen = create_display(w,h)
  print(p.make_segment(origin, 30 * np.pi / 180))
  draw_line(screen, p.get_x_axis_segment(), colors["cyan"])
  draw_line(screen, p.get_y_axis_segment(), colors["magenta"])
  draw_line(screen, p.make_segment(origin, 30 * np.pi / 180), colors["green"])
  
  
  yo = create_axis(xa.get_endpoint(), y_len, y_rad)
  xo = create_axis(ya.get_endpoint(), x_len, x_rad)
  draw_line(screen, yo.get_segment(), colors["magenta"])
  draw_line(screen, xo.get_segment(), colors["cyan"])
  
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        sys.exit()

main()
      
