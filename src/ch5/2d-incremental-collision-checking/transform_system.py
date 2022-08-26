#!/usr/bin/python3
from transform_polygon import *
from pygame_rendering.render_support import *
from polygon_debugging import *

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
  step_dist = r / some_constant
  x_step = step_dist * np.cos(theta)
  y_step = step_dist * np.sin(theta)
  return (x_step, y_step, some_constant)

def gradually_translate_system(OPList, P_index, t, screen = None, some_constant = 100):
  rx,ry, const = get_step_translation_function(OPList[P_index], t, some_constant)
  for step in range(int(const)):
    translate_polygon(OPList[P_index], rx, ry)
    clear_frame(screen)
    for i in range(len(OPList)):
      sanity_check_polygon(screen, OPList[i])