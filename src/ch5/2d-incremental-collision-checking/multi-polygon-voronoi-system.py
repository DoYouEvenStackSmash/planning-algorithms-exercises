#!/usr/bin/python3

from support.unit_norms import *
from support.Polygon import *
from support.Line import *
from support.Point import *
from support.World import *
from support.star_algorithm import *
from support.doubly_connected_edge_list import *
from pygame_rendering.pygame_loop_support import *
from pygame_rendering.render_support import PygameArtFxns as pafn
from pygame_rendering.render_support import GeometryFxns as gfn
from pygame_rendering.render_support import MathFxns
from pygame_rendering.render_support import TransformFxns as tfn
from voronoi_regions import *
from feature_markers import *
from polygon_debugging import *
from region_tests import *
from file_loader import *
from transform_polygon import *
from transform_system import *

VERBOSE = False
SAMPLE_RATE = 400
LALT = 256
LSHIFT = 1
LCTRL = 64
SPACE = 32

def construct_star_diagram(A, O):
  '''
  Get the minkowski sum of the two polygons
  Returns a list of points 
  '''
  sl = build_star(A.get_front_edge(),O.get_front_edge())

  obs_spc = derive_obstacle_space_points(sl)
  return obs_spc

def pygame_transform_voronoi_system_loop(screen, A, Olist):
  '''
  Driver function interactions between two polygons A and static O
  Mouse driven path following
  '''
  pts = []
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        # LCTRL for exit hotkey
        if pygame.key.get_mods() == LCTRL:
          sys.exit()
        
        ptlist = []
        
        counter = 0
        # construct the path
        while pygame.MOUSEBUTTONUP not in [event.type for event in pygame.event.get()]:
          continue
        
        p = pygame.mouse.get_pos()
        pts.append(p)
        
        # render line segments between existing points
        pafn.frame_draw_dot(screen, p,pafn.colors["green"])
        for i in range(1,len(pts)):
          pafn.frame_draw_line(screen, (pts[i-1],pts[i]), pafn.colors['green'])
        
        # continue until at least 4 points defined
        if len(pts) < 4:
          pygame.display.update()
          continue
        
        update_world(screen, A, Olist, pts, VERBOSE)
        pygame.display.update()
        pts = []


def triple_polygon_mod():
  '''
  Wrapper for single robot, single obstacle world
  '''
  A = None
  Olist = []
  for arg in sys.argv[1:]:
    try:
      if not A:
        A = build_polygon(arg)
      else:
        Olist.append(build_polygon(arg))
    except:
      pass
  
  # A,O1,O2 = build_polygon(sys.argv[1]),build_polygon(sys.argv[2]), build_polygon(sys.argv[3])
  if A == None: 
    print("robot region is none.")
    sys.exit()
  for o in Olist:
    if o == None:
      print("obstacle region is none")
      sys.exit()
  
  A.color = pafn.colors["green"]
  A.v_color = pafn.colors["cyan"]
  A.e_color = pafn.colors["tangerine"]
  
  for O in Olist:
    O.color = pafn.colors["white"]
    O.v_color = pafn.colors["yellow"]
    O.e_color = pafn.colors["red"]

  # initialize pygame display
  pygame.init()
  screen = pafn.create_display(800,800)
  
  # draw polygons
  sanity_check_polygon(screen, A)  
  for O in Olist:
    sanity_check_polygon(screen, O)
  pygame.display.update()
  # start pygame loop
  pygame_transform_voronoi_system_loop(screen, A, Olist)

def main():
  triple_polygon_mod()

if __name__ == '__main__':
  main()
