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

'''
  CTRL: Given a polygon P, draws a line from at most one vertex region of P to a
        a mouse-click target point.
  LALT: Clears the frame and redraws the polygon
'''
def pygame_region_loop(screen, P, region_function):
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
          sanity_check_polygon(screen, P)
        elif pygame.key.get_mods() == ctrl:
          region_function(P, p, screen)
        else:
          print(p)
        pygame.display.update()

'''
  loads a single polygon from a file.
'''  
def single_polygon_mod():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  if sys.argv[-1] == '-v':
    rf = lambda P, p, screen : find_vertex_region(P, p, screen)
  elif sys.argv[-1] == '-e':
    rf = lambda P, p, screen : find_edge_region(P, p, screen)
  else:
    rf = lambda P, p, screen : find_all_region(P, p, screen)
  
  filename = sys.argv[1]
  
  A = build_polygon(filename)
  if A == None:
    print("the polygon is invalid. exiting...")
    sys.exit()
  A.color = colors["white"]
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, A)
  pygame_region_loop(screen, A, rf)

def main():

  single_polygon_mod()

main()