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
  # print(f"building polygon from")
  pts = load_point_set(filename)
  if not len(pts):
    print("no polygon can be built.")
    return None
  P = Polygon(pts)
  return P

def sanity_check_polygon(screen, P):
  draw_lines_between_points(screen, P.dump_points(), P.color)
  pygame.display.update()

def sanity_check_edge(screen, edge):
  he_curr = edge
  
  p1 = he_curr.source_vertex.get_point_coordinate()
  p2 = he_curr._next.source_vertex.get_point_coordinate()
  frame_draw_line(screen,[p1,p2],colors["white"])
  # frame_draw_dot(screen,p1,colors["white"])
  # frame_draw_dot(screen,p2,colors["white"])
  pygame.display.update()

def voronoi_prep(P):
  env = []
  load_edge_normal_vectors(P.get_front_edge(),env)
  print(env[0][0])
  return env

  

def pygame_half_planes_loop(screen,W):
  lalt = 256
  lshift = 1
  ctrl = 64

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        print(p)
        # if pygame.key.get_mods() == ctrl:
        val = W.test_set_of_planes(p)
        # val = W.test_plane(p, 0)
        if val < 0:
          print(f"{p} is right of the line")
          frame_draw_dot(screen, p, colors["cyan"])
        elif val > 0:
          print(f"{p} is left of the line")
          frame_draw_dot(screen, p, colors["magenta"])
        else:
          print(f"{p} is unknown?")
        pygame.display.update()

def main():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  filename = sys.argv[1]
  A = build_polygon(filename)
  if not A:
    print(f"could not build polygon from {filename}")
    print("\nexiting...")
    sys.exit()
  A.color = colors["green"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, A)
  s = A.dump_segments()
  W = World()
  W.create_half_plane(s[0][0],s[0][1])
  frame_draw_line(screen, s[0], colors["magenta"])
  edge_list = voronoi_prep(A)
  pygame.display.update()
  sanity_check_edge(screen, edge_list[0][1])
  pygame_half_planes_loop(screen,W)
  # pygame_loop(screen)

main()
  

