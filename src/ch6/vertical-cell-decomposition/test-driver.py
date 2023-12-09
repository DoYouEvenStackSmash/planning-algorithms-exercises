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
  ox,oy=cart_pt[0] - center[0], cart_pt[1] - center[1]
  r = np.sqrt(ox**2 + oy**2)
  theta = np.arctan2(oy,ox)
  return r * np.exp(1j*theta)

def complex2cart(complex_pt, center=(0,0)):
  m = mag(complex_pt)
  p = phase(complex_pt)
  x = xval(m,p) + center[0]
  y = yval(m,p) + center[1]
  return x,y
  

def draw_shape(screen, bc, maxs=(1000,1000)):
      
    for p in range(1, len(bc)):
        
        pafn.frame_draw_dot(screen, bc[p-1])
        ptx = cart2complex(bc[p], bc[p-1]) * np.exp(1j * np.pi/2) * 0.5
        new_pt = complex2cart(ptx, bc[p-1])
        pafn.frame_draw_ray(screen, bc[p-1], bc[p], pafn.colors['magenta'])
        pygame.display.update()
        time.sleep(0.5)
        pafn.frame_draw_ray(screen, bc[p-1], new_pt, pafn.colors['green'])
        pygame.display.update()
        time.sleep(0.5)
    
    pafn.frame_draw_dot(screen, bc[-1])
    ptx = cart2complex(bc[0], bc[-1]) * np.exp(1j * np.pi/2) * 0.5
    new_pt = complex2cart(ptx, bc[-1])
    pafn.frame_draw_ray(screen, bc[-1], bc[0], pafn.colors['cyan'])
    pygame.display.update()
    time.sleep(0.5)
    pafn.frame_draw_ray(screen, bc[-1], new_pt, pafn.colors['green'])
    pygame.display.update()


def draw_last_point(screen, point_list):

    pafn.frame_draw_ray(screen, point_list[-1], point_list[0], pafn.colors['cyan'])
    pygame.display.update()
    time.sleep(0.5)
    
    
  
def chain2vertex(chain):
  return [e.get_source_vertex() for e in chain]

def chain2points(chain):
  return [e.get_point_coordinate() for e in chain2vertex(chain)]

def draw_face(screen, dcel, f_id=0):
  face = dcel.face_records[f_id]
  point_list = chain2points(face.get_boundary_chain())
  
  for p in range(1, len(point_list)):

    pafn.frame_draw_ray(screen, point_list[p-1], point_list[p], pafn.colors['magenta'])
    
    pygame.display.update()
    time.sleep(0.2)
  draw_last_point(screen, point_list)
  pygame.display.update()
  

  for ic in face.get_interior_component_chains():
    ic_point_list = chain2points(ic)
    for p in range(1, len(ic_point_list)):

      pafn.frame_draw_ray(screen, ic_point_list[p-1], ic_point_list[p], pafn.colors['magenta'])
      
    draw_last_point(screen, ic_point_list)
    pygame.display.update()
  
  
def main():
    bc = [
        (159, 629),
        (332, 196),
        (427, 260),
        (581, 82),
        (765, 148),
        (628, 329),
        (534, 269),
        (460, 391),
        (608, 638),
        (427, 832),
    ]
    dcel = DCEL()
    a = [(436, 754), (401, 674), (501, 667)]
    b = [(437, 326), (422, 380), (396, 334), (430, 291), (487, 286)]
    c = [(590, 242), (556, 163), (680, 198)]
    x = [(397, 605), (319, 661), (368, 549), (290, 570), (395, 458)]
    x.reverse()
    print(a)
    a.reverse()
    print(a)
    # sys.exit()
    b.reverse()
    c.reverse()
    ID = dcel.create_face(bc, [[(308, 609), (257, 591), (323, 424), (199, 619)], x, a, b, c])
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)  
    #
    # bc = [(226, 280), (778, 284), (670, 711), (136, 706)]
    # obs_1 = [(285, 579), (430, 622), (345, 515), (485, 333), (260, 393)]
    # obs_2 = [(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)]
    
    # bc = [(137, 86), (965, 56), (920, 944), (75, 930)]
    # obs_1 = [(879, 116), (782, 160), (668, 154), (535, 174), (424, 221), (301, 361), (245, 515), (286, 648), (403, 727), (560, 757), (694, 734), (788, 616), (814, 491), (783, 361), (712, 278), (599, 267), (474, 349), (411, 474), (434, 546), (549, 560), (589, 528), (579, 462), (541, 392), (580, 314), (658, 319), (718, 361), (750, 474), (729, 576), (686, 633), (599, 668), (500, 671), (360, 604), (341, 495), (358, 406), (444, 317), (568, 237), (686, 195), (833, 236), (913, 440), (879, 656), (733, 838), (504, 873), (224, 772), (142, 565), (198, 308), (422, 151), (759, 106)]
    # #
    # obs_1.reverse()
    # #
    # dcel = DCEL()
    # ID = dcel.create_face(bc, [obs_1])
    # #
    
    draw_face(screen, dcel, ID)
    
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
    
    # # active_edges = deque()
    # # active_edges.append(get_adj_pred(pts[0]))
    # # active_edges.append(get_adj_succ(pts[0]))
    get_rank = lambda v: v.rank
    is_active = lambda rank, e: min(get_rank(e.get_source_vertex()), get_rank(get_adj_succ(e))) <= rank and max(get_rank(e.get_source_vertex()), get_rank(get_adj_succ(e))) >= rank
    norm = lambda cv: cv / abs(cv)
    tang = lambda ang: ang * np.exp(1j * np.pi / 2)
    atang = lambda ang: ang * np.exp(1j * -np.pi / 2)
    added_ranks = 0
    angles = [np.pi / 2, -np.pi / 2]
    for p in range(len(pts)):
      added_ranks = get_rank(pts[p])
      nxt = get_adj_succ(pts[p])
      prev = get_adj_pred(pts[p])
      pt = pts[p]
  
      p1 = cart2complex(v2pt(prev), v2pt(pt))
      p2 = cart2complex(v2pt(nxt), v2pt(pt))

      bounds = [norm(atang(p1)), norm(tang(p2))]
      delta = np.mean(bounds)
      
      x,y = complex2cart(delta, v2pt(pt))
  
      pafn.frame_draw_dot(screen,[x[0],y[0]],pafn.colors["red"])

      a = np.exp(1j * angles[0])
      D = np.dot(np.exp(1j*angles[0]),delta)
      for i in range(len(angles)):
        a = np.exp(1j * angles[i])
        if np.angle(delta / a) < 0 and np.angle(p1/ a ) > 0:
          pafn.frame_draw_line(screen, (v2pt(pt), mfn.pol2car(v2pt(pt), 100, angles[i])), pafn.colors["tangerine"])
        if np.angle(delta / a) > 0 and np.angle(p2 / a) < 0:
          pafn.frame_draw_line(screen, (v2pt(pt), mfn.pol2car(v2pt(pt), 100, angles[i])), pafn.colors["green"])

        
      pygame.display.update()
      time.sleep(0.5)

  
    time.sleep(5)
        

if __name__ == '__main__':
    main()
        