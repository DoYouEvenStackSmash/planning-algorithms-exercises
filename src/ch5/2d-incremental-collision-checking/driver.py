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



# def draw_test_vectors(point_list):
  
def adjust_points(point_list, center):
  adj_point_list = []
  for i in range(len(point_list)):
    x,y = point_list[i]
    adj_point_list.append([x + center, y + center])
  return adj_point_list


def main():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  p = load_json_file(sys.argv[1])
  if not len(p):
    print(f"json file did not load.")
    sys.exit()
  # p = adjust_points(p, 350)
  # return
  
  P = Polygon(p)
  
  pygame.init()
  w, h = 1000,1000
  screen = create_display(w, h)
  draw_lines_between_points(screen, P.dump_points(), colors["green"])
  W = World()
  pts = P.dump_points()
  s = P.dump_segments()
  for i,j in s:
    W.create_half_plane(i, j)
  # W.create_half_plane(pts[0], pts[1])
  for i in s:
    a,b = i
    l = get_unit_norm(a,b)
    l.toggle_switch()
    frame_draw_line(screen, l.get_segment(), colors["yellow"])
  
  # frame_draw_line(screen, s[0], colors["magenta"])
  # a,b = s[0]
  
  
  pygame.display.update()
  for i,j in enumerate(pts):
    print(f"{i}:\t{j}")
  # frame_draw_polygon(screen, pts, colors["magenta"])
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
          

main()