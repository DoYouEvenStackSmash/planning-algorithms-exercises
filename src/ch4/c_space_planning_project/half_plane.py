#!/usr/bin/python3
import numpy as np

class Point:
  def __init__(self, x = 0, y = 0) -> None:
    self.x = x
    self.y = y
  
  def get_point(self):
    return (self.x,self.y)

class Line:
  def __init__(self, origin = Point(), length = 0, rad_angle = 0):
    self.origin = origin
    self.length = length
    self.rad_angle = rad_angle

  def get_endpoint(self):
    x_o, y_o = self.origin.get_point()
    r = self.length
    theta = self.rad_angle
    x_e = r * np.cos(theta)
    y_e = r * np.sin(theta)
    return (x_o + x_e, y_o + y_e)
  
  def get_origin(self):
    return self.origin.get_point()
  
  def get_segment(self):
    x_o, y_o = self.get_origin()
    x_e, y_e = self.get_endpoint()
    return ((x_o, y_o), (x_e, y_e))
  
  def get_length(self):
    return self.length

  def get_rad_angle(self):
    return self.rad_angle

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
      theta_0_prime = np.pi
      # print("why is theta_0 == 0?")
    
    f = 0
    if rad_theta > 0: # implies arrow is pointing up
      if theta_1 < theta_0 or theta_1 > theta_0_prime:
        #outside_shape
        f = -1
      else:
        f = 1
        #inside_shape
    elif rad_theta < 0: # implies arrow is pointing down
      if theta_1 > theta_0_prime and theta_1 < theta_0:
        # outside shape
        f = -1
      else:
        f = 1
        #inside shape
    else:
      if theta_1 > theta_0_prime:
        # outside shape
        f = -1
      else:
        f = 1
    
    return f
    

