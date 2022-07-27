#!/usr/bin/python3
import pygame
import time
import sys
import numpy as np
from chain_link import Point,Link


def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_polygon(screen, point_set):  
  pygame.draw.polygon(screen, (255,0,0), point_set, width=2)
  pygame.display.update()

def draw_frame(screen, polygons):
  pygame.Surface.fill(screen, (0,0,0))
  for i in range(len(polygons)):
    draw_polygon(screen, [j.get_coord() for j in polygons[i].get_point_set()])
    draw_dot(screen, polygons[i].get_origin())
  pygame.display.update()

def draw_dot(screen, dot_pt):
  pygame.draw.circle(screen, (0,255,0),dot_pt.get_coord(), 2)
  pygame.display.update()

def create_link(origin, side_length, side_width, link_len = 0):
  back_two = [Point(origin.x - side_length/10, origin.y - side_width/2), Point(origin.x - side_length/10, origin.y + side_width/2)]
  front_two = [Point(origin.x + side_length + 5, origin.y - side_width/2), Point(origin.x + side_length + 5, origin.y + side_width/2)]
  point_set = [back_two[0], front_two[0], front_two[1], back_two[1]]
  new_link = Link(origin, link_len, 0, point_set)
  return new_link

def main():
  
  pygame.init()
  screen = create_display(500,500)
  
  origin = Point(250,250)
  l,w = 50, 10
  link_1 = create_link(origin, l, w, 45)
  x, y = link_1.get_end_point()
  link_2 = create_link(Point(x,y), l, w, 45)
  
  # back_two = [Point(origin.x - l/10, origin.y - w/2), Point(origin.x - l/10, origin.y + w/2)]
  # front_two = [Point(origin.x + l + 5, origin.y - w/2), Point(origin.x + l + 5, origin.y + w/2)]
  # point_set = [back_two[0], front_two[0], front_two[1], back_two[1]]
  # link_1 = Link(origin, l, 0, point_set)
  # a = link_1.get_point_set()
  # b = []
  # for i in a:
  #   b.append(i.get_coord())
  draw_frame(screen, [link_1, link_2])
  # draw_polygon(screen, b)
  # draw_dot(screen, link_1.get_origin())

  while 1:
    for event in pygame.event.get():
      if event.type ==pygame.QUIT: sys.exit()
  
main()


