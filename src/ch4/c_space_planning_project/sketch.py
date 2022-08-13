#!/usr/bin/python3
import numpy as np
from half_plane import *

class HalfPlane:
  def __init__(self, line = Line()):
    self.line = line
  
  def test_point(self, pt = (0, 0)):
    # get vector from from ray origin to target point
    ox, oy = self.line.get_origin()
    tx, ty = pt
    delta_x, delta_y = tx - ox, ty - oy
    theta_1 = np.arctan2(delta_y, delta_x)
    
    # adjust theta to be nonnegative
    if theta_1 < 0:
      theta_1 = 2 * np.pi - abs(theta_1)
    
    #original slope of half plane
    rad_theta = self.line.get_rad_angle()
    # calculate adjusted ray slope, theta_0
    # and opposite ray slope theta_0_prime
    theta_0 = rad_theta
    theta_0_prime = 0

    if theta_0 < 0:
      theta_0_prime = np.pi + theta_0
      theta_0 = 2 * np.pi - abs(theta_0)
    elif theta_0 > 0:
      theta_0_prime = theta_0 + np.pi
    else:
      print("why is theta_0 == 0?")
    
    f = 0
    if rad_theta > 0: # implies arrow is pointing up
      if theta_1 < theta_0 or theta_1 > theta_0_prime:
        #outside_shape
        f = -1
      else:
        f = 1
        #inside_shape
    elif rad_theta > 0: # implies arrow is pointing down
      if theta_1 > theta_0_prime and theta_1 < theta_0:
        # outside shape
        f = -1
      else:
        f = 1
        #inside shape
    else:
      print("why is rad_theta == 0")
    
    return f
    
def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def rotate_edge_vector(origin, edge_vector, rotation_matrix):
  ox,oy = origin.get_point()
  ev_x,ev_y = edge_vector.get_origin()
  step = np.matmul(rotation_matrix, np.array([[ev_x - ox], [ev_y - oy]]))
  edge_vector.origin = Point(step[0][0] + ox, step[0][1] + oy)
  edge_vector.rad_angle = edge_vector.rad_angle + target_rad


def rotate_polygon(polygon, target_point):
  base_line = polygon.get_base_line()
  # ox,oy = base_line.get_origin()
  target_rad = base_line.compute_rotation_rad(target_point)
  r_theta = get_cc_rotation_matrix(target_rad)
  el = polygon.get_edge_list()
  for i in range(len(el)):
    l = el[i].H.line
    rotate_edge_vector(l.origin,el[i].H.line,r_theta)
    el[i].H.line.rad_angle = el[i].H.line.rad_angle + target_rad
  

  


