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

def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def rotate_point_set(origin, point_set, rotation_matrix):
  new_point_set = []
  x_o, y_o = origin.get_coord()
  for p in range(len(point_set)):
    lp_x, lp_y = point_set[p].get_coord()
    step = np.matmul(rotation_matrix, np.array([[lp_x - x_o], [lp_y - y_o]]))
    new_point_set.append(Point(step[0][0] + x_o, step[1][0] + y_o))
  return new_point_set

def rotate_link(origin, target_link, rotation_matrix):
  target_link.set_point_set(rotate_point_set(origin, target_link.get_point_set(), rotation_matrix))
  target_link.set_origin(rotate_point_set(origin, [target_link.get_origin()], rotation_matrix)[0])
  


def rotation(screen, link_base, link_chain, target_point):
  t_x, t_y = target_point
  o_x, o_y = link_base.get_origin().get_coord()
  base_rad = link_base.get_rad_angle()
  target_rad = np.arctan2(t_y - o_y, t_x - o_x)

  rotation = target_rad - base_rad
  if rotation > np.pi:
    rotation = rotation - (2 * np.pi)
  if rotation < -np.pi:
    rotation = rotation + 2 * (np.pi)

  moves = abs(rotation * 180 / np.pi)
  
  if int(moves) == 0:
    moves = 1
  
  step_rad = rotation / int(moves)
  orig = link_base.get_origin()
  cc_rotation_matrix = get_cc_rotation_matrix(step_rad)
  for i in range(int(moves)):
    for j in range(len(link_chain)):
      rotate_link(orig, link_chain[j], cc_rotation_matrix)
    draw_frame(screen, link_chain)
    time.sleep(0.01)
  
  link_base.set_rad_angle(target_rad)
    

def main():
  
  pygame.init()
  screen = create_display(500,500)
  
  origin = Point(250,250)
  l,w = 50, 10
  link_1 = create_link(origin, l, w, 45)
  x, y = link_1.get_end_point()
  link_2 = create_link(Point(x,y), l, w, 45)
  link_chain = [link_1, link_2]
  # back_two = [Point(origin.x - l/10, origin.y - w/2), Point(origin.x - l/10, origin.y + w/2)]
  # front_two = [Point(origin.x + l + 5, origin.y - w/2), Point(origin.x + l + 5, origin.y + w/2)]
  # point_set = [back_two[0], front_two[0], front_two[1], back_two[1]]
  # link_1 = Link(origin, l, 0, point_set)
  # a = link_1.get_point_set()
  # b = []
  # for i in a:
  #   b.append(i.get_coord())
  draw_frame(screen, link_chain)
  # draw_polygon(screen, b)
  # draw_dot(screen, link_1.get_origin())

  while 1:
    for event in pygame.event.get():
      if event.type ==pygame.QUIT: sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        rotation(screen, link_1, link_chain, pygame.mouse.get_pos())
  
main()


