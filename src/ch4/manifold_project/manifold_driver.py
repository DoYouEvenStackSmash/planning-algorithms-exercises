#!/usr/bin/python3

from venv import create
from identification_objects import *
from flat_cylinder_manifold import *
from mobius_manifold import *
from torus_manifold import *
from klein_bottle_manifold import *
from projective_plane import *
from two_sphere_manifold import *
from double_torus_manifold import *
import sys
import numpy as np
import pygame
import time

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

def frame_draw_bold_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.line(screen, color, s, e, width=3)

def frame_draw_dot(screen, point, color = (0,0,0)):
  pygame.draw.circle(screen, color, point, 4, 4)

def clear_frame(screen):
  pygame.Surface.fill(screen, (0,0,0))


# "-RS1": lambda o, deg: flat_cylinder(o, deg),
# "-Ms": lambda o, deg: mobius_strip(o, deg),
# "-T2": lambda o, deg: torus(o, deg),
# "-Kb" : lambda o, deg: klein_bottle(o, deg),
# "-RP2": lambda o, deg: projective_plane(o, deg),
# "-S2" : lambda o, deg: two_sphere(o, deg),
# "-DT2": lambda o, deg: double_torus(o, deg)


fxn_table = {
"-RS1": lambda o, deg: flat_cylinder(o, deg),
"-Ms": lambda o, deg: mobius_strip(o, deg),
"-T2": lambda o, deg: torus(o, deg),
"-Kb" : lambda o, deg: klein_bottle(o, deg),
"-RP2": lambda o, deg: projective_plane(o, deg),
"-S2" : lambda o, deg: two_sphere(o, deg),
"-DT2": lambda o, deg: double_torus(o, deg)
}
def gen_func():
  if len(sys.argv) < 2:
    print("please enter option")
    for i in set(fxn_table):
      print(i)
    sys.exit()
  val = sys.argv[1]
  if val not in fxn_table:
    print(f"{val} not recognized. please choose one of the following:")
    for i in set(fxn_table):
      print(i)
      sys.exit()
  return fxn_table[val]

def change_angle(screen, o):
  bx = o.get_x_borders()
  by = o.get_y_borders()
  gen_fxn = gen_func()
  s = 1
  e = 90
  step = 1
  for flip in range(2):
    for deg in range(s,e,step):
      clear_frame(screen)
      for i in range(2):
        frame_draw_line(screen, [bx[2 * i], bx[2 * i + 1]], colors["cyan"])
        frame_draw_line(screen, [by[2 * i], by[2 * i + 1]], colors["magenta"])
      
      # l = flat_cylinder(o, deg)
      l = gen_fxn(o, deg)
      # l = mobius_strip(o, deg)
      # l = torus(o, deg)
      # l = klein_bottle(o, deg)
      # l = projective_plane(o, deg)
      # l = two_sphere(o, deg)
      # l = double_torus(o, deg)
      print(f"theta: {deg}")
      # print(l)
      # frame_draw_line(screen, [(o.get_x_min(), o.get_y_min()),(o.get_x_max(), o.get_y_max())], colors["red"])
      frame_draw_bold_line(screen, l[0], colors["yellow"])
      frame_draw_dot(screen, l[0][0],colors["green"])
      frame_draw_dot(screen, l[0][1],colors["red"])
      for segment in l[1:]:
        frame_draw_dot(screen, segment[0],colors["green"])
        frame_draw_dot(screen, segment[1],colors["red"])
        frame_draw_line(screen, segment, colors["white"])
        
      pygame.display.update()
      time.sleep(0.12)
    step = step * -1
    s,e = e-1,s-1

def single_angle(screen, o):
  bx = o.get_x_borders()
  by = o.get_y_borders()
  for i in range(2):
    frame_draw_line(screen, [bx[2 * i], bx[2 * i + 1]], colors["cyan"])
    frame_draw_line(screen, [by[2 * i], by[2 * i + 1]], colors["magenta"])

  # l = flat_cylinder(o, 60)
  # l = mobius_strip(o, 20)
  # l = torus(o, 7)
  # l = klein_bottle(o, 60)
  # l = projective_plane(o, 80)
  # l = two_sphere(o, 10)
  l = double_torus(o, 75)
  # print(l)
  
  for i in l:
    frame_draw_line(screen, i, colors["green"])
    frame_draw_dot(screen, i[0], colors["yellow"])
    frame_draw_dot(screen, i[1], colors["red"])
    pygame.display.update()
    time.sleep(1)
  # pygame.display.update()

def main():
  pygame.init()
  w, h = 500, 500
  screen = create_display(w, h)

  o = blank_object(w/10, w - w/10, h/10, h - h/10)
  change_angle(screen,o)
  # single_angle(screen, o)

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()


main()