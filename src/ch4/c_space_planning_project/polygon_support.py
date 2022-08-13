#!/usr/bin/python3

import numpy as np
from half_plane import *
    
class Edge:
  def __init__(self, hp = None, m_next = None):
    self.H = hp
    self.m_next = m_next
    self.in_vec = None
    self.out_vec = None
    self.vec_len = 20
  
  def test_pt(self, pt = (0,0)):
    return self.H.test_point(pt)
  
  def get_in_vec(self):
    if not self.in_vec:
      self.in_vec = self.compute_vec(self.calculate_in_vec_angle())
    return self.in_vec

  def get_out_vec(self):
    if not self.out_vec:
      self.out_vec = self.compute_vec(self.calculate_out_vec_angle())
    return self.out_vec
  
  def get_out_vec_segment(self):
    if not self.out_vec:
      self.out_vec = self.compute_vec(self.calculate_out_vec_angle())
    return self.out_vec.get_segment()

  # get normal vector pointing to the left of ray
  # + pi/2
  def get_in_vec_segment(self):
    if not self.in_vec:
      self.in_vec = self.compute_vec(self.calculate_in_vec_angle())
    return self.in_vec.get_segment()
  
  #compute normal vector
  def compute_vec(self, vec_angle):
    d = self.vec_len
    r = self.H.line.get_length() / 2
    ox,oy = self.H.line.get_origin()
    rad_theta = self.H.line.get_rad_angle()

    x = r * np.cos(rad_theta)
    y = r * np.sin(rad_theta)
    return Line(Point(x + ox, y + oy), d, vec_angle)

  # calculate normal inner vector angle
  def calculate_in_vec_angle(self):
    theta_0 = self.H.line.get_rad_angle()
    if theta_0 < 0:
      theta_0 = 2 * np.pi - abs(theta_0)
    theta_i = 0
    
    if (theta_0 + (np.pi / 2)) >= 2 * np.pi:
      theta_i = (theta_0 + np.pi / 2) - 2 * np.pi
    elif theta_0 + (np.pi / 2) >= np.pi:
      theta_i = -2 * np.pi + theta_0 + (np.pi / 2)
    else:
      theta_i = theta_0 + (np.pi / 2)
    
    return theta_i
  
  def calculate_out_vec_angle(self):
    theta_0 = self.H.line.get_rad_angle()
    if (theta_0 < -np.pi / 2):
      theta_0 = 2 * np.pi - abs(theta_0)
    theta_i = theta_0 - np.pi / 2
    return theta_i

class Polygon:
  def __init__(self):
    self.half_planes_head = None
  
  def check_collision(self, target_point):
    
    hold = self.half_planes_head
    if hold == None:
      return False
    if hold.test_pt(target_point) != 1:
      return False
    hold = hold.m_next
    
    while hold != self.half_planes_head:
      if hold.test_pt(target_point) != 1:
        return False
      hold = hold.m_next
    return True
  
  def get_segments(self):
    hold = self.half_planes_head
    x = [hold.H.line.get_segment()]
    hold = hold.m_next
    while hold != self.half_planes_head:
      x.append(hold.H.line.get_segment())
      hold = hold.m_next
    return x
  
  def get_in_vec_segments(self):
    hold = self.half_planes_head
    x = [hold.get_in_vec_segment()]
    hold = hold.m_next
    while hold != self.half_planes_head:
      x.append(hold.get_in_vec_segment())
      hold = hold.m_next
    return x
  
  def get_out_vec_segments(self):
    hold = self.half_planes_head
    x = [hold.get_out_vec_segment()]
    hold = hold.m_next
    while hold != self.half_planes_head:
      x.append(hold.get_out_vec_segment())
      hold = hold.m_next
    return x
  
  
  def get_edge_list(self):
    hold = self.half_planes_head
    edgelist = [hold]
    hold = hold.m_next
    while hold != self.half_planes_head:
      edgelist.append(hold)
      hold = hold.m_next
    return edgelist
  
def points_to_polygon(origin, point_list):
  o = Point(origin[0], origin[1])
  edge_list = []
  for i in range(1,len(point_list)):
    h = get_single_edge(o,point_list[i - 1], point_list[i])
    edge_list.append(Edge(h))
  h = get_single_edge(o,point_list[-1], point_list[0])
  edge_list.append(Edge(h))
  for i in range(1,len(edge_list)):
    edge_list[i - 1].m_next = edge_list[i]
  edge_list[-1].m_next = edge_list[0]
  p = Polygon()
  p.half_planes_head = edge_list[0]
  return p
  
