#!/usr/bin/python3

from identification_objects import *

'''
  Identify [0,1]/~ for x
  "Wrap around to x = 0"
'''
def flat_cylinder_x_identify(O, x):
  if O.check_x_max(x):
    return O.get_x_min()
  return x

'''
  No identification for y
  "Wo wrapping for y"
'''
def flat_cylinder_y_identify(O, y):
  return y

'''
  Calculate flat cylinder segment embedded in R2
  Given a start point and some angle, determine the end point.
'''
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

'''
  Flat Cylinder function
    (0,y) ~ (1, y) for all y in [0,1]
  
  Given some angle, return pairs of points which draw segments on the manifold.
'''
def flat_cylinder(o, angle_degrees):
  # o = Obj(10, 100, 10, 100)
  # x_max_rules
  o.end_flag = False
  o.x_identify = lambda O,x: flat_cylinder_x_identify(O, x)
  # y_max_rules
  o.y_identify = lambda O,y : flat_cylinder_y_identify(O, y)
  o.next_segment = lambda O, x_curr, y_curr, rad_angle: flat_cylinder_next_segment(O, x_curr, y_curr, rad_angle)
  lines = []
  ox,oy = o.get_x_min(),o.get_y_min()
  r = angle_degrees * np.pi / 180
  while not o.end_flag:
    lines.append(o.next_segment(o,ox,oy,r))
    ox,oy = lines[-1][1]
  return lines

