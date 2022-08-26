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
from transform_polygon import *
from transform_system import *

def pygame_transform_system_loop(screen, A, O):
  lalt = 256
  lshift = 1
  ctrl = 64
  OPList = [A, O]
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        print(p)
        if pygame.key.get_mods() == ctrl:
          clear_frame(screen)
          gradually_rotate_system(OPList, 0, p, screen)
        elif pygame.key.get_mods() == lalt:
          clear_frame(screen)
          gradually_translate_system(OPList, 0, p, screen)
        elif pygame.key.get_mods() == lshift:
          clear_frame(screen)
          for P in OPList:
            sanity_check_polygon(screen, P)
        else:
          print(p)

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
  
  # # function select
  # if sys.argv[-1] == '-v':
  #   rf = lambda P, p, screen : find_vertex_region(P, p, screen)
  # elif sys.argv[-1] == '-e':
  #   rf = lambda P, p, screen : find_edge_region(P, p, screen)
  # else:
  #   rf = lambda P, p, screen : find_all_region(P, p, screen)
  pygame.init()
  screen = create_display(1600,1000)
  sanity_check_polygon(screen, A)  
  sanity_check_polygon(screen, O)
  pygame_transform_system_loop(screen, A, O)

def main():
  double_polygon_mod()

main()
