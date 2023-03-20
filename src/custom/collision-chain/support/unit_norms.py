#!/usr/bin/python3
import numpy as np
from support.Line import *


def get_unit_norm(ray_origin, ray_target):
  '''
  returns a vector normal to the segment connecting origin and target
  Returns a Line object
  '''
  # x0,y0 = world_origin.get_point()
  x1,y1 = ray_origin
  x2,y2 = ray_target
  # placeholder for global origin
  # y2 + (y0 - y1) - y0 = y2 - y1
  # x2 + (x0 - x1) - x0 = x2 - x1
  
  rad_theta = np.arctan2(y2 - y1, x2 - x1)
  rad_prime = rad_theta
  if rad_prime < -np.pi / 2:
    rad_prime = 2 * np.pi + rad_prime
  rad_prime = rad_prime - np.pi / 2
  # print(rad_theta)
  dist = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
  r = dist / 2
  norm_x = r * np.cos(rad_theta)
  norm_y = r * np.sin(rad_theta)
  return Line([x1 + norm_x,y1 + norm_y], r, rad_prime)


def get_unit_norm_angle(ray_origin, ray_target, switch = False):
  '''
  Returns the angle in radians of the vector normal to the line between two
  points.
  Switch is used by caller functions to flip the angle around the unit circle.
  '''
  x1,y1 = ray_origin
  x2,y2 = ray_target
  
  rad_theta = np.arctan2(y2 - y1, x2 - x1)
  # print(rad_theta)
  rad_prime = rad_theta
  if rad_prime < -np.pi / 2:
    rad_prime = 2 * np.pi + rad_prime
  rad_prime = rad_prime - np.pi / 2

  if switch:
    if rad_prime > 0:
      return rad_prime - np.pi
    return rad_prime + np.pi
  return rad_prime

def get_ray_angle(ray_origin, ray_target):
  '''
  Computes the angle of the vector from origin to target
  '''
  x1,y1 = ray_origin
  x2,y2 = ray_target
  
  rad_theta = np.arctan2(y2 - y1, x2 - x1)
  return rad_theta

def get_rectangular_coord(origin, radius, rad_theta):
  '''
  Converts from polar coordinates to rectangular coordinates
  Returns a point (x,y)
  '''
  ox, oy = origin
  x = np.cos(rad_theta) * radius
  y = np.sin(rad_theta ) * radius
  return (ox + x, oy + y)

def get_polar_coord(origin, target):
  '''
  Converts from rectangular coordinates to polar coordinates
  returns a point (r, theta)
  '''
  ox,oy = origin
  tx,ty = target
  dist = np.sqrt(np.square(tx - ox) + np.square(ty - oy))
  theta = np.arctan2(ty - oy, tx - ox)
  return (dist,theta)