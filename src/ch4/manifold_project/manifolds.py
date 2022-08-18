#!/usr/bin/python3

from identification_objects import *

def flat_cylinder(o, angle_degrees):
  # o = Obj(10, 100, 10, 100)
  # x_max_rules
  o.x_identify = lambda O,x: flat_cylinder_x_identify(O, x)
  # y_max_rules
  # print(o.x_identify(o,.5))
  o.y_identify = lambda O,y : flat_cylinder_y_identify(O, y)
  o.next_segment = lambda O, x_curr, y_curr, rad_angle: flat_cylinder_next_segment(O, x_curr, y_curr, rad_angle)
  lines = []
  ox,oy = o.get_x_min(),o.get_y_min()
  r = angle_degrees * np.pi / 180
  while not o.end_flag:
    lines.append(o.next_segment(o,ox,oy,r))
    ox,oy = lines[-1][1]
  for i in lines:
    print(i)
  return lines

def blank_object(x_min, x_max, y_min, y_max):
  return Obj(x_min, x_max, y_min, y_max)