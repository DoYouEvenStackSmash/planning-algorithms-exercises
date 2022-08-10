#!/usr/bin/python3
import numpy as np

from half_plane import *
# class CoordConv:

def create_edge(world_origin, ray_origin, ray_target):
  x0,y0 = world_origin.get_point()
  
  x1,y1 = ray_origin.get_point()
  x2,y2 = ray_target.get_point()

  delta_x = x0 - x1
  delta_y = y0 - y1
  shift_x = x2 + delta_x
  shift_y = y2 + delta_y

  rad_theta = np.arctan2(shift_y - y0, shift_x - x0)
  # rad_theta = np.arctan2(delta_y, delta_x)
  print(f"two point slope rad_theta: {rad_theta}")
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  l = Line(Point(x1,y1),dist, rad_theta)
  print(l.get_origin())
  
  return l
  
def two_point_slope(origin, pt1, pt2):
  x0,y0 = origin.get_point()
  
  x1,y1 = pt1.get_point()
  x2,y2 = pt2.get_point()
  # determine which point comes first, counterclockwise order.
  # this will become the origin.
  theta_pts = [
        np.arctan2(y1 - y0, x1 - x0),
        np.arctan2(y2 - y0, x2 - x0)
  ]
  print(theta_pts)
  # get first counterclockwise point
  min_posn = 0
  for i in range(len(theta_pts)):
    if theta_pts[i] < 0:
      theta_pts[i] = np.pi * 2 - abs(theta_pts[i])
    
    if theta_pts[min_posn] > theta_pts[i]:
      min_posn = i
  
  if min_posn == 1:
    x1,y1 = pt2.get_point()
    x2,y2 = pt1.get_point()
  else:
    x1,y1 = pt1.get_point()
    x2,y2 = pt2.get_point()
  
  # get delta_x
  delta_x = x0 - x1
  delta_y = y0 - y1
  shift_x = x2 + delta_x
  shift_y = y2 + delta_y

  # if delta_y == 0:
  #   if delta_x > 0:
  #     rad_theta = 0
  #   else:
  #     rad_theta = np.pi
  # elif delta_x == 0:
  #   if delta_y > 0:
  #     rad_theta = np.pi / 2
  #   else:
  #     rad_theta = -np.pi / 2
  # else:
  # compute rad_theta using x2 - x0, y2 - y0
  rad_theta = np.arctan2(shift_y - y0, shift_x - x0)
  # rad_theta = np.arctan2(delta_y, delta_x)
  print(f"two point slope rad_theta: {rad_theta}")
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  l = Line(Point(x1,y1),dist, rad_theta)
  print(l.get_origin())
  
  return l
# at this point we have the origin point, which we label as x1,y1


  
      