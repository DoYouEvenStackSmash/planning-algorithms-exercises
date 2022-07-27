#!/usr/bin/python3
import pygame
import numpy as np
import sys
import time


from linkage import *

def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_polygon(screen, point_set):  
  pygame.draw.polygon(screen, (255,0,0), point_set, width=2)
  pygame.display.update()

def draw_frame(screen, polygons):
  pygame.Surface.fill(screen, (0,0,0))
  for i in range(len(polygons)):
    draw_polygon(screen, [j.get_coord() for j in polygons[i].get_point_set()])
    draw_origin_dot(screen, polygons[i].get_origin().get_coord())
  pygame.display.update()

def draw_origin_dot(screen, dot_pt):
  pygame.draw.circle(screen, (0,0,255), dot_pt, 2)
  pygame.display.update()

def draw_dot(screen, dot_pt):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.circle(screen, (0,255,0), dot_pt, 2)
  pygame.display.update()

def draw_red_dot(screen, dot_pt):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.circle(screen, (255,0,0), dot_pt, 2)
  pygame.display.update()

def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

def rotate_link(origin, link, rotation_matrix):
  o_x, o_y = origin.get_coord()
  new_point_set = []
  for p in link.get_point_set():
    lp_x, lp_y = p.get_coord()
    step = np.matmul(rotation_matrix, np.array([[lp_x - o_x], [lp_y - o_y]]))
    new_point_set.append(Point(step[0][0] + o_x, step[1][0] + o_y))
  
  link.set_point_set(new_point_set)
  
  if link.origin.get_coord() != origin.get_coord():
    lp_x, lp_y = link.get_origin().get_coord()
    step = np.matmul(rotation_matrix, np.array([[lp_x - o_x], [lp_y - o_y]]))
    link.set_origin(Point(step[0][0] + o_x, step[1][0] + o_y))
  
  # return new_point_set
def rotate_chain(base_link, target_point):
  origin = base_link.get_origin()
  prev_rad = base_link.get_relative_rad_angle() - base_link.get_local_rad_angle()
  target_rad = base_link.compute_rotation_rad(target_point)
  r_theta = get_cc_rotation_matrix(target_rad)
  link = base_link
  while link != None:
    rotate_link(origin, link, r_theta)
    link = link.m_next
  base_link.set_rad_angle(target_rad + base_link.get_local_rad_angle())
  

def create_link(origin, side_length, side_width, link_len = 0):
  back_two = [Point(origin.x - side_length/10, origin.y - side_width/2), Point(origin.x - side_length/10, origin.y + side_width/2)]
  front_two = [Point(origin.x + side_length + 5, origin.y - side_width/2), Point(origin.x + side_length + 5, origin.y + side_width/2)]
  point_set = [back_two[0], front_two[0], front_two[1], back_two[1]]
  new_link = Link(origin, link_len, 0, point_set)
  return new_link

def main():
  w,h = 500, 500
  pygame.init()

  lalt = 256
  lshift = 1

  origin = [w/2,h/2]
  screen = create_display(w,h)
  
  origin = Point(250,250)
  l,w = 50, 10
  link_1 = create_link(origin, l, w, 45)
  link_1.absolute_offset = origin
  x, y = link_1.get_end_point()
  link_2 = create_link(Point(x,y), l, w, 45)
  link_2.absolute_offset = origin
  link_2.m_prev = link_1
  link_1.m_next = link_2
  cl = [link_1, link_2]
  draw_frame(screen, cl)


  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        
        if pygame.key.get_mods() == lalt:
          draw_origin_dot(screen, p)
          rotate_chain(link_2, p)
          print(link_2.get_local_rad_angle())
          # print(link_2.compute_rotation_rad(p))
        # if pygame.key.get_pressed()[] == True:
          # draw_dot(screen, p)
        elif pygame.key.get_mods() == lshift:
          draw_origin_dot(screen, p)
          rotate_chain(link_1, p)
          print(link_1.get_local_rad_angle())
          # print(link_1.compute_rotation_rad(p))
          # draw_red_dot(screen,p)
        else:
          print("nothing pressed")
        draw_frame(screen, cl)

main()