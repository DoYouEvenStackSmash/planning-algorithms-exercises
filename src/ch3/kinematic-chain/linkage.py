#!/usr/bin/python3
import numpy as np
class Point:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y

  def get_coord(self):
    return (self.x, self.y)
  
class Link:
  def __init__(self, origin = Point(), link_len = 0, rad_angle = 0, point_set = [], m_prev = None, m_next = None):
    # center pivot point
    self.origin = origin
    # distance between origin and end member
    self.link_len = link_len
    # unit circle for arithmetic
    self.r = 1
    # angle from center in radians
    self.rad_angle = rad_angle
    # outline of link
    self.point_set = point_set

    self.absolute_offset = None
    
    # doubly linked list
    self.m_prev = m_prev
    self.m_next = m_next
  
  def get_point_set(self):
    return self.point_set

  def get_local_rad_angle(self):
    return self.rad_angle
   
  def get_end_point(self):
    x_o, y_o = self.origin.get_coord()
    x = np.cos(self.get_relative_rad_angle()) * self.link_len
    y = np.sin(self.get_relative_rad_angle()) * self.link_len
    return (x + x_o, y + y_o)

  def set_rad_angle(self, rad_angle):
    self.rad_angle = rad_angle

  def compute_rotation_rad(self, target_point):
    t_x, t_y = target_point
    o_x, o_y = self.origin.get_coord()
    a_x, a_y = 0,0#self.absolute_offset.get_coord()
    base_rad = self.get_relative_rad_angle()
    target_rad = np.arctan2((t_y - a_y) - (o_y - a_y), (t_x - a_x) - (o_x - a_x))

    rotation = target_rad - base_rad
    if rotation > np.pi:
      rotation = rotation - (2 * np.pi)
    if rotation < -np.pi:
      rotation = rotation + (2 * np.pi)
    
    return rotation
  
  def get_relative_rad_angle(self):
    if self.m_prev:
      return self.m_prev.get_relative_rad_angle() + self.rad_angle
    return self.rad_angle
  
  def set_point_set(self, point_set):
    self.point_set = point_set

  def set_origin(self, origin):
    self.origin = origin

  def get_origin(self):
    return self.origin
  
  
  # def rotate_chain(self, target_point):

    