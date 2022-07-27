#!/usr/bin/python3
import numpy as np

class Point:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y
  
  def get_coord(self):
    return (self.x, self.y)
  
class Link:
  def __init__(self, origin = Point(), link_len = 0, rad_angle = 0, point_set = []):
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
  
  def get_point_set(self):
    return self.point_set
  
  def set_point_set(self, point_set):
    self.point_set = point_set
  
  def get_origin(self):
    return self.origin
  
  def set_origin(self, origin):
    self.origin = origin
  
  def set_rad_angle(self, rad_angle):
    self.rad_angle = rad_angle
  
  def get_end_member(self):
    e_x, e_y = self.origin.get_coord()
    return (e_x + self.link_len, e_y + self.link_len)
  
  def get_end_point(self):
    x_o, y_o = self.origin.get_coord()
    x = np.cos(self.rad_angle) * self.link_len
    y = np.sin(self.rad_angle) * self.link_len
    return (x + x_o, y + y_o)
  
  def get_rad_angle(self):
    return self.rad_angle

# radius = linkage_len
# chord_len = distance_to_target
# center_angle = np.arcsin(chord_len / 2 * radius)

# rads_orig_to_origin - rads_origin_to_target
# origin_target_rad = np.arctan2(global_origin_y - link_origin_y, global_origin_x - link_origin_x)
# rads_center_target_dist = np.arcsin(target_dist / 2 * link_len) * 2

# target_rad = origin_target_rad - link_rad_angle - rads_center_target_dist