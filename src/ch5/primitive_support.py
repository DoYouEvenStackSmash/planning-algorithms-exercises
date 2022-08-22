#!/usr/bin/python3

import numpy as np

class Point:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y
  
  def get_point(self):
    return (self.x, self.y)
  
  def dump(self):
    return f"{self.get_point()}"

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

  def compute_rotation_rad(self, target_point):
    tx, ty = target_point
    ox, oy = self.get_origin()

    base_rad = self.get_rad_angle()
    target_rad = np.arctan2((ty - oy), (tx - ox))
    rotation = target_rad - base_rad
    if rotation > np.pi:
      rotation = rotation - (2 * np.pi)
    if rotation < -np.pi:
      rotation = rotation + (2 * np.pi)
    
    return rotation
