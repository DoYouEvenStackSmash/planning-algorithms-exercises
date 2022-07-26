#!/usr/bin/python3

import pygame
import time

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
  return pygame.display.set_mode((width, height))

def frame_draw_polygon(screen, point_set, color = (0,0,0)):
  pygame.draw.polygon(screen, color, point_set, width=1)

def frame_draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)

def frame_draw_bold_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.line(screen, color, s, e, width=4)

def frame_draw_dot(screen, point, color = (0,0,0), width = 4):
  pygame.draw.circle(screen, color, point, 4, width)

def clear_frame(screen):
  pygame.Surface.fill(screen, (0,0,0))

def draw_lines_between_points(screen, pts, color = colors["white"]):
  # draw_test_vectors(pts)
  color_arr = [colors["red"], colors["yellow"], colors["white"]]
  for i in range(1, len(pts)):
    frame_draw_dot(screen, pts[i - 1], colors["red"])
    # pygame.display.update()
    # time.sleep(.1)
    frame_draw_line(screen, (pts[i - 1], pts[i]), color)
    # pygame.display.update()
    # time.sleep(.1)
  frame_draw_dot(screen, pts[-1], colors["red"])
  frame_draw_line(screen, (pts[-1], pts[0]), color)
  # pygame.display.update()


