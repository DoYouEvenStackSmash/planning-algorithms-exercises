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
    


  