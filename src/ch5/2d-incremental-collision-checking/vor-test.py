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
  

