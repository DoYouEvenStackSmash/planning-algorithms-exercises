#!/usr/bin/python3

from identification_objects import *

def torus_x_identify(O, x):
  if O.check_x_max(x):
    return O.get_x_min()
  return x

def torus_y_identify(O, y):
  if O.check_y_max(y):
    return O.get_y_min()
  return y

def torus_next_segment(O, x_curr, y_curr, rad_angle):
  x_curr = O.x_identify(O, x_curr)
  y_curr = O.y_identify(O, y_curr)
  
  # x_dist could overshoot x_max
  x_dist = O.get_x_max() - O.get_x_min()
  x_end = x_curr + x_dist
  if not O.check_x_min(x_curr):
    x_excess = x_end - O.get_x_max()
    x_dist = x_dist - x_excess
    x_end = x_curr + x_dist
  # y_dist could overshoot y_max
  y_dist = np.multiply(x_dist, np.tan(rad_angle))
  y_end = y_curr + y_dist

  if O.check_y_max(y_end):
    y_excess = y_end - O.get_y_max()
    y_dist = y_dist - y_excess
    y_end = y_dist + y_curr # should equal y_max
    x_dist = np.divide(y_dist, np.tan(rad_angle))
  x_end = x_curr + x_dist
  return ((x_curr, y_curr), (x_end, y_end))
  

def torus(o, angle_degrees):
  o.x_identify = lambda O,x: torus_x_identify(O, x)
  # y_max_rules
  # print(o.x_identify(o,.5))
  o.y_identify = lambda O,y : torus_y_identify(O, y)
  o.next_segment = lambda O, x_curr, y_curr, rad_angle: torus_next_segment(O, x_curr, y_curr, rad_angle)
  lines = []
  ox,oy = o.get_x_min(),o.get_y_min()
  r = angle_degrees * np.pi / 180
  counter = 0
  while not o.end_flag and counter < 20:
    lines.append(o.next_segment(o,ox,oy,r))
    ox,oy = lines[-1][1]
    counter+=1
  for i in lines:
    print(i)
  return lines

  