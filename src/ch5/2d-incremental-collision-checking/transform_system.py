#!/usr/bin/python3
from transform_polygon import *
from pygame_rendering.render_support import *
from polygon_debugging import *
from voronoi_regions import *

def get_step_rotation_matrix(P, t):
  rad_theta = compute_rotation(P.get_front_edge(), t)
  deg = abs(rad_theta * 180 / np.pi)
  step_rad = rad_theta / deg
  r_mat = get_cc_rotation_matrix(step_rad)
  return deg,r_mat

def gradually_rotate_system(OPList, P_index, t, screen = None):
  steps, r_mat = get_step_rotation_matrix(OPList[P_index], t)
  for step in range(int(steps)):
    rotate_polygon(OPList[P_index], r_mat)
    clear_frame(screen)
    for i in range(len(OPList)):
      sanity_check_polygon(screen, OPList[i])
    
def get_step_translation_function(P, t, some_constant = 100):
  h = P.get_front_edge()
  r,theta = get_polar_coord(h.source_vertex.get_point_coordinate(), t)
  if r < 100:
    some_constant = 30
  step_dist = r / some_constant
  x_step = step_dist * np.cos(theta)
  y_step = step_dist * np.sin(theta)
  val = (x_step, y_step, some_constant)
  return val

def gradually_translate_system(OPList, P_index, t, screen = None, some_constant = 100):
  rx,ry, const = get_step_translation_function(OPList[P_index], t, some_constant)
  for step in range(int(const)):
    translate_polygon(OPList[P_index], rx, ry)
    clear_frame(screen)
    for i in range(len(OPList)):
      sanity_check_polygon(screen, OPList[i])

def gradually_rotate_voronoi_system(A, O, t, screen = None):
  steps, r_mat = get_step_rotation_matrix(A, t)
  for step in range(int(steps)):
    rotate_polygon(A, r_mat)
    clear_frame(screen)
    find_contact(build_star(A.get_front_edge(), O.get_front_edge()), screen)
    sanity_check_polygon(screen, A)
    sanity_check_polygon(screen, O)
    time.sleep(0.01)

def gradually_translate_voronoi_system(A, O, t, screen = None, some_constant = 100):
  rx,ry, const = get_step_translation_function(A, t, some_constant)
  print(f"here: {rx}, {ry}, {const}")
  thres = np.divide(1,123456789)
  if abs(rx) < thres or abs(rx) < thres:
    return
  for step in range(int(const)):
    # print(f"here: {rx}, {ry}")
    
    translate_polygon(A, rx, ry)
    clear_frame(screen)
    find_contact(build_star(A.get_front_edge(), O.get_front_edge()), screen)
    sanity_check_polygon(screen, A)
    sanity_check_polygon(screen, O)
    time.sleep(0.01)