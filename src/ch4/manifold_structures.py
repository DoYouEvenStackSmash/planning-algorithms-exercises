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
    return sef.rad_angle
  
class Plane:
  def __init__(self, origin = Point(), x_axis = Line(), y_axis = Line()):
    self.origin = origin
    self.x_axis = x_axis
    self.y_axis = y_axis
  
  def get_x_axis_segment(self):
    return self.x_axis.get_segment()
  
  def get_y_axis_segment(self):
    return self.y_axis.get_segment()
  
  def make_segment(self, origin_pt, rad_angle):
    opp = lambda adj,theta: adj * np.tan(theta)

    x_o, y_o = origin_pt
    
    
    # if angle > 45 degrees, compute x val 
    if rad_angle > (np.pi / 4):
      a =  self.y_axis.get_length()
      # angle is complementary to input
      r_theta = self.y_axis.get_rad_angle() - rad_angle
      x_e = opp(a, r_theta)
      y_e = y_o + a
      # y axis is bounding, compute x
    else:
      # angle <= 45 degrees, compute y val
      
      r_theta = rad_angle
      a = self.x_axis.get_length()
      y_e = opp(a, r_theta)
      x_e = x_o + a
    
    return ((x_o, y_o), (x_e, y_e))
    






