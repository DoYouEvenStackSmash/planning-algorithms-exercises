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

def build_polygon(filename):
  # print(f"building polygon from")
  pts = load_point_set(filename)
  if not len(pts):
    print("no polygon can be built.")
    return None
  P = Polygon(pts)
  return P

def sanity_check_polygon(screen, P):
  draw_lines_between_points(screen, P.dump_points(), P.color)
  pygame.display.update()

def sanity_check_edge(screen, edge):
  he_curr = edge
  
  p1 = he_curr.source_vertex.get_point_coordinate()
  p2 = he_curr._next.source_vertex.get_point_coordinate()
  frame_draw_line(screen,[p1,p2],colors["white"])
  frame_draw_dot(screen,p1,colors["white"])
  frame_draw_dot(screen,p2,colors["indigo"])
  pygame.display.update()

def voronoi_prep(P):
  env = []
  load_edge_normal_vectors(P.get_front_edge(),env)
  print(env[0][0])
  return env

def t_in_vor_edge(edge, t, screen = None):
  

  a = edge.source_vertex.get_point_coordinate()
  b = edge._next.source_vertex.get_point_coordinate()
  
  r = distance_between_points(a, b)
  
  theta_ab = get_ray_angle(a, b)
  theta_ab_norm = get_unit_norm_angle(a, b)
  theta_at = get_ray_angle(a, t)
  
  print(f"ab:\t{theta_ab}\nnorm:\t{theta_ab_norm}\nt:\t{theta_at}")
  if (screen != None):
    frame_draw_line(screen, [a,get_rectangular_coord(a, r, theta_ab)], colors["red"])
    frame_draw_line(screen,[a, get_rectangular_coord(a, r, theta_ab_norm)], colors["yellow"])
    pygame.display.update()
  
  if theta_ab < -np.pi / 2:
    print("adjusting ab")
    theta_ab = 2 * np.pi + theta_ab
    if theta_at < 0:
      theta_at = 2 * np.pi + theta_at

  if not (theta_ab_norm <= theta_at):
    if (screen != None):
      frame_draw_line(screen, [a, t], colors["tangerine"])
    print("outside ab_norm!")
    print(f"norm: {theta_ab_norm} >= {theta_at}")
    print(f"{t} is out of region by angle test.")
    return -1
  if not (theta_at <= theta_ab):
    if (screen != None):
      frame_draw_line(screen, [a, t], colors["tangerine"])
    print("outside ab!")
    print(f"{theta_ab} <= {theta_at}")
    print(f"{t} is out of region by angle test.")
    return -2
  
  theta_E = abs(theta_ab - theta_at)
  rho_at = distance_between_points(a, t)
  h_max = r / np.cos(theta_E)
  
  if (rho_at < h_max):
    print(f"{t} is in vor(E)")
    if (screen != None):
      frame_draw_line(screen, [a, t], colors["green"])
    return 1
  if (screen != None):
    frame_draw_line(screen, [a, t], colors["indigo"])
  print(f"{t} is out of region due to maximum hypotenuse_test.")
  return -3

def find_contact(star_list, screen):
  I1 = 0
  I2 = 0
  NO_MATCH = True
  while star_list[I2][1]._bounded_face == star_list[I1][1]._bounded_face and I2 < len(star_list):
    I2+=1
  # assume that we have found the first edge in other polygon
  T_OOB_HYPOTENUSE = -3
  T_OOB_NORM = -1
  T_OOB_EDGE = -2
  T_IN_VOR_EDGE = 1
  END = False
  
  while I1 < len(star_list) and I2 < len(star_list):
    time.sleep(1)
    val = t_in_vor_edge(star_list[I1][1], star_list[I2][1].source_vertex.get_point_coordinate())

    if val == T_OOB_HYPOTENUSE:
      neighbor_edge = star_list[I1][1]._next
      neighbor_val = t_in_vor_edge(neighbor_edge, star_list[I2][1].source_vertex.get_point_coordinate(),screen)
      if neighbor_val == T_OOB_NORM:
        print("VV found!")
        VV_found(neighbor_edge.source_vertex, star_list[I2][1].source_vertex, screen)
        NO_MATCH = False
        # break
      elif neighbor_val == T_IN_VOR_EDGE:
        print("neigbor happens to have EV!")
        EV_found(neighbor_edge, star_list[I2][1].source_vertex, screen)
        NO_MATCH = False
        break
        # return
      elif neighbor_val == T_OOB_EDGE:
        print("nothing interesting found.")
      else:
        print("somehow val isn't what it should be?")
    elif val == T_IN_VOR_EDGE:
      print("EV found!")
      EV_found(star_list[I1][1], star_list[I2][1].source_vertex, screen)
      NO_MATCH = False
      break
      # return
    elif val == T_OOB_EDGE: # val = T_OOB_EDGE, which means it could be anywhere and we therefore don't care.
      print("nothing interesting found")
    elif val == T_OOB_NORM:
      neighbor_edge = star_list[I1][1]._prev
      neighbor_val = t_in_vor_edge(neighbor_edge, star_list[I2][1].source_vertex.get_point_coordinate(),screen)
      if neighbor_val == T_OOB_HYPOTENUSE:
        print("VV found!")
        VV_found(neighbor_edge.source_vertex, star_list[I2][1].source_vertex, screen)
        NO_MATCH = False
        # break
      elif neighbor_val == T_IN_VOR_EDGE:
        print("neigbor happens to have EV!")
        EV_found(neighbor_edge, star_list[I2][1].source_vertex, screen)
        NO_MATCH = False
        # break
        # return
      elif neighbor_val == T_OOB_EDGE:
        print("nothing interesting found.")
      else:

        print("somehow val isn't what it should be?")
    else:
      print("somehow val isn't what it should be?")
    
    mark_edge_clear(star_list[I1][1], screen)
    # mark_vertex_clear()
    e_hold = star_list[I1][1]._next
    while I1 < len(star_list) and star_list[I1][1] != e_hold:
      I1+=1
    
    # if I1 is at star list oob, we must wrap to 0 for the last edge
    if I1 == len(star_list):
      break
    # make sure I1 is always trailing
    #swap(I1, I2)
    if I1 > I2:
      temp = I1
      I1 = I2
      I2 = temp
    elif I1 == I2:
      print("not sure how this one happened.")
      
    # we can assume the next I1 has been found
    #goto next 
  if NO_MATCH:
    print("must be wrapped to beginning of unit circle")

