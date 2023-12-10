#!/usr/bin/python3
import pygame
import sys

sys.path.append("./support")
sys.path.append("./DCEL")
from env_init import *

# from BoundaryVertex import BoundaryVertex
# from DCEL import *

from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
from graph_processing import *
from cell_decomp_support import VerticalCellDecomposition as vcd
import numpy as np
import time
from V import V
from aux_functions import *
from test_objects import *

THRES =1e-8
xval = lambda m,p: 0 if abs(m) < THRES else m*np.cos(p)
yval = lambda m,p: 0 if abs(m) < THRES else m*np.sin(p)
mag = lambda complex_val: np.sqrt(complex_val.real**2 + complex_val.imag**2)

def phase(complex_val):
    checkfxn = lambda x: [0 if abs(x) < THRES else x]

    r,i = checkfxn(complex_val.real),checkfxn(complex_val.imag)
    
    if r != 0:
        return np.arctan2(i,r)
    if i == 0:
        return 0
    return [np.pi/2 if i > 0 else -np.pi/2]
  
def cart2complex(cart_pt, center=(0,0)):
  """Transforms a cartesian coordinate into a complex number with a center

  Args:
      cart_pt (_type_): _description_
      center (tuple, optional): _description_. Defaults to (0,0).

  Returns:
      _type_: complex exponential
  """
  ox,oy=cart_pt[0] - center[0], cart_pt[1] - center[1]
  r = np.sqrt(ox**2 + oy**2)
  theta = np.arctan2(oy,ox)
  return r * np.exp(1j*theta)

def complex2cart(complex_pt, center=(0,0)):
  """Transforms a complex number into an x,y coordinate

  Args:
      complex_pt (_type_): _description_
      center (tuple, optional): _description_. Defaults to (0,0).

  Returns:
      _type_: pair of coordinates
  """
  m = mag(complex_pt)
  p = phase(complex_pt)
  x = xval(m,p) + center[0]
  y = yval(m,p) + center[1]
  return x,y


def vertical_edge_loop(screen,dcel):
      # #
    pts = chain2vertex(dcel.construct_global_edge_list())
    sortkey = lambda x: x.get_point_coordinate()[0]
    pts = sorted(pts, key=sortkey)
    for p in range(len(pts)):
      pts[p].rank = p
    
    get_adj_succ = lambda p: p.get_half_edge().get_next_half_edge().get_source_vertex()
    get_adj_pred = lambda p: p.get_half_edge().get_prev_half_edge().get_source_vertex()
    v2pt = lambda p: p.get_point_coordinate()
    # #
    
    # active_edges = deque()
    # active_edges.append(get_adj_pred(pts[0]))
    # active_edges.append(get_adj_succ(pts[0]))
    
    get_rank = lambda v: v.rank
    is_active = lambda rank, e: min(get_rank(e.get_source_vertex()), get_rank(get_adj_succ(e))) <= rank and max(get_rank(e.get_source_vertex()), get_rank(get_adj_succ(e))) >= rank
    norm = lambda cv: cv / abs(cv)
    tang = lambda ang: ang * np.exp(1j * np.pi / 2)
    atang = lambda ang: ang * np.exp(1j * -np.pi / 2)
    added_ranks = [0]
    angles = [np.pi / 2, -np.pi / 2]
    
    valid_edges = deque()
    valid_edges.append(get_adj_pred(pts[0]).get_half_edge())
    added_ranks.append(get_rank(get_adj_pred(pts[0])))
    valid_edges.append(get_adj_succ(pts[0]).get_half_edge())
    added_ranks_edges.append(get_rank(get_adj_succ(pts[0])))
    
    # point iteration
    # valid_edges = [e for e in valid_edges if is_active(added_ranks, e)]
    for p in range(1,len(pts)):
      added_ranks = get_rank(pts[p])
      
      nxt = get_adj_succ(pts[p])
      prev = get_adj_pred(pts[p])
      
      pt = pts[p]
  
      p1 = cart2complex(v2pt(prev), v2pt(pt))
      p2 = cart2complex(v2pt(nxt), v2pt(pt))

      bounds = [norm(atang(p1)), norm(tang(p2))]
      delta = np.mean(bounds)
  
      pafn.frame_draw_dot(screen,[x[0],y[0]],pafn.colors["red"])

      a = np.exp(1j * angles[0])
      
      for i in range(len(angles)):
        a = np.exp(1j * angles[i])
        
        if np.angle(delta / a) < 0 and np.angle(p1/ a ) > 0:
          pafn.frame_draw_line(screen, (v2pt(pt), mfn.pol2car(v2pt(pt), 100, angles[i])), pafn.colors["tangerine"])
          
          
        if np.angle(delta / a) > 0 and np.angle(p2 / a) < 0:
          pafn.frame_draw_line(screen, (v2pt(pt), mfn.pol2car(v2pt(pt), 100, angles[i])), pafn.colors["green"])
          
      pygame.display.update()
      time.sleep(0.2)
      
      
def main():

    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)  

    ID,dcel = textbook_obj()
    draw_face(screen, dcel, ID)
    pygame.display.update()
    vertical_edge_loop(screen, dcel)
  
    time.sleep(5)
        

if __name__ == '__main__':
    main()
        