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
  def __init__(self, origin = Point(), end_pts = [Point(), Point()]):
    self.line_function = None
    self.origin = origin
    self.rad_angle = 0
    self.end_pts = end_pts
  
  def get_end_points(self):
    s,e = self.end_pts
    return (s.get_point(), e.get_point())
  
  # angle theta with respect to the origin
  # displacement with respect to the origin
  # this gives us a vector
  def get_rad_angle(self):
    return self.rad_angle

  def test_point(self, target_point):
    s,e = self.end_pts
    x1,y1 = s.get_point()
    x2,y2 = target_point
    target_theta = np.arctan2(y2 - y1, x2 - x1)
    real_theta = target_theta - self.rad_angle
    return real_theta

  def set_rad_angle(self):
    s,e = self.end_pts
    x1,y1 = s.get_point()
    x2,y2 = e.get_point()
    if x2 == x1:
      m = 0
    else:
      m = (y2 - y1) / (x2 - x1)

    y = m * 1 + 0

    # ox,oy = self.origin.get_point()

    theta = np.arctan2(y, 1)
    self.rad_angle = theta

  def calculate_test_function(self):
    s,e = self.end_pts
    x1,y1 = s.get_point()
    x2,y2 = e.get_point()
    if x2 == x1:
      m = 0
    else:
      m = (y2 - y1) / (x2 - x1)

  