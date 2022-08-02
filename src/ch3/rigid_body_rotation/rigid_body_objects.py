#!/usr/bin/python3

import numpy as np

class line:
  def __init__(self, origin = [0,0], r = 1, rad_angle = 0):
    self.origin = origin
    self.r = r
    self.rad_angle = rad_angle
    self.x_off_t = origin[0]
    self.y_off_t = origin[1]
  
  def get_point(self):
    x_o = self.x_off_t
    y_o = self.y_off_t
    x = np.cos(self.rad_angle) * self.r
    y = np.sin(self.rad_angle) * self.r
    return (x + x_o, y + y_o)

  def get_rad_angle(self):
    return self.rad_angle
  
  def get_x_off_t(self):
    return self.x_off_t
  
  def get_y_off_t(self):
    return self.y_off_t
  
  def set_rad_angle(self, rad_angle):
    self.rad_angle = rad_angle
  
  

class RigidBody:
  def __init__(self, origin, point_set):
    self.origin = origin
    self.x_axis = line(origin)
    self.point_set = point_set

  def set_x_axis(self, x_axis_rad):
    self.x_axis.rad_angle = x_axis_rad
  
  def set_point_set(self, point_set):
    self.point_set = point_set
  
  def get_point_set(self):
    return self.point_set
  
  def get_x_axis(self):
    return self.x_axis
  
