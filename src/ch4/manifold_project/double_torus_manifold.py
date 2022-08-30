#!/usr/bin/python3
from identification_objects import *


  
'''
  Block of identification functions for the 4 sections of a double torus.
         1     2
      +-----+-----+
     4|           |3
     _|           |_
     3|           |4
      |           | 
      +-----+-----+
         2     1

'''
# (x, 1) ~ (x + 1/2, 0) for x in [0, 1/2]
def double_torus_identify_1(O, x_curr, y_curr):
  half_x = O.get_x_dist() / 2
  return (x_curr + half_x, O.get_y_min())

# (x, 1) ~ (x - 1/2, 0) for x in [1/2, 1]
def double_torus_identify_2(O, x_curr, y_curr):
  half_x = O.get_x_dist() / 2
  return (x_curr - half_x, O.get_y_min())

# (1, y) ~ (0, y - 1/2) for y in [1/2, 1]
def double_torus_identify_3(O, x_curr, y_curr):
  half_y = O.get_y_dist() / 2
  return (O.get_x_min(), y_curr - half_y)

# (1, y) ~ (0, y + 1/2) for y in [0, 1/2]
def double_torus_identify_4(O, x_curr, y_curr):
  half_y = O.get_y_dist() / 2
  return (O.get_x_min(), y_curr + half_y)

double_torus_region_map = [(0, 3), (np.pi/4, 2), (np.pi / 2, 1), ( 3 * np.pi / 4, 4), (10, 10),(np.pi, 3), (5 * np.pi / 4, 2), (3 * np.pi / 2, 1), (7 * np.pi / 4, 4), (10, 10)]

'''
  For sanity, we use angles to inform which identification should be used when constructing the line segment.
  double_torus_region_map: Hardcoded boundaries to enforce separation between regions
'''
def find_region(O, target_point):
  center = (O.get_x_dist() / 2 + O.get_x_min(), O.get_y_dist() / 2 + O.get_y_min())

  tx,ty = target_point
  cx,cy = center
  rad_theta = np.arctan2(ty - cy, tx - cx)
  if rad_theta < 0:
    rad_theta = 2 * np.pi + rad_theta
  c = 5
  if rad_theta < np.pi:
    c = 0
  while rad_theta >= double_torus_region_map[c + 1][0]:
    c+=1
  
  return double_torus_region_map[c][1]

# jump table for identifications
double_torus_identifications = {
  1 : lambda o, x, y : double_torus_identify_1(o, x, y),
  2 : lambda o, x, y : double_torus_identify_2(o, x, y),
  3 : lambda o, x, y : double_torus_identify_3(o, x, y),
  4 : lambda o, x, y : double_torus_identify_4(o, x, y)
}
'''
  Calculate double torus segment embedded in R2.
  Given a start point and some angle, determine the end point.
'''
def double_torus_next_segment(O, x_curr, y_curr, rad_angle):
  # hardcoded condition for dodging origin 
  if not (x_curr == O.get_x_min() and y_curr == O.get_y_min()):
    x_curr, y_curr = double_torus_identifications[find_region(O, (x_curr,y_curr))](O,x_curr, y_curr)

  x_dist = O.get_x_dist()
  x_end = x_curr + x_dist

  # check overshoot opposite x axis
  # this would mean that y_curr is y_min
  if O.check_x_max(x_end):
    x_excess = x_end - O.get_x_max()
    x_dist = x_dist - x_excess
    x_end = x_curr + x_dist
  
  #this is an adjustment for y_dist assuming x_dist is out of bounds.
  y_dist = np.multiply(x_dist, np.tan(rad_angle))
  y_end = y_curr + y_dist
  
  # check out of bounds on opposite y axis. 
  # this would mean that x_curr is x_min
  if O.check_y_max(y_end):
    y_excess = y_end - O.get_y_max()
    y_dist = y_dist - y_excess
    y_end = y_curr + y_dist
    x_dist = np.divide(y_dist, np.tan(rad_angle))
    x_end = x_curr + x_dist
  
  return ((x_curr, y_curr), (x_end, y_end))

'''
Double Torus Function

  Author's Note:
    Several specific identifications may be left out. Finding and adding them is left as
    an exercise.
  
  Given some angle, return pairs of points which draw segments on the manifold.
  
'''
def double_torus(o, angle_degrees):
  o.next_segment = lambda O, x_curr, y_curr, rad_angle: double_torus_next_segment(O, x_curr, y_curr, rad_angle)
  lines = []
  ox,oy = o.get_x_min(), o.get_y_min()
  r = angle_degrees * np.pi / 180
  # Double torus is unbounded, artificial limit is set on the number of line segments
  counter = 0
  LIMIT = 30
  while not o.end_flag and counter < LIMIT:
    lines.append(o.next_segment(o, ox, oy, r))
    ox, oy = lines[-1][1]
    counter+=1

  return lines


