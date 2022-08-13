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
  
  def reset_all_vec(self):
    self.reset_in_vec()
    self.reset_out_vec()
  
  def reset_in_vec(self):
    self.in_vec = self.compute_vec(self.calculate_in_vec_angle())
  
  def reset_out_vec(self):
    self.out_vec = self.compute_vec(self.calculate_out_vec_angle())
  
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
    # head of half planes circular linked list
    self.half_planes_head = None
    # orientation line for the polygon. contains the origin to rotate around
    self.orient_axis = None
  
  def get_orient_axis(self):
    return self.orient_axis
  
  def update_edges(self):
    hold = self.half_planes_head
    hold.reset_all_vec()
    hold = hold.m_next
    while hold != self.half_planes_head:
      hold.reset_all_vec()
      hold = hold.m_next
    
  
  # returns a tuple of the polygon origin
  def get_origin(self):
    return self.half_planes_head.H.line.get_origin()
  
  def get_base_line(self):
    return self.half_planes_head.H.line
  
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
  
def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def rotate_edge_vector(origin, edge_vector, rotation_matrix):
  ox,oy = origin.get_point()
  ev_x,ev_y = edge_vector.get_origin()
  step = np.matmul(rotation_matrix, np.array([[ev_x - ox], [ev_y - oy]]))
  edge_vector.origin = Point(step[0][0] + ox, step[1][0] + oy)
  # edge_vector.rad_angle = edge_vector.rad_angle + target_rad


# def rotate_polygon_rad(polygon, rotation_matr):

def get_polygon_point_rotation(polygon, target_point):
  base_line = polygon.get_base_line()
  target_rad = base_line.compute_rotation_rad(target_point)
  return target_rad

def rotate_polygon(polygon, target_point, rotation_matrix = None, target_angle = None):
  base_line = polygon.get_base_line()
  # ox,oy = base_line.get_origin()
  if target_point == None:
    target_rad = target_angle
    r_theta = rotation_matrix
  else:
    target_rad = base_line.compute_rotation_rad(target_point)
    r_theta = get_cc_rotation_matrix(target_rad)
  # el = polygon.get_edge_list()
  h = polygon.half_planes_head
  rotate_edge_vector(base_line.origin,h.H.line,r_theta)
  if h.H.line.get_rad_angle() + target_rad > np.pi:
    h.H.line.rad_angle = -2 * np.pi + h.H.line.get_rad_angle() + target_rad
  elif h.H.line.get_rad_angle() + target_rad < -np.pi:
    h.H.line.rad_angle = 2 * np.pi + h.H.line.get_rad_angle() + target_rad
  else:
    h.H.line.rad_angle = h.H.line.get_rad_angle() + target_rad
    # print("all is well")
  
  # print(f"rad_angle:\t{h.H.line.rad_angle}")
  # print(f"rad_angle:\t{target_rad}")
  h = h.m_next
  while h != polygon.half_planes_head:
  # for i in range(len(el)):
    # l = el[i].H.line
    rotate_edge_vector(base_line.origin,h.H.line,r_theta)
    if h.H.line.get_rad_angle() + target_rad > np.pi:
      h.H.line.rad_angle = -2 * np.pi + h.H.line.get_rad_angle() + target_rad
    elif h.H.line.get_rad_angle() + target_rad < -np.pi:
      h.H.line.rad_angle = 2 * np.pi + h.H.line.get_rad_angle() + target_rad
    else:
      h.H.line.rad_angle = h.H.line.get_rad_angle() + target_rad
      # print("all is well")
    h = h.m_next
  polygon.update_edges()


def conv_func(theta):
    if theta < 0:
      return 2 * np.pi - abs(theta)
    return theta

def edge_key(e):
  return conv_func(e[1].get_rad_angle())

def sort_edge_vectors(edge_list):
  adjust = lambda edge_obj : edge_key(edge_obj)
  sorted_edge_list = sorted(edge_list, key=adjust)
  return sorted_edge_list

def add_robot_vectors(polygon, edge_vector_list):
  in_el = polygon.get_edge_list()
  for e in in_el:
    edge_vector_list.append((e,e.get_in_vec()))

def add_obstacle_vectors(polygon, edge_list):
  out_el = polygon.get_edge_list()
  for e in out_el:
    edge_list.append((e,e.get_out_vec()))

def solve_cross_angle(cross_angle):
  theta_0 = cross_angle
  if theta_0 < np.pi / 2:
    theta_1 = theta_0 + np.pi / 2
  else:
    theta_1 = -2 * np.pi + theta_0 + np.pi / 2
  return theta_1

def compute_end_point(origin, length, rad_angle):
  ox,oy = origin
  r = length
  x = r * np.cos(rad_angle)
  y = r * np.sin(rad_angle)
  return Point(ox + x, oy + y)

def compute_obs_polygon(robot, obstacle):
  edge_list = []
  # obs_el = rectangle_p.get_edge_list()
  # rob_el = offset_triangle_p.get_edge_list()
  add_robot_vectors(robot, edge_list)
  add_obstacle_vectors(obstacle, edge_list)
  # print(len(edge_list))
  # sel = tuples (Edge, radian key)
  sorted_edge_tuple_list = sort_edge_vectors(edge_list)
  e,r = sorted_edge_tuple_list[0]
  # print(f"first_edge\t{r.get_rad_angle()}")
  x1,y1 = e.H.line.get_endpoint()
  first_point = Point(x1,y1)
  # print(f"first point\t{first_point.get_point()}")
  point_list = [first_point]
  c = 1
  for i,j in sorted_edge_tuple_list[1:]:
    edge_object = i
    norm_v = j
    rad_angle = solve_cross_angle(norm_v.get_rad_angle())
    
    # print(norm_v.get_rad_angle())
    length = i.H.line.get_length()
    # print(length)
    # print(rad_angle * 180 / np.pi)
    point_list.append(compute_end_point(point_list[-1].get_point(),length, rad_angle))
    # print(f"pt {c}:\t{point_list[-1].get_point()}")
    c+=1
    # point_list.append(compute_end_point(point_list[-1].get_point(),length, rad_angle))

  c_obs = points_to_polygon((500,500),point_list)
  return c_obs
