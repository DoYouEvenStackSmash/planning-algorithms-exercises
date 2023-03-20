#!/usr/bin/python3
from transform_polygon import *
from pygame_rendering.render_support import PygameArtFxns as pafn
from pygame_rendering.render_support import GeometryFxns as gfn
from pygame_rendering.render_support import MathFxns
from pygame_rendering.render_support import TransformFxns as tfn
from polygon_debugging import *
from voronoi_regions import *
# VERBOSE = False
SLEEP_CONSTANT = 0.0001
COLLISION_THRESHOLD = np.divide(1,123456789)

def get_step_rotation_matrix(P, t):
  '''
  Derives incremental rotation matrix for a polygon to reach a target orientation
  using representative edge and a target point.
  Returns a step size in radians, and a 2x2 rotation matrix
  '''
  rad_theta = compute_rotation(P.get_front_edge(), t)
  deg = abs(rad_theta * 180 / np.pi)
  step_rad = rad_theta / deg
  r_mat = get_cc_rotation_matrix(step_rad)
  return deg,r_mat

def gradually_rotate_system(OPList, P_index, t, screen = None):
  '''
  Gradually rotates a system of polygons by repeatedly applying rotations to each
  Does not return
  '''
  steps, r_mat = get_step_rotation_matrix(OPList[P_index], t)
  for step in range(int(steps)):
    pafn.clear_frame(screen)
    rotate_polygon(OPList[P_index], r_mat)
    for i in range(len(OPList)):
      sanity_check_polygon(screen, OPList[i])
    pygame.display.update()
    
def get_step_translation_function(P, t, some_constant = 100):
  '''
  Derives incremental displacement for a polygon to reach a target point
  in some number of steps
  Returns a tuple containing displacement for x,y, and a constant
  '''
  h = P.get_front_edge()
  r,theta = get_polar_coord(h.source_vertex.get_point_coordinate(), t)
  # print(f"radius: {r}")
  if r < 100:
    # print("correcting")
    some_constant = 30
  step_dist = r / some_constant
  x_step = step_dist * np.cos(theta)
  y_step = step_dist * np.sin(theta)
  val = (x_step, y_step, some_constant)
  return val

def gradually_translate_system(OPList, P_index, t, screen = None, some_constant = 100):
  '''
  Gradually translates a system of polygons by repeatedly applying displacement to each
  Does not return
  '''
  rx,ry, const = get_step_translation_function(OPList[P_index], t, some_constant)
  for step in range(int(const)):
    pafn.clear_frame(screen)
    translate_polygon(OPList[P_index], rx, ry)
    for i in range(len(OPList)):
      sanity_check_polygon(screen, OPList[i])
    pygame.display.update()

def gradually_rotate_voronoi_system(A, Olist, t, screen = None, path_line = [], VERBOSE=False):
  '''
  Gradually transforms a polygon A, maintaining a connection between closest pair of points
  (x1,y1),(x2,y2) where x1,y1 is in A and x2,y2 is in O
  Does not return
  '''
  steps, r_mat = get_step_rotation_matrix(A, t)
  for step in range(int(steps)):
    pafn.clear_frame(screen)
    rotate_polygon(A, r_mat)
    for O in Olist:
      val = find_contact(build_star(A.get_front_edge(), O.get_front_edge()), screen, VERBOSE)
      sanity_check_polygon(screen, A)
      for Ox in Olist:
        sanity_check_polygon(screen, Ox)
      
      sanity_check_edge(screen,A.get_front_edge())
      if val < 5:
        pygame.display.update()
        return val
    for i in range(0,len(path_line), 4):
      pafn.frame_draw_dot(screen, path_line[i], pafn.colors["yellow"])
    pygame.display.update()
    time.sleep(SLEEP_CONSTANT)
  return 0

def gradually_translate_voronoi_system(A, Olist, t, screen = None, some_constant = 100, path_line = [], VERBOSE=False):
  '''
  Gradually transforms a polygon A, maintaining a connection between closest pair of points
  (x1,y1),(x2,y2) where x1,y1 is in A and x2,y2 is in O
  Does not return
  '''
  rx,ry, const = get_step_translation_function(A, t, some_constant)
  
  if abs(rx) < COLLISION_THRESHOLD or abs(ry) < COLLISION_THRESHOLD:
    return min(abs(rx), abs(ry))

  for step in range(int(const)):
    # print(f"here: {rx}, {ry}")
    pafn.clear_frame(screen)
    translate_polygon(A, rx, ry)
    for O in Olist:
      val = find_contact(build_star(A.get_front_edge(), O.get_front_edge()), screen, VERBOSE)
      sanity_check_polygon(screen, A)
      for Ox in Olist:
        sanity_check_polygon(screen, Ox)
      if val < 5:
        pygame.display.update()
        return val
    for i in range(0,len(path_line), 4):
      pafn.frame_draw_dot(screen, path_line[i], pafn.colors["yellow"])
    pygame.display.update()
    time.sleep(SLEEP_CONSTANT)
  return 0

def update_world(screen, A, Olist, pts, VERBOSE=False):
  '''
  Driver for updating the World space, and all objects therein
  Does not return
  '''
  
  pafn.clear_frame(screen)
  
  l1,l2,l3,m1,m2,mpts = gfn.cubic_lerp_calculate(pts)
  
  # lerp rendering
  for i in range(len(mpts)):
    pafn.clear_frame(screen)
    # render interpolated points up to i
    for j in range(i):
      pafn.frame_draw_dot(screen, mpts[j], pafn.colors["cyan"])
    
    # render lines if verbose
    if VERBOSE:
      pafn.frame_draw_line(screen, (pts[0],pts[1]), pafn.colors['red'])
      pafn.frame_draw_line(screen, (pts[1],pts[2]), pafn.colors['red'])
      pafn.frame_draw_line(screen, (pts[2],pts[3]), pafn.colors['red'])
      pafn.frame_draw_line(screen, (l1[i],l2[i]),pafn.colors["tangerine"])
      pafn.frame_draw_line(screen, (l2[i],l3[i]),pafn.colors["tangerine"])
      pafn.frame_draw_bold_line(screen, (m1[i],m2[i]),pafn.colors['green'])
    
    # render polygons
    sanity_check_polygon(screen, A)
    for O in Olist:
      sanity_check_polygon(screen, O)

    pygame.display.update()
    time.sleep(0.005)
  
  pts = []
  ptlist = mpts
  
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