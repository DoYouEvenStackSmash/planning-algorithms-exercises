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

def lerp_list(p1, p2, n = 100):
  '''
  Lerp helper function for two points
  Returns a list of points
  '''
  pts = []
  step = 1 / n
  for i in range(n):
    pts.append(gfn.lerp(p1, p2, step * i))
  pts.append(p2)
  return pts

def cubic_lerp_calculate(pts, n = 100):
  '''
  Cubic lerp function for a list of at least 4 points
  Returns linear interpolation between pairs of points
    l1=(A,B)
    l2=(B,C)
    l3=(C,D)
    m1 = (l1,l2)
    m2 = (l2,l3)
    p1 = (m1, m2)
  '''
  l1 = lerp_list(pts[0],pts[1])
  l2 = lerp_list(pts[1],pts[2])
  l3 = lerp_list(pts[2],pts[3])
  m1 = []
  m2 = []
  step = 1 / n

  for i in range(n):
    m1.append(gfn.lerp(l1[i],l2[i],i * step))
    m2.append(gfn.lerp(l2[i],l3[i],i * step))
  m1.append(gfn.lerp(l1[-1],l2[-1],1))
  m2.append(gfn.lerp(l2[-1],l3[-1],1))

  p1 = []
  for i in range(n):
    p1.append(gfn.lerp(m1[i],m2[i],i * step))
  p1.append(gfn.lerp(m1[-1],m2[-1],1))
  return l1,l2,l3,m1,m2,p1

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
        pafn.frame_draw_dot(screen, p,pafn.colors["green"])
        for i in range(1,len(pts)):
          pafn.frame_draw_line(screen, (pts[i-1],pts[i]), pafn.colors['green'])
        if len(pts) == 4:
          pafn.clear_frame(screen)
          pafn.frame_draw_polygon(screen, pts, pafn.colors["red"])
          l1,l2,l3,m1,m2,mpts = cubic_lerp_calculate(pts)
          
          # lerp rendering
          for i in range(len(mpts)):
            pafn.clear_frame(screen)
            # render points up to i
            for j in range(i):
              pafn.frame_draw_dot(screen, mpts[j], pafn.colors["cyan"])
            # render lines
            pafn.frame_draw_line(screen, (pts[0],pts[1]), pafn.colors['red'])
            pafn.frame_draw_line(screen, (pts[1],pts[2]), pafn.colors['red'])
            pafn.frame_draw_line(screen, (pts[2],pts[3]), pafn.colors['red'])
            pafn.frame_draw_line(screen, (l1[i],l2[i]),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (l2[i],l3[i]),pafn.colors["tangerine"])
            pafn.frame_draw_bold_line(screen, (m1[i],m2[i]),pafn.colors['green'])
            sanity_check_polygon(screen, A)
            for O in Olist:
              sanity_check_polygon(screen, O)

            pygame.display.update()
            time.sleep(0.005)
          pts = []
          ptlist = mpts
        else:
          pygame.display.update()
          continue
        
        # observe the line
        # time.sleep(0.5)
        #clear_frame(screen)
        
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
        ptlist = []
          


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
