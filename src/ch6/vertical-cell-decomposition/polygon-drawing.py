#!/usr/bin/python3
import pygame
import sys
sys.path.append("./support")
#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import time
import sys
import numpy as np
from Polygon import *
from polygon_debugging import *
LALT = 256
LSHIFT = 1

def shape_draw(screen, A=None):
  pts = []
  polygons = []
  # polygons = [A]
  colors = []
  for i in pafn.colors:
    colors.append(pafn.colors[i])
  # colors = [pafn.colors["magenta"], pafn.colors["cyan"], pafn.colors["white"]]
  while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          if pygame.key.get_mods() == LALT:
            polygons.append(Polygon(pts))
            polygons[-1].color = colors[len(polygons)]
            pts = []
            pafn.clear_frame(screen)
            for p in polygons:
              sanity_check_polygon(screen, p)
            pygame.display.update()
          elif pygame.key.get_mods() == LSHIFT:
            for p in polygons:
              print(p.dump_points())
            sys.exit()
          else:
            pts.append(pygame.mouse.get_pos())
            pafn.frame_draw_dot(screen, pts[-1], pafn.colors["green"])
            pygame.display.update()

def adjust_angle(theta):
  """
  adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
  """
  if theta > np.pi:
      theta = theta + -2 * np.pi
  elif theta < -np.pi:
      theta = theta + 2 * np.pi

  return theta

def get_polygons():
  rhombus = Polygon([(800.0, 400.0), (706.8251437630926, 747.7332974640647), (306.82514376309257, 747.7332974640647), (400.0, 400.00000000000006)])
  rhombus.color = pafn.colors["red"]
  shape_1 = Polygon([(521, 590), (561, 697), (445, 646), (428, 497), (596, 442)], -1)
  shape_1.color = pafn.colors["green"]
  shape_2 = Polygon([(568, 563), (661, 499), (682, 652), (600, 673), (623, 608)], -1)
  shape_2.color = pafn.colors["cyan"]
  shapes = [rhombus, shape_1, shape_2]
  return shapes

def draw_rays(screen, A):
  pts = A.dump_points()
  for i in range(1, len(pts)):
    pafn.frame_draw_ray(screen, pts[i - 1], pts[i], A.color)
    # theta, r = mfn.car2pol(pts[i - 1], pts[i])
  pafn.frame_draw_ray(screen, pts[-1], pts[0], A.color)

def get_normals(v):
  he_prev = v._half_edge._prev
  he_next = v._half_edge._next
  prev_pt = he_prev.source_vertex.get_point_coordinate()
  next_pt = he_next.source_vertex.get_point_coordinate()
  prev_theta, prev_dist = mfn.car2pol(prev_pt, v.get_point_coordinate())
  next_theta, next_dist = mfn.car2pol(v.get_point_coordinate(), next_pt)
  # norm_angle = v._half_edge._bounded_face.norm_direction * -np.pi / 2
  return (adjust_angle(prev_theta + np.pi/2), adjust_angle(next_theta + np.pi/2))

def get_reversed_normals(v):
  he_prev = v._half_edge._next
  he_next = v._half_edge._prev
  prev_pt = he_prev.source_vertex.get_point_coordinate()
  next_pt = he_next.source_vertex.get_point_coordinate()
  prev_theta, prev_dist = mfn.car2pol(prev_pt, v.get_point_coordinate())
  next_theta, next_dist = mfn.car2pol(v.get_point_coordinate(), next_pt)
  return (adjust_angle(prev_theta - np.pi / 2), adjust_angle(next_theta - np.pi / 2))

def get_quadrant(angle):
  # if angle == -np.pi:
  #   angle = np.pi
  if 0 <= angle and angle < (np.pi / 2):
    return 1
  if np.pi / 2 <= angle and angle < np.pi:
    return 2
  if -np.pi < angle and angle <= -np.pi / 2:
    return 3
  if -np.pi / 2 < angle and angle <= 0:
    return 4

