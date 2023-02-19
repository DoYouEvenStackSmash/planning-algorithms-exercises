#!/usr/bin/python3
from transform_polygon import *
from pygame_rendering.render_support import *
from polygon_debugging import *
from voronoi_regions import *
SLEEP_CONSTANT = 0.003
COLLISION_THRESHOLD = np.divide(1,123456789)
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
  print(f"radius: {r}")
  if r < 100:
    print("correcting")
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

def gradually_rotate_voronoi_system(A, O, t, screen = None, path_line = []):
  steps, r_mat = get_step_rotation_matrix(A, t)
  for step in range(int(steps)):
    rotate_polygon(A, r_mat)
    clear_frame(screen)
    find_contact(build_star(A.get_front_edge(), O.get_front_edge()), screen)
    sanity_check_polygon(screen, A)
    sanity_check_polygon(screen, O)
    
    sanity_check_edge(screen,A.get_front_edge())
    for i in path_line[:2:]:
      frame_draw_dot(screen, i, colors["yellow"])
    pygame.display.update()
    time.sleep(SLEEP_CONSTANT)

def gradually_translate_voronoi_system(A, O, t, screen = None, some_constant = 100, path_line = []):
  rx,ry, const = get_step_translation_function(A, t, some_constant)
  print(f"here: {rx}, {ry}, {const}")
  
  if abs(rx) < COLLISION_THRESHOLD or abs(rx) < COLLISION_THRESHOLD:
    return
  for step in range(int(const)):
    # print(f"here: {rx}, {ry}")
    translate_polygon(A, rx, ry)
    clear_frame(screen)
    find_contact(build_star(A.get_front_edge(), O.get_front_edge()), screen)
    sanity_check_polygon(screen, A)
    sanity_check_polygon(screen, O)
    for i in path_line[:2:]:
      frame_draw_dot(screen, i, colors["yellow"])
    pygame.display.update()
    time.sleep(SLEEP_CONSTANT)