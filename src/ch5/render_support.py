#!/usr/bin/python3

import pygame
colors = {
  "black" : (0,0,0),
  "yellow" : (255,255,0),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255),
  "red" : (255, 0, 0),
  "white" : (255,255,255),
  "indigo" : (48,79,254)
}

def create_display(width, height):
  return pygame.display.set_mode((width, height))

def frame_draw_polygon(screen, point_set, color = (0,0,0)):
  pygame.draw.polygon(screen, color, point_set, width=1)

def frame_draw_line(screen, point_set, color = (0,0,0)):
  s,e = point_set
  pygame.draw.aaline(screen, color, s, e)

def frame_draw_dot(screen, point, color = (0,0,0)):
  pygame.draw.circle(screen, color, point, 4, 4)

def clear_frame(screen):
  pygame.Surface.fill(screen, (0,0,0))