def get_ray_angles(norms):
  prev_norm, next_norm = norms
  pq = get_quadrant(prev_norm)
  nq = get_quadrant(next_norm)
  angles = []
  if pq == nq:
    if pq == 1 or pq == 2:
      angles.append(np.pi/2)
    else:
      angles.append(-np.pi / 2)
  elif pq == 1 and nq == 4 or pq == 3 and nq == 2 or abs(pq - nq) == 2:
    # print(f"{pq},{nq}: {prev_norm},{next_norm}")
    angles.append(np.pi / 2)
    angles.append(-np.pi / 2)
  elif pq == 1 and nq == 2 or pq == 2 and nq == 1:
    angles.append(np.pi / 2)
  elif pq == 3 and nq == 4 or pq == 4 and nq == 3:
    angles.append(-np.pi / 2)
  

  
  return angles


  
def main():

    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    shape_draw(screen)
    sys.exit()
    
    # sortkey = lambda v: v.get_point_coordinate()[0]
    # s = get_polygons()
    # vlist = []
    # for p in s:
    #   # sanity_check_polygon(screen, p)
    #   vl = p.dump_vertices()
    #   for i in range(len(vl)):
    #     vlist.append(vl[i])
      
    #   # draw_rays(screen, p)
    # vlist = sorted(vlist, key=sortkey)
    # for p in s:
    #   sanity_check_polygon(screen, p)
    # pygame.display.update()
    # for v in vlist:
    #   angles = get_ray_angles(get_normals(v))
    #   print(v.get_point_coordinate(), end = "\t")
    #   print(angles)
      
    #   # reversed_angles = get_ray_angles(get_reversed_normals(v))
    #   # get_midpoints()
    #   pafn.frame_draw_dot(screen, v.get_point_coordinate(), pafn.colors["indigo"])
    #   pafn.frame_draw_line(screen, [v.get_point_coordinate(), v._half_edge._next.source_vertex.get_point_coordinate()], pafn.colors["white"])
    #   pafn.frame_draw_ray(screen, v.get_point_coordinate(), v._half_edge._next.source_vertex.get_point_coordinate(), pafn.colors["white"])
    #   pts = []
    #   for a in angles:
    #     # pts.append
    #     pts.append((v,a)):
    # edges = []
    # for p in s:
    #   edges.append(p.get_front_edge())
    
    # for p in pts:
    #   queue = []
    #   for front_edge in edges:
    #     hold = front_edge
    #     next_edge = hold._next
    #     while next_edge != hold:
    #       theta_1, r1 = mfn.car2pol(p[0], next_edge.source_vertex.get_point_coordinate())
    #       theta_2, r2 = mfn.car2pol(p[0], next_edge._next.source_vertex.get_point_coordinate())
    #       if theta_1 < 0:
    #         theta_1 = 2 * np.pi + theta_1
    #       if theta_2 < 0:
    #         theta_2 = 2 * np.pi + theta_2
    #       if min(theta_1, theta_2) < p[1] and max(theta_1, theta_2) > p[1]:
    #         queue.append(next_edge)
    #       next_edge = next_edge._next
        

    #       if theta_1 < p[1] and theta_2 > p[1] or -1 * theta_2 < p[1] and theta_1
          
    #       if theta_1 

    #   for pt in pts:
    #     pafn.frame_draw_line(screen, (v.get_point_coordinate(), pt), pafn.colors["silver"])
    #     # pt2 = mfn.pol2car(v.get_point_coordinate(), 300, np.pi / 2)
    #   # ll = gfn.lerp_list(pt1, pt2, 30)
    #   # for pt in ll:
    #     # pafn.frame_draw_dot(screen, pt, pafn.colors["red"])

    #   pygame.display.update()
    #   time.sleep(1)

    
    # time.sleep(5)
    # sys.exit()
    
    # # pygame.display.update()
    # # shape_draw(screen, A)
    # # time.sleep(3)
    # # sequence_test(screen, pl)
    # # sequence_with_goal_test(screen, pl)

if __name__ == '__main__':
  main()