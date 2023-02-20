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
from voronoi_regions import *
from feature_markers import *
from polygon_debugging import *
from region_tests import *
from file_loader import *
import sys


def pygame_two_region_loop(screen, polygon_list, region_function):
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
        if pygame.key.get_mods() == lalt:
          clear_frame(screen)
          for P in polygon_list:
            sanity_check_polygon(screen, P)
        elif pygame.key.get_mods() == ctrl:
          for P in polygon_list:
            region_function(P, p, screen)
        else:
          print(p)
        pygame.display.update()

def double_polygon_mod():
  if len(sys.argv) < 3:
    print("provide two files")
    sys.exit()
  
  # polygon construction
  A,O = build_polygon(sys.argv[1]),build_polygon(sys.argv[2])
  if A == None or O == None:
    print("one of the regions is none.")
    sys.exit()
  
  A.color = colors["green"]
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  
  O.color = colors["white"]
  O.v_color = colors["yellow"]
  O.e_color = colors["red"]
  
  # function select
  if sys.argv[-1] == '-v':
    rf = lambda P, p, screen : find_vertex_region(P, p, screen)
  elif sys.argv[-1] == '-e':
    rf = lambda P, p, screen : find_edge_region(P, p, screen)
  else:
    rf = lambda P, p, screen : find_all_region(P, p, screen)
  pygame.init()
  screen = create_display(1000,1000)
  
  sanity_check_polygon(screen, O)
  sanity_check_polygon(screen, A)
  pygame_two_region_loop(screen, [A, O], rf)

def main():
  double_polygon_mod()

main()