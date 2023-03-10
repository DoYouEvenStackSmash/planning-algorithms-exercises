#!/usr/bin/python3
import numpy as np
import pygame
import time


class MathFxns:
  '''
  Math helper functions
  '''
  def euclidean_dist(p1, p2):
    '''
    Calculates euclidean distance between two points
    Returns a scalar value
    '''
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

  def car2pol(origin, pt):
    '''
    Converts a pair of points into a vector
    returns a vector (radians, radius)
    '''
    x,y = pt
    ox, oy = origin
    rad = np.arctan2(y - oy, x - ox)
    r = MathFxns.euclidean_dist(origin, pt)
    return (rad, r)

class GeometryFxns:
  def get_equilateral_vertex(pt1, pt2,sign=1):
    '''
    Calculates the vertex of an equilateral triangle
    Returns a point
    '''
    rad,r = MathFxns.car2pol(pt1,pt2)
    nx = r * np.cos(rad + np.pi * sign / 3) 
    ny = r * np.sin(rad + np.pi * sign / 3) 
    return (nx + pt1[0],ny + pt1[1])

  def get_midpoint(pt1, pt2):
    '''
    Calculates the midpoint of the segment connecting two points
    Returns a point
    '''
    rad,r = MathFxns.car2pol(pt1,pt2)
    nx = r/2 * np.cos(rad)
    ny = r/2 * np.sin(rad)
    return (nx + pt1[0],ny + pt1[1])
  
  def lerp(pt1, pt2, t):
    '''
    Lerp between two points
    Returns a point
    '''
    rad, r = MathFxns.car2pol(pt1,pt2)
    nx = r * t * np.cos(rad)
    ny = r * t * np.sin(rad)
    return (nx + pt1[0],ny + pt1[1])
    
class PygameArtFxns:
  ''' set of colors '''
  colors = {
  "black" : (0,0,0),
  "indigo" : (48,79,254),
  "faded-blue": (15,173,237),
  "sky-blue": (111,205,244),
  "darker-green": (47,178,35),
  "yellow" : (255,255,0),
  "tangerine":(255,119,34),
  "pink":(255,122,173),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255),
  "red" : (255, 0, 0),
  "white" : (255,255,255)
  
  }
  def create_display(width, height):
    '''
    Initializes a pygame display
    width, height := pixel dimensions of the display
    Returns a pygame display object

    '''
    return pygame.display.set_mode((width, height))

  def frame_draw_polygon(screen, point_set, color = (0,0,0)):
    '''
    Draws a polygon of specified color
    Returns nothing
    '''
    pygame.draw.polygon(screen, color, point_set, width=1)

  def frame_draw_line(screen, point_set, color = (0,0,0)):
    '''
    Draws a thin line given a pair of points (start, end)
    Returns nothing
    '''
    s,e = point_set
    pygame.draw.aaline(screen, color, s, e)

  def frame_draw_bold_line(screen, point_set, color = (0,0,0)):
    '''
    Draws a bold line given a pair of points (start, end)
    Returns nothing
    '''
    s,e = point_set
    pygame.draw.line(screen, color, s, e, width=4)

  def frame_draw_dot(screen, point, color = (0,0,0), width = 4):
    '''
    Draws a single dot given a point (x, y)
    Returns nothing
    '''
    pygame.draw.circle(screen, color, point, 4, width)

  def clear_frame(screen, color=(0,0,0)):
    '''
    Resets the pygame display to a given color
    Returns nothing
    '''
    pygame.Surface.fill(screen, color)

  def draw_lines_between_points(screen, pts, color = colors["white"]):
    '''
    Given an ordered list of points, draws lines connecting each pair
    Returns nothing
    '''
    color_arr = [colors["red"], colors["yellow"], colors["white"]]
    for i in range(1, len(pts)):
      # frame_draw_dot(screen, pts[i - 1], colors["red"])
      
      frame_draw_line(screen, (pts[i - 1], pts[i]), color)
      
    # frame_draw_dot(screen, pts[-1], colors["red"])
    frame_draw_line(screen, (pts[-1], pts[0]), color)
    


