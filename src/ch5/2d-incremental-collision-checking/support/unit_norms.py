#!/usr/bin/python3
import numpy as np
from support.Line import *

'''
  returns a vector normal to the line between two points
'''
def get_unit_norm(ray_origin, ray_target):
  # x0,y0 = world_origin.get_point()
  x1,y1 = ray_origin
  x2,y2 = ray_target
  # placeholder for global origin
  # y2 + (y0 - y1) - y0 = y2 - y1
  # x2 + (x0 - x1) - x0 = x2 - x1
  
  rad_theta = np.arctan2(y2 - y1, x2 - x1)
  rad_prime = rad_theta
  if rad_prime < -3 * np.pi / 2:
    rad_prime = 2 * np.pi + rad_prime
  rad_prime = rad_prime - np.pi / 2
  # print(rad_theta)
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  r = dist / 2
  norm_x = r * np.cos(rad_theta)
  norm_y = r * np.sin(rad_theta)
  return Line([x1 + norm_x,y1 + norm_y], r, rad_prime)

'''
  Returns the angle in radians of the vector normal to the line between two
  points.
  Switch is used by caller functions to flip the angle around the unit circle.
'''
def get_unit_norm_angle(ray_origin, ray_target, switch = False):
  x1,y1 = ray_origin
  x2,y2 = ray_target
  
  rad_theta = np.arctan2(y2 - y1, x2 - x1)
  rad_prime = rad_theta
  if rad_prime < -3 * np.pi / 2:
    rad_prime = 2 * np.pi + rad_prime
  rad_prime = rad_prime - np.pi / 2

  if switch:
    if rad_prime > 0:
      return rad_prime - np.pi
    return rad_prime + np.pi
  return rad_prime




