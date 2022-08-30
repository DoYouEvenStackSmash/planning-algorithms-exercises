#!/usr/bin/python3
from identification_objects import *

'''
  Identify [0, 1 - x]/~ for x
  "Wrap around, and twist
'''
def projective_plane_x_identify(O, x, flip = False):
  if flip:
    return O.get_x_max() - x + O.get_x_min()
  elif O.check_x_max(x):
    return O.get_x_min()
  else:
    return x

'''
  Identify [0, 1 - y]/~ for y
  "Wrap around and twist"
'''
def projective_plane_y_identify(O, y, flip = False):
  if flip:
    return O.get_y_max() - y + O.get_y_min()
  elif O.check_y_max(y):
    return O.get_y_min()
  else:
    return y

'''
  Calculate Projective Plane segment embedded in R2
  Given a start point and some angle, determine the end point.
'''
def projective_plane_next_segment(O, x_curr, y_curr, rad_angle):
  x_flip, y_flip = False, False
  if O.check_x_max(x_curr):
    y_flip = True
  if O.check_y_max(y_curr):
    x_flip = True
  
  x_curr = O.x_identify(O, x_curr, x_flip)
  y_curr = O.y_identify(O, y_curr, y_flip)
  
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


'''
  Projective Plane Function
    (0, y) ~ (1, 1 - y) for all y in (0, 1)
    (x, 0) ~ (1 - x, 1) for all x in (0, 1)

  Author's Note:
    Origin should be identified with 3 other points, corresponding to 
    the corners of the plane. Adding this functionality is left as an exercise.
  
  Given some angle, return pairs of points which draw segments on the manifold.
'''
def projective_plane(o, angle_degrees):
  
  # x_max_rules
  o.end_flag = False
  o.x_identify = lambda O,x, flip: projective_plane_x_identify(O, x, flip)
  # y_max_rules
  # print(o.x_identify(o,.5))
  o.y_identify = lambda O,y,flip : projective_plane_y_identify(O, y, flip)
  o.next_segment = lambda O, x_curr, y_curr, rad_angle: projective_plane_next_segment(O, x_curr, y_curr, rad_angle)
  lines = []
  ox,oy = o.get_x_min(),o.get_y_min()
  r = angle_degrees * np.pi / 180
  
  # Projective plane is unbounded, an artificial limit is set on the number of line segments
  counter = 0
  LIMIT = 10
  while not o.end_flag and counter < LIMIT:
    lines.append(o.next_segment(o,ox,oy,r))
    ox,oy = lines[-1][1]
    counter+=1

  return lines