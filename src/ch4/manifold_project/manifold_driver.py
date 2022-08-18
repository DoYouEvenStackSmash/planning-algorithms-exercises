#!/usr/bin/python3

from venv import create
from identification_objects import *
from flat_cylinder_manifold import *
import sys
import numpy as np
import pygame

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

def frame_draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)

def main():
  pygame.init()
  screen = create_display(1000, 1000)

  o = blank_object(100, 900, 100, 900)
  

  bx = o.get_x_borders()
  by = o.get_y_borders()
  for i in range(2):
    frame_draw_line(screen, [bx[2 * i], bx[2 * i + 1]], colors["cyan"])
    frame_draw_line(screen, [by[2 * i], by[2 * i + 1]], colors["magenta"])

  l = flat_cylinder(o, 60)
  # print(l)
  for i in l:
    frame_draw_line(screen, i, colors["green"])
  pygame.display.update()
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()


main()