def mark_vertex_clear(v, screen):
  frame_draw_dot(screen, v.get_point_coordinates(), colors["tangerine"], 1)
  pygame.display.update()

def mark_edge_clear(edge, screen):
  e_p1 = edge.source_vertex.get_point_coordinate()
  e_p2 = edge._next.source_vertex.get_point_coordinate()
  frame_draw_line(screen, [e_p1, e_p2], colors["tangerine"])
  pygame.display.update()

def VV_found(v1,v2, screen):
  p1 = v1.get_point_coordinate()
  p2 = v2.get_point_coordinate()
  frame_draw_bold_line(screen,[p1,p2], colors["magenta"])
  pygame.display.update()

def EV_found(edge, v1, screen):
  e_p1 = edge.source_vertex.get_point_coordinate()
  e_p2 = edge._next.source_vertex.get_point_coordinate()
  l = get_unit_norm(e_p1,e_p2)
  e_mid = l.get_origin()
  v_p = v1.get_point_coordinate()
  frame_draw_bold_line(screen, [e_mid, v_p], colors["cyan"])
  pygame.display.update()
  



def pygame_half_planes_loop(screen,W):
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

def pygame_single_voronoi_loop(screen, edge):
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
        
        v_val = t_in_vor_edge(edge, p, screen)
        if v_val > 0:
          frame_draw_dot(screen, p, colors["green"])
        elif v_val < 0:
          frame_draw_dot(screen, p, colors["tangerine"], 2)
        else:
          print(f"{p} is unknown?")
        pygame.display.update()

def single_polygon_single_edge_voronoi():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  filename = sys.argv[1]
  A = build_polygon(filename)
  if not A:
    print(f"could not build polygon from {filename}")
    print("\nexiting...")
    sys.exit()
  A.color = colors["white"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, A)
  print(A.get_front_edge()._bounded_face)
  return
  s = A.dump_segments()
  W = World()
  W.create_half_plane(s[0][0],s[0][1])
  frame_draw_line(screen, s[0], colors["magenta"])
  edge_list = voronoi_prep(A)
  pygame.display.update()
  # sanity_check_edge(screen, edge_list[0][1])
  pygame_single_voronoi_loop(screen, edge_list[0][1])

def two_polygon_all_edge_voronoi():
  if len(sys.argv) < 3:
    print("provide two files")
    sys.exit()
  pygame.init()
  screen = create_display(1600,1000)
  # pygame_loop(screen)
  
  A,O = build_polygon(sys.argv[1]),build_polygon(sys.argv[2])
  if A == None or O == None:
    print("one of the regions is none.")
    sys.exit()

  A.color = colors["green"]
  O.color = colors["white"]
  sanity_check_polygon(screen, A)
  sanity_check_polygon(screen, O)
  sl = build_star(A.get_front_edge(), O.get_front_edge())
  find_contact(sl, screen)
  pygame_loop(screen)
  
  
def main():
  # single_polygon_single_edge_voronoi()
  two_polygon_all_edge_voronoi()

  # pygame_half_planes_loop(screen,W)
  # pygame_loop(screen)

main()
  

