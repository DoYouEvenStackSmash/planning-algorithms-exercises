#!/usr/bin/python3

from support.unit_norms import *
from support.Polygon import *
from support.Line import *
from support.Point import *
from support.World import *
from support.star_algorithm import *
from support.doubly_connected_edge_list import *
from pygame_rendering.pygame_loop_support import *
from pygame_rendering.render_support import *

from file_loader import *

import sys
import time

def build_polygon(filename):
  pts = load_json_file(filename)
  if not len(pts):
    print("no polygon can be built.")
    return None
  P = Polygon(pts)
  return P


def sanity_check_polygon(screen, P):
  draw_lines_between_points(screen, P.dump_points(), P.color)
  pygame.display.update()
  # s = P.dump_segments()
  # for i in s:
  #   a,b = i
  #   l = get_unit_norm(a,b)
  #   # should draw outward vectors
  #   frame_draw_line(screen, l.get_segment(), colors["yellow"])
  #   # should draw inward vectors
  #   l.toggle_switch()
  #   frame_draw_line(screen, l.get_segment(), colors["sky-blue"])
  # pygame.display.update()
  
  # draw_lines_between_points(screen, O.dump_points(), O.color)


def construct_star_diagram(A, O, origin):

  sl = build_star(A.get_front_edge(),O.get_front_edge())
  for e in sl:
    print(f"angle:\t{e[0]}")
  obs_spc = derive_obstacle_space_points(sl)
  return obs_spc
  # segments = get_star_segments(sl, origin)
  # return segments
  # print(len(sl))

def build_obstacle_space():
  if len(sys.argv) < 3:
    print("provide two files")
    sys.exit()
  pygame.init()
  screen = create_display(1600,1000)
  # pygame_loop(screen)
  
  A,O = build_polygon(sys.argv[1]),build_polygon(sys.argv[2])
  if A == None or O == None:
    print("one of the regions is none.")
    sys.exit()

  A.color = colors["green"]
  O.color = colors["white"]
  sanity_check_polygon(screen, A)
  sanity_check_polygon(screen, O)
  origin = (1000,500)
  obstacle_space_points = construct_star_diagram(A, O,origin)
  C_obs = Polygon(obstacle_space_points)
  C_obs.color = colors["magenta"]
  sanity_check_polygon(screen, C_obs)
  for i in obstacle_space_points:
    print(i)
  # for i in segments:
  #   print(i)
  #   frame_draw_line(screen, i, colors["tangerine"])
  pygame.display.update()
  
  pygame_loop(screen)

def main():
  build_obstacle_space()
  
  

main()



