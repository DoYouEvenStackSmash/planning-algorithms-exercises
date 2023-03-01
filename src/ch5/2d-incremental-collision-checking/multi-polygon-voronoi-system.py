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
          if not counter % SAMPLE_RATE:
            ptlist.append(pygame.mouse.get_pos())
            frame_draw_dot(screen, ptlist[-1], colors["yellow"])
            pygame.display.update()
          counter+=1
        
        # observe the line
        # time.sleep(0.5)
        clear_frame(screen)
        
        # execute the path following
        p_last = None
        for p in range(len(ptlist)):
          if p_last != ptlist[p]:
            flag1 = gradually_rotate_voronoi_system(A, Olist, ptlist[p], screen,path_line=ptlist[p:])
            if flag1 > 1:
              break
            flag2 = gradually_translate_voronoi_system(A,Olist,ptlist[p], screen,path_line=ptlist[p:])
            if flag2 > 1:
              break
          p_last = ptlist[p]
          


def triple_polygon_mod():
  '''
  Wrapper for single robot, single obstacle world
  '''
  if len(sys.argv) < 4:
    print("provide two files")
    sys.exit()
  
  # initialize and construct polygons
  A = build_polygon(sys.argv[1])
  Olist = []
  for i in sys.argv[2:]:
    Olist.append(build_polygon(i))

  # A,O1,O2 = build_polygon(sys.argv[1]),build_polygon(sys.argv[2]), build_polygon(sys.argv[3])
  if A == None: 
    print("robot region is none.")
    sys.exit()
  for o in Olist:
    if o == None:
      print("obstacle region is none")
      sys.exit()
  
  A.color = colors["green"]
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  
  for O in Olist:
    O.color = colors["white"]
    O.v_color = colors["yellow"]
    O.e_color = colors["red"]

  # initialize pygame display
  pygame.init()
  screen = create_display(1000,1000)
  
  # draw polygons
  sanity_check_polygon(screen, A)  
  for O in Olist:
    sanity_check_polygon(screen, O)

  # start pygame loop
  pygame_transform_voronoi_system_loop(screen, A, Olist)

def main():
  triple_polygon_mod()

if __name__ == '__main__':
  main()