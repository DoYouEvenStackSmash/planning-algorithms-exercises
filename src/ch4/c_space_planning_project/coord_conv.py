#!/usr/bin/python3
import numpy as np

from half_plane import *
# class CoordConv:

def create_edge(world_origin, ray_origin, ray_target):
  # x0,y0 = world_origin.get_point()
  
  x1,y1 = ray_origin.get_point()
  x2,y2 = ray_target.get_point()
  # placeholder for global origin
  # y2 + (y0 - y1) - y0 = y2 - y1
  # x2 + (x0 - x1) - x0 = x2 - x1
  
  rad_theta = np.arctan2(y2 - y1, x2 - x1)
  
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  return Line(Point(x1,y1),dist, rad_theta)

      