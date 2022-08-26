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
import time

def build_polygon(filename):
  # print(f"building polygon from")
  pts = load_point_set(filename)
  if not len(pts):
    print("no polygon can be built.")
    return None
  P = Polygon(pts)
  return P


def voronoi_prep(P):
  env = []
  load_edge_normal_vectors(P.get_front_edge(),env)
  print(env[0][0])
  return env

  

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


def pygame_edge_region_loop(screen, P):
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
          find_edge_region(P, p, screen)
        else:
          print(p)
    
def pygame_find_all_region_loop(screen, P):
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
          find_all_region(P, p, screen)
        else:
          print(p)
    
def pygame_two_region_loop(screen, A, O):
  lalt = 256
  lshift = 1
  ctrl = 64
  PL = [A, O]
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        print(p)
        if pygame.key.get_mods() == lalt:
          clear_frame(screen)
          for i in PL:
            sanity_check_polygon(screen, i)
        elif pygame.key.get_mods() == ctrl:
          for i in PL:
            # find_vertex_region(i, p, screen)
            find_all_region(i, p, screen)
        else:
          print(p)
        # if v_val > 0:
        #   frame_draw_dot(screen, p, colors["green"])
        # elif v_val < 0:
        #   frame_draw_dot(screen, p, colors["tangerine"], 2)
        # else:
        #   print(f"{p} is unknown?")
        pygame.display.update()

def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def compute_rotation(h, target_point):
  pt1 = h.source_vertex.get_point_coordinate()
  pt2 = h._next.source_vertex.get_point_coordinate()
  base_rad = get_ray_angle(pt1, pt2)
  target_rad = get_ray_angle(pt1, target_point)
  # tx,ty = target_point
  
  rotation = target_rad - base_rad
  if rotation > np.pi:
    rotation = rotation - (2 * np.pi)
  if rotation < -np.pi:
    rotation = rotation + (2 * np.pi)
  return rotation
  
def gradually_rotate_polygon(P, target_point, step_size = 1):
  h = P.get_front_edge()
  rad_theta = compute_rotation(h, target_point)
  step_theta = rad_theta / step_size
  r_mat = get_cc_rotation_matrix(step_theta)
  rotate_polygon(P, r_mat)

def rotate_point(rotation_matrix, origin, point):
  ox,oy = origin
  px,py = point
  step = np.matmul(rotation_matrix, np.array([[px - ox], [py - oy]]))
  return [step[0][0] + ox, step[1][0] + oy]

def rotate_polygon(P, rotation_matrix):
  h = P.get_front_edge()
  o = h.source_vertex.get_point_coordinate()
  h = h._next
  while h != P.get_front_edge():
    h.source_vertex.point_coordinate = rotate_point(rotation_matrix, o, h.source_vertex.get_point_coordinate())
    h = h._next

def rotate_voronoi(A, O, p, screen):
  gradually_rotate_polygon(A, p)
  sl = build_star(A.get_front_edge(), O.get_front_edge())
  find_contact(sl, screen)

'''
  CTRL: Given a polygon P, draws a line from at most one vertex region of P to a
        a mouse-click target point.
  LALT: Clears the frame and redraws the polygon
'''
def pygame_region_loop(screen, P):
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
          find_vertex_region(P, p, screen)
        else:
          print(p)
        pygame.display.update()

def pygame_voronoi_loop(screen, A, O):
  lalt=256
  ctrl = 64
  pl = [A, O]
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        # print(p)
        if pygame.key.get_mods() == ctrl:
          clear_frame(screen)
          rotate_voronoi(A, O, p, screen)
          for i in pl:
            sanity_check_polygon(screen, i)
        elif pygame.key.get_mods() == lalt:
          clear_frame(screen)
          rotate_voronoi(O, A, p, screen)
          for i in pl:
            sanity_check_polygon(screen, i)
        else:
          print(p)
        # elif pygame.key.get_mods() == lalt:
          # clear_frame(screen)  
        # else:
          # find_all_region(P, p, screen)
        print(p)

def pygame_rotation_loop(screen, P):
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
        if pygame.key.get_mods() == ctrl:
          gradually_rotate_polygon(P, p)
        elif pygame.key.get_mods() == lalt:
          clear_frame(screen)  
        else:
          find_all_region(P, p, screen)
          print(p)
        sanity_check_polygon(screen, P)

def single_polygon_mod():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  filename = sys.argv[1]
  A = build_polygon(filename)
  A.color = colors["white"]
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, A)
  pygame_rotation_loop(screen, A)

def single_polygon_locate_edge():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  filename = sys.argv[1]
  A = build_polygon(filename)
  A.color = colors["white"]
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, A)
  # pygame_region_loop(screen, A)
  # pygame_edge_region_loop(screen, A)
  pygame_find_all_region_loop(screen, A)

def double_polygon_mod():
  if len(sys.argv) < 3:
    print("provide two files")
    sys.exit()
  A,O = build_polygon(sys.argv[1]),build_polygon(sys.argv[2])
  if A == None or O == None:
    print("one of the regions is none.")
    sys.exit()
  A.color = colors["green"]
  O.color = colors["white"]
  
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  O.v_color = colors["yellow"]
  O.e_color = colors["red"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, O)
  sanity_check_polygon(screen, A)
  pygame_voronoi_loop(screen, A, O)

def double_polygon_locate_edge():
  if len(sys.argv) < 3:
    print("provide two files")
    sys.exit()
  A,O = build_polygon(sys.argv[1]),build_polygon(sys.argv[2])
  if A == None or O == None:
    print("one of the regions is none.")
    sys.exit()
  A.color = colors["green"]
  O.color = colors["white"]
  
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  O.v_color = colors["yellow"]
  O.e_color = colors["red"]
  pygame.init()
  screen = create_display(1000,1000)
  sanity_check_polygon(screen, O)
  sanity_check_polygon(screen, A)
  pygame_two_region_loop(screen, A, O)


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
  
  A.v_color = colors["cyan"]
  A.e_color = colors["tangerine"]
  O.v_color = colors["yellow"]
  O.e_color = colors["red"]
  sanity_check_polygon(screen, A)
  # for i in A.dump_segments():
  #   print(i)
  sanity_check_polygon(screen, O)
  sl = build_star(A.get_front_edge(), O.get_front_edge())
  find_contact(sl, screen)
  pygame_loop(screen)
  
  
def main():
  double_polygon_mod()
  # single_polygon_mod()
  # single_polygon_locate_edge()
  # double_polygon_locate_edge()
  # single_polygon_single_edge_voronoi()
  # two_polygon_all_edge_voronoi()

  # pygame_half_planes_loop(screen,W)
  # pygame_loop(screen)

main()
  

