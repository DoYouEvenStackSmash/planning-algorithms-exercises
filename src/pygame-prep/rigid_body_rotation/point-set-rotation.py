#!/usr/bin/python3

import pygame
import time
import sys
import numpy as np
from rigid_body_objects import line,RigidBody

def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_polygon(screen, point_set):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.polygon(screen, (255,0,0), point_set, width=2)
  pygame.display.update()

def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def rotate(origin, point_set, rotation_matrix):
  new_point_set = []
  x_o, y_o = origin
  for p in point_set:
    lp_x, lp_y = p
    step = np.matmul(rotation_matrix, np.array([[lp_x - x_o], [lp_y - y_o]]))
    new_point_set.append((step[0][0] + x_o, step[1][0] + y_o))
  return new_point_set

def rotation(screen, rb, target_point):
  origin = rb.origin

  base_line = rb.get_x_axis()
  t_x, t_y = target_point
  
  target_rad = np.arctan2(t_y - base_line.y_off_t, t_x - base_line.x_off_t)
  
  rotation = target_rad - base_line.get_rad_angle()
  if rotation > np.pi:
    rotation = rotation - (2 * np.pi)
  if rotation < -np.pi:
    rotation = rotation + 2 * (np.pi)
  
  moves = abs(rotation * 180 / np.pi)
  
  if moves == 0:
    moves = 1
  
  step_rad = rotation / int(moves)

  cc_rotation_matrix = get_cc_rotation_matrix(step_rad)
  for i in range(int(moves)):
    point_set = rotate(origin, rb.get_point_set(), cc_rotation_matrix)
    draw_polygon(screen, point_set)
    pygame.draw.circle(screen,(0,255,0), (t_x, t_y), 2)
    pygame.display.update()
    rb.set_point_set(point_set)
    time.sleep(0.01)
  
  rb.set_x_axis(target_rad)

def create_rectangle(origin, length, width):
  o_x, o_y = origin
  return [(o_x, o_y), (o_x + length, o_y), (o_x + length, o_y + width), (o_x, o_y + width)]

def create_rigid_body(origin, length, width):
  o_x, o_y = origin
  off_y = width/2
  return [(o_x, o_y - off_y), (o_x + length, o_y - off_y), (o_x + length, o_y + off_y), (o_x, o_y + off_y)]


def main():
  w,h = 500,500
  pygame.init()
  screen = create_display(w,h)
  origin = [250,250]
  length, width = 100, 20
  # ps = create_rectangle(origin, length, width)
  ps = create_rigid_body(origin, length, width)
  rb = RigidBody(origin, ps)
  draw_polygon(screen, ps)

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        rotation(screen, rb, pygame.mouse.get_pos())

main()
