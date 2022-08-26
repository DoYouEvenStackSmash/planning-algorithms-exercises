#!/usr/bin/python3


def gradually_translate_polygon(P, target_point, step_size = 1):
  h = P.get_front_edge()
  r,theta = get_polar_coord(h.source_vertex.get_point_coordinate(), target_point)
  step_r = r / step_size
  x_step = step_r * np.cos(theta)
  y_step = step_r * np.sin(theta)
  for i in range(step_size):
    translate_polygon(P, x_step, y_step)


def translate_polygon(P, x_disp, y_disp):
  h = P.get_front_edge()
  px,py = h.source_vertex.get_point_coordinate()
  h.source_vertex.set_point_coordinate([px + x_disp, py + y_disp])
  h = h._next
  while h != P.get_front_edge():
    px,py = h.source_vertex.get_point_coordinate()
    h.source_vertex.set_point_coordinate([px + x_disp, py + y_disp])
    h = h._next
  



