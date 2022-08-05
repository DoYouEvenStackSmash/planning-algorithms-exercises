#!/usr/bin/python3

import pygame
import numpy as np
import sys
import time
from manifold_structures import *

colors = {
  "black" : (0,0,0),
  "yellow" : (255,255,0),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255),
  "red" : (255, 0, 0)
}

def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_polygon(screen, point_set, color = (0,0,0)):
  pygame.draw.polygon(screen, color, point_set, width = 1)
  pygame.display.update()

def draw_dot(screen, point, color = (0,0,0)):
  pygame.draw.circle(screen, color, point, 2 , 2)
  pygame.display.update()

def draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)
  pygame.display.update()

def frame_draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)

def draw_plane(screen, point_set, axis_color = (0,0,0), boundary_color = (0,0,0)):
  xs, xe = point_set[0]
  axs, axe = point_set[2]
  ys, ye = point_set[1]
  ays, aye = point_set[3]
  pygame.draw.aaline(screen, axis_color, xs, xe)
  pygame.draw.aaline(screen, axis_color, ys, ye)

  pygame.draw.aaline(screen, boundary_color, axs, axe)
  pygame.draw.aaline(screen, boundary_color, ays, aye)

  pygame.display.update()


def to_rad(deg):
  return np.multiply(deg / 180, np.pi)


def create_axis(origin_pt, length, rad_angle):
  x,y = origin_pt
  return Line(Point(x,y), length, rad_angle)

def create_plane(origin_pt, x_axis, y_axis):
  x,y = origin_pt
  return Plane(Point(x,y), x_axis, y_axis)

def draw_frame_lines(screen, line_segments, line_colors):
  pygame.Surface.fill(screen, (0,0,0))
  for i in range(len(line_segments)):
    frame_draw_line(screen, line_segments[i], line_colors[i])
  pygame.display.update()

def compute_lines(origin, l, theta, x_max, y_max):

  s, e = l
  x1,y1 = s
  x2,y2 = e

  delta_y = y2 - y1

  opposite = y_max
  
  adjacent = opposite / np.tan(theta)
  print(f"adj: {adjacent}")
  n = int(adjacent / x_max)
  print(f"n:\t{n}")
  xs, ys = origin
  
  ls = [((x1,y1),(x2,y2))]
  lc = [colors["green"]]
  
  for i in range(1,n):
    '''
    ls[-1] =  (
            0   (x1, y1),
            1   (x2, y2)
              )
    '''
    last_x1, last_y1 = ls[-1][0][0],ls[-1][0][1]
    last_x2, last_y2 = ls[-1][1][0],ls[-1][1][1]
    curr_x1, curr_y1 = last_x1, last_y2
    curr_x2, curr_y2 = last_x2, last_y2 + delta_y
    
    ls.append(((curr_x1, curr_y1), (curr_x2, curr_y2)))
    lc.append(colors["green"])

  return ls,lc

def m_flat_cylinder(screen):
  
  origin = [100, 100]
  x_len, y_len = 800,800
  x_rad, y_rad = 0, np.pi / 2
  xa = create_axis(origin, x_len, x_rad)
  ya = create_axis(origin, y_len, y_rad)
  o_xa = create_axis(ya.get_endpoint(), x_len, x_rad)
  o_ya = create_axis(xa.get_endpoint(), y_len, y_rad)
  p = create_plane(origin, xa, ya)
  
  x_axis = p.get_x_axis_segment()
  y_axis = p.get_y_axis_segment()
  cx_axis = o_xa.get_segment()
  cy_axis = o_ya.get_segment()
  x_color = colors["cyan"]
  y_color = colors["magenta"]
  line_segments = [x_axis, y_axis, cx_axis, cy_axis]
  line_colors = [x_color, y_color, x_color, y_color]
  
  draw_frame_lines(screen, line_segments, line_colors)

  for i in range(2,45):
    line_segments = [x_axis, y_axis, cx_axis, cy_axis]
    line_colors = [x_color, y_color, x_color, y_color]
  
    theta = i * np.pi / 180

    l = p.make_segment(origin, theta)
    print(l)
    # draw_line(screen, l, colors["green"])
    # return
    ls, lc = compute_lines(origin, l, theta, x_len, y_len)
    for j in range(len(ls)):
      line_segments.append(ls[j])
      line_colors.append(lc[j])
    print(len(ls))
      
    draw_frame_lines(screen, line_segments, line_colors)
    time.sleep(0.2)
  
  

def m_R2(screen):
  origin = [100, 100]
  x_len, y_len = 800,800
  x_rad, y_rad = 0, np.pi / 2
  xa = create_axis(origin, x_len, x_rad)
  ya = create_axis(origin, y_len, y_rad)
  o_xa = create_axis(ya.get_endpoint(), x_len, x_rad)
  o_ya = create_axis(xa.get_endpoint(), y_len, y_rad)
  p = create_plane(origin, xa, ya)
  
  
  print(p.make_segment(origin, 30 * np.pi / 180))
  x_axis = p.get_x_axis_segment()
  y_axis = p.get_y_axis_segment()
  cx_axis = o_xa.get_segment()
  cy_axis = o_ya.get_segment()
  x_color = colors["cyan"]
  y_color = colors["magenta"]
  line_segments = [x_axis, y_axis, cx_axis, cy_axis]
  line_colors = [x_color, y_color, x_color, y_color]
  draw_frame_lines(screen, line_segments, line_colors)
  line_segments.append(None)
  line_colors.append(colors["green"])
  for i in range(91):
    l = p.make_segment(origin, i * np.pi / 180)
    print(f"{i} deg,\t{l}")
    line_segments[-1] = l
    draw_frame_lines(screen, line_segments, line_colors)
    time.sleep(0.1)
  # print(p.x_axis.get_length())
  # draw_line(screen, p.get_x_axis_segment(), colors["cyan"])
  # draw_line(screen, p.get_y_axis_segment(), colors["magenta"])
  # l = p.make_segment(origin, 30 * np.pi / 180)
  
  # draw_line(screen, l, colors["green"])
  
  
  # yo = create_axis(xa.get_endpoint(), y_len, y_rad)
  # xo = create_axis(ya.get_endpoint(), x_len, x_rad)
  # draw_line(screen, yo.get_segment(), colors["magenta"])
  # draw_line(screen, xo.get_segment(), colors["cyan"])


def main():
  w,h = 1000,1000
  pygame.init()
  s = create_display(w,h)
  # m_R2(s)
  m_flat_cylinder(s)
  # lalt = 256
  # lshift = 1
  # ctrl = 64

  # # 500, 500
  
  # origin = [100, 100]
  # x_len, y_len = 800,800
  # x_rad, y_rad = 0, np.pi / 2
  # xa = create_axis(origin, x_len, x_rad)
  # ya = create_axis(origin, y_len, y_rad)
  # p = create_plane(origin, xa, ya)
  # screen = create_display(w,h)
  # print(p.make_segment(origin, 30 * np.pi / 180))
  # draw_line(screen, p.get_x_axis_segment(), colors["cyan"])
  # draw_line(screen, p.get_y_axis_segment(), colors["magenta"])
  # l = p.make_segment(origin, 30 * np.pi / 180)
  # draw_line(screen, l, colors["green"])
  
  
  # yo = create_axis(xa.get_endpoint(), y_len, y_rad)
  # xo = create_axis(ya.get_endpoint(), x_len, x_rad)
  # draw_line(screen, yo.get_segment(), colors["magenta"])
  # draw_line(screen, xo.get_segment(), colors["cyan"])
  
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        sys.exit()

main()
      
