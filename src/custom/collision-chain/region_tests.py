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

# determines whether a point is within either of the adjacent regions
def t_in_adj_e_vor(E, t):
  '''
  Determines whether point t is in one of two neighboring edge regions
  Equivalently determines whether t is in voronoi region of their shared vertex
  '''
  pE = t_in_vor_edge(E._prev, t)
  nE = t_in_vor_edge(E, t)
  if pE < 0 and nE < 0:
    return True
  return False


def t_in_V_region(V, t):
  '''
  Determines whether t is in voronoi region of V
  '''
  E = V._half_edge
  pt1 = V.get_point_coordinate()
  pt2 = E._next.source_vertex.get_point_coordinate()
  ub = get_unit_norm_angle(pt1,pt2)
  pt3 = E._prev.source_vertex.get_point_coordinate()
  lb = get_unit_norm_angle(pt3,pt1)
  tb = get_ray_angle(pt1, t)
  if ub < 0:
    ub = 2 * np.pi + ub
    if lb < 0:
      lb = 2 * np.pi + lb
    if tb < 0:
      tb = 2 * np.pi + tb
  return (lb < tb and tb < ub)

def t_in_overlapping_edges(E, t):
  '''
  Determines whether a point is a member of two overlapping half planes
  '''
  pt1 = E.source_vertex.get_point_coordinate()
  pt2 = E._next.source_vertex.get_point_coordinate()
  pt3 = E._prev.source_vertex.get_point_coordinate()
  # print(f"pt1:{pt1}\npt2:{pt2}\npt3:{pt3}\nt:{t}")
  H_prev_31 = check_half_plane(pt3, pt1, t)
  H_next_12 = check_half_plane(pt1, pt2, t)
  return H_next_12 or H_prev_31

def check_half_plane(a,b ,t):
  '''
  Determines whether point t is a member of the half plane, as an angle
  offset from the vector normal to the segment ab
  '''
  lead = get_ray_angle(a, b)
  target = get_ray_angle(a, t)
  
  if lead < 0:
    lead = 2 * np.pi + lead
    if target < 0:
      target = 2 * np.pi + target
  
  trail = lead - np.pi
  return (trail < target and target < lead)
  
def t_in_E_region(E, t):
  '''
  Wrapper function
  Determines whether t is in voronoi region of E
  '''
  if t_in_vor_edge(E, t) > 0:
    return True
  return False

def t_in_vor_edge(half_edge, t, screen = None):
  '''
  Determines whether t is in voronoi region of E
  '''
  a = half_edge.source_vertex.get_point_coordinate()
  b = half_edge._next.source_vertex.get_point_coordinate()
  # print(f"edge {a} - {b} checking {t}...")
  r = distance_between_points(a, b)
  
  theta_ab = get_ray_angle(a, b)
  theta_ab_norm = get_unit_norm_angle(a, b)
  theta_at = get_ray_angle(a, t)
  
  # print(f"ab:\t{theta_ab}\nnorm:\t{theta_ab_norm}\nt:\t{theta_at}")
  if (screen != None):
    frame_draw_line(screen, [a,get_rectangular_coord(a, r, theta_ab)], colors["red"])
    frame_draw_line(screen,[a, get_rectangular_coord(a, r, theta_ab_norm)], colors["yellow"])
    pygame.display.update()
  
  if theta_ab < -np.pi / 2:
    # print("adjusting ab")
    theta_ab = 2 * np.pi + theta_ab
    if theta_at < 0:
      theta_at = 2 * np.pi + theta_at

  if not (theta_ab_norm <= theta_at):
    if (screen != None):
      frame_draw_line(screen, [a, t], colors["tangerine"])
    # print("outside ab_norm!")
    # print(f"norm: {theta_ab_norm} >= {theta_at}")
    # print(f"{t} is out of region by angle test.")
    return -1
  if not (theta_at <= theta_ab):
    if (screen != None):
      frame_draw_line(screen, [a, t], colors["tangerine"])
    # print("outside ab!")
    # print(f"{theta_ab} <= {theta_at}")
    # print(f"{t} is out of region by angle test.")
    return -2
  
  theta_E = abs(theta_ab - theta_at)
  rho_at = distance_between_points(a, t)
  h_max = r / np.cos(theta_E)
  
  if (rho_at < h_max):
    # print(f"{t} is in vor(E)")
    if (screen != None):
      frame_draw_line(screen, [a, t], colors["green"])
    return 1
  if (screen != None):
    frame_draw_line(screen, [a, t], colors["indigo"])
  # print(f"{t} is out of region due to maximum hypotenuse_test.")
  return -3
