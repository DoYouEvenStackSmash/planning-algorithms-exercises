#!/usr/bin/python3

import pygame
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
# class DrawingFunctions:
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

def display_polygon_attr(screen, polygon = None,color = colors["white"]):
  display_polygon_edges(screen, polygon, color)
  display_out_vectors(screen, polygon)
  display_in_vectors(screen, polygon)

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

def clear_frame(screen):
  pygame.Surface.fill(screen, (0,0,0))

def draw_frame_polygons(screen, polygon_list, polygon_colors):
  for i in range(len(polygon_list)):
    display_polygon_attr(screen, polygon_list[i], polygon_colors[i])  
