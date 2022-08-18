#!/usr/bin/python3
import numpy as np
class Obj:
  def __init__(self, x_min, x_max, y_min, y_max):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.x_identify = None
    self.y_identify = None
    self.next_segment = None
    self.end_flag = False

  # def get_next_x(self, x_curr):
  def get_x_borders(self):
    return [(self.x_min, self.y_min), (self.x_max, self.y_min), (self.x_min, self.y_max), (self.x_max, self.y_max)]
  
  def get_y_borders(self):
    return [(self.x_min, self.y_min),(self.x_min,self.y_max), (self.x_max, self.y_min), (self.x_max, self.y_max)]

  def is_complete(self):
    return self.end_flag

  def get_y_min(self):
    return self.y_min
  
  def get_x_min(self):
    return self.x_min

  def get_y_max(self):
    return self.y_max
  
  def get_x_max(self):
    return self.x_max

  def check_y_max(self, y_curr):
    return y_curr >= self.y_max  
  
  def check_x_max(self, x_curr):
    return x_curr >= self.x_max
  
  def check_y_min(self, y_curr):
    return y_curr <= self.y_min  
  
  def check_x_min(self, x_curr):
    return x_curr <= self.x_min
  

# def flat_cylinder_end(O, x_curr, y_curr):
  

def flat_cylinder_x_identify(O, x):
  if O.check_x_max(x):
    return O.get_x_min()
  return x

def flat_cylinder_y_identify(O, y):
  return y

def flat_cylinder_next_segment(O, x_curr, y_curr, rad_angle):
  x_curr = O.x_identify(O, x_curr)
  y_curr = O.y_identify(O, y_curr)
  x_dist = O.get_x_max() - O.get_x_min()
  y_dist = np.multiply(x_dist, np.tan(rad_angle))
  y_end = y_curr + y_dist
  # if y_end is out of bounds...
  if O.check_y_max(y_end):
    y_excess = y_end - O.get_y_max()
    y_dist = y_dist - y_excess
    y_end = y_dist + y_curr # should equal y_max
    x_dist = np.divide(y_dist, np.tan(rad_angle))
    O.end_flag = True
  x_end = x_curr + x_dist
  
  return ((x_curr, y_curr), (x_end, y_end))
