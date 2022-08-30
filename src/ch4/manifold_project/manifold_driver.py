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

''' drawing colors '''
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

''' 
  helpers for rendering 
'''
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

fxn_help = {
  "-RS1": "flat_cylinder",
  "-Ms":  "mobius_strip",
  "-T2":  "torus",
  "-Kb" : "klein_bottle",
  "-RP2": "projective_plane",
  "-S2" : "two_sphere",
  "-DT2": "double_torus"
  }

fxn_table = {
"-RS1": lambda o, deg: flat_cylinder(o, deg),
"-Ms": lambda o, deg: mobius_strip(o, deg),
"-T2": lambda o, deg: torus(o, deg),
"-Kb" : lambda o, deg: klein_bottle(o, deg),
"-RP2": lambda o, deg: projective_plane(o, deg),
"-S2" : lambda o, deg: two_sphere(o, deg),
"-DT2": lambda o, deg: double_torus(o, deg)
}

def print_args_help():
  for i in set(fxn_table):
    print(f"\t{i}\t{fxn_help[i]}")

# helper for reading options from cli
def gen_func():
  if len(sys.argv) < 2:
    print(f"USAGE:\n\t./manifold_driver.py [ARG]")
    print_args_help()
    sys.exit()
  val = sys.argv[1]
  if val not in fxn_table:
    print(f"{val} not recognized")
    print(f"USAGE:\n\t./manifold_driver.py [ARG]")
    print_args_help()
    sys.exit()
  return fxn_table[val]

'''
  change_angle:
    Sweeps an "infinite" line, constrained to origin point, from [0,90] degrees across a specified 2d manifold. 
    Color Codes;
      Bold Yellow is original line.
      Green dot is start of line segment
      Red Dot is end of line segment
      Cyan is x axis
      Magenta is y axis
'''
def change_angle(screen, o):
  bx = o.get_x_borders()
  by = o.get_y_borders()
  gen_fxn = gen_func()
  s = 1
  e = 90
  step = 1
  # 1->90, 90->1
  for flip in range(2):
    for deg in range(s,e,step):
      clear_frame(screen)
      # draw axes
      for i in range(2):
        frame_draw_line(screen, [bx[2 * i], bx[2 * i + 1]], colors["cyan"])
        frame_draw_line(screen, [by[2 * i], by[2 * i + 1]], colors["magenta"])
      
      # generate manifold segments for deg
      l = gen_fxn(o, deg)
      print(f"theta: {deg}")
      
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

'''
  single_angle:
    Infinite line, constrained to origin point, on a specified 2d manifold for a hardcoded angle.
  '''
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