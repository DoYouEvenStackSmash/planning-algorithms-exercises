#!/usr/bin/python3
from support.Polygon import *
from support.doubly_connected_edge_list import *
from support.unit_norms import *

import numpy as np

def get_cc_rotation_matrix(rad_theta):
  '''
  Get 2D rotation matrix for a given angle theta
  Returns a 2x2 matrix
  '''
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def compute_rotation(h, target_point):
  '''
  Compute angle of rotation between some origin point and a target
  Returns an angle in radians
  '''
  pt1 = h.source_vertex.get_point_coordinate()
  pt2 = h._next.source_vertex.get_point_coordinate()
  base_rad = get_ray_angle(pt1, pt2)
  target_rad = get_ray_angle(pt1, target_point)
  
  rotation = target_rad - base_rad
  if rotation > np.pi:
    rotation = rotation - (2 * np.pi)
  if rotation < -np.pi:
    rotation = rotation + (2 * np.pi)
  
  return rotation
  
def gradually_rotate_polygon(P, target_point, step_size = 1):
  '''
  Incremental rotation of a polygon
  Does not return
  '''
  h = P.get_front_edge()
  rad_theta = compute_rotation(h, target_point)
  step_theta = rad_theta / step_size
  r_mat = get_cc_rotation_matrix(step_theta)
  rotate_polygon(P, r_mat)
      

def rotate_point(rotation_matrix, origin, point):
  '''
  Rotates point about some fixed origin by applying rotation matrix
  Returns the transformed point
  '''
  ox,oy = origin
  px,py = point
  step = np.matmul(rotation_matrix, np.array([[px - ox], [py - oy]]))
  return [step[0][0] + ox, step[1][0] + oy]

def rotate_polygon(P, rotation_matrix):
  '''
  Transforms a polygon by applying rotation_matrix to each of its vertices
  Does not return
  '''
  h = P.get_front_edge()
  o = h.source_vertex.get_point_coordinate()
  h = h._next
  while h != P.get_front_edge():
    h.source_vertex.point_coordinate = rotate_point(rotation_matrix, o, h.source_vertex.get_point_coordinate())
    h = h._next

def gradually_translate_polygon(P, target_point, step_size = 1):
  '''
  Applies a gradual translation to a polygon by repeatedly applying small translations
  Does not return
  '''
  h = P.get_front_edge()
  r,theta = get_polar_coord(h.source_vertex.get_point_coordinate(), target_point)
  step_r = r / step_size
  x_step = step_r * np.cos(theta)
  y_step = step_r * np.sin(theta)
  for i in range(step_size):
    translate_polygon(P, x_step, y_step)

def translate_polygon(P, x_disp, y_disp):
  '''
  Transforms a polygon by applying a displacement to each of its vertices
  Does not return
  '''
  h = P.get_front_edge()
  px,py = h.source_vertex.get_point_coordinate()
  h.source_vertex.set_point_coordinate([px + x_disp, py + y_disp])
  h = h._next
  while h != P.get_front_edge():
    px,py = h.source_vertex.get_point_coordinate()
    h.source_vertex.set_point_coordinate([px + x_disp, py + y_disp])
    h = h._next
  
