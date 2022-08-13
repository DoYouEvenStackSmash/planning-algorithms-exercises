#!/usr/bin/python3
import pygame
import pygame
import numpy as np
import sys
import time
# from coord_conv import create_edge
from half_plane import *
from polygon_support import *
from render_support import *

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

def pygame_polygon_rotation_loop(screen, polygon = None):
  ctrl = 64
  display_polygon_attr(screen, polygon, colors["green"])
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:

        p = pygame.mouse.get_pos()
        if pygame.key.get_mods() == ctrl:
          clear_frame(screen)
          draw_dot(screen, p, colors["white"])
          rotate_polygon(polygon, p)
          base_line = polygon.get_base_line()
          a,b = base_line.get_origin()
          new_line = Line(Point(a,b),300 , base_line.get_rad_angle())
          draw_line(screen, new_line.get_segment(), colors["indigo"])
          display_polygon_attr(screen, polygon, colors["green"])  
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

def pygame_polygon_obstacle_rotation_loop(screen, polygon = None, obstacle_polygon = None):
  ctrl = 64
  polygon_list = [polygon, obstacle_polygon]
  
  display_polygon_attr(screen, polygon, colors["green"])
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:

        p = pygame.mouse.get_pos()
        if pygame.key.get_mods() == ctrl:
          clear_frame(screen)
          draw_dot(screen, p, colors["white"])
          rotate_polygon(polygon, p)
          base_line = polygon.get_base_line()
          a,b = base_line.get_origin()
          new_line = Line(Point(a,b),300 , base_line.get_rad_angle())
          draw_line(screen, new_line.get_segment(), colors["indigo"])
          display_polygon_attr(screen, polygon, colors["green"])  
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
