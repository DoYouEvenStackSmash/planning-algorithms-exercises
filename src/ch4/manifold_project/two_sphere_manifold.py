#!/usr/bin/python3

from identification_objects import *

def a_identify(o, x, y):
  return (o.get_x_min() + x - x, o.get_y_min() + y - x)

def b_identify(o, x, y):
  return (o.get_x_min() + x - y, o.get_y_min() + y - y)

def two_sphere_next_segment(O, x_curr, y_curr, rad_angle):
  if rad_angle > np.pi / 4:
    x_curr, y_curr = a_identify(O, x_curr, y_curr)
  else:
    x_curr, y_curr = b_identify(O, x_curr, y_curr)
  x_dist = O.get_x_max() - O.get_x_min()
  # y_dist = O.get_y_max() - O.get_y_min()

  x_end = x_curr + x_dist
  # y_end = y_curr + y_dist
  if O.check_x_max(x_end): # x segment goes out of bounds, would happen in B
    x_excess = x_end - O.get_x_max()
    x_dist = x_dist - x_excess
    x_end = x_curr + x_dist # x_end should now be x_max
  y_dist = np.multiply(x_dist, np.tan(rad_angle))
  y_end = y_curr + y_dist
  if O.check_y_max(y_end): # y segment goes out of bounds, would happen in A
    y_excess = y_end - O.get_y_max()
    y_dist = y_dist - y_excess
    y_end = y_curr + y_dist
    x_dist = np.divide(y_dist, np.tan(rad_angle))
    x_end = x_curr + x_dist
  return ((x_curr, y_curr), (x_end, y_end))

def two_sphere(o, angle_degrees):
  o.next_segment = lambda O, x_curr, y_curr, rad_angle: two_sphere_next_segment(O, x_curr, y_curr, rad_angle)
  lines = []
  ox, oy = o.get_x_min(), o.get_y_min()
  r = angle_degrees * np.pi / 180
  counter = 0
  while not o.end_flag and counter < 20:
    lines.append(o.next_segment(o, ox, oy, r))
    ox,oy = lines[-1][1]
    counter+=1
  return lines


    
