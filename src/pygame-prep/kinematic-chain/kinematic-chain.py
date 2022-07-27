#!/usr/bin/python3
import pygame
import time
import sys
import numpy as np
from chain_link import Point,Link


def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_polygon(screen, point_set):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.polygon(screen, (255,0,0), point_set, width=2)
  pygame.display.update()

def main():
  
  pygame.init()
  screen = create_display(500,500)
  
  origin = Point(250,250)
  l,w = 50, 10
  back_two = [Point(origin.x - l/10, origin.y - w/2), Point(origin.x - l/10, origin.y + w/2)]
  front_two = [Point(origin.x + l, origin.y - w/2), Point(origin.x + l, origin.y + w/2)]
  point_set = [back_two[0], front_two[0], front_two[1], back_two[1]]
  link_1 = Link(origin, l, 0, point_set)
  a = link_1.get_point_set()
  b = []
  for i in a:
    b.append(i.get_coord())
  
  draw_polygon(screen, b)
  while 1:
    for event in pygame.event.get():
      if event.type ==pygame.QUIT: sys.exit()
  
main()


