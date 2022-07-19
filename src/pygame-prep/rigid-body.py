#!/usr/bin/python3

import time
import pygame
import sys
import numpy as np

class RigidBody:
  def __init__(self, origin=(0,0), x_angle=0, point_set=[]):
    self.origin = origin
    self.x_angle = x_angle
    self.point_set = point_set
  

#create the display
def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_rigid_body(screen, ps):
  pygame.Surface.fill(screen,(0,0,0))
  pygame.draw.polygon(screen, (255, 0, 0), ps, width=3)
  pygame.display.update()


def init_rectangle_rigid_body(length, width, origin):
  o_x,o_y = origin
  points = [origin,(o_x + length, o_y), (o_x + length, o_y + width), (o_x, o_y + width)]
  r = RigidBody(origin, 0, points)
  return r

#pre compute point positions per change in angle
def rotation_matrix(theta):
  conv_rad = np.multiply(theta, np.pi / 180)
  return np.array([[np.cos(conv_rad), -np.sin(conv_rad)],[np.sin(conv_rad),np.cos(conv_rad)]])

#rotate polygon by some amount, return new point set
def rotate( origin, theta, orig_point_set):
  R_theta = rotation_matrix(theta)
  new_point_set = []
  off_x, off_y = origin
  for i in range(len(orig_point_set)):
    x,y = orig_point_set[i]
    np_arr = np.matmul(R_theta,np.array([[x - off_x],[y - off_y]]))
    new_point_set.append((np_arr[0][0] + off_x, np_arr[1][0] + off_y))
  return new_point_set

def rotation(screen, orig_body, target_point):
  x,y = target_point
  total_radians = np.arctan2(y,x) - orig_body.x_angle
  deg = int(np.multiply(total_radians, 180 / np.pi))
  
  ps = orig_body.point_set
  interval = 1
  if deg < 0:
    interval = -1
  for i in range(abs(deg)+1):
    ps = rotate(orig_body.origin, interval, ps)
    draw_rigid_body(screen, ps)
    time.sleep(0.01)
  
  orig_body.point_set = ps
  orig_body.x_angle = np.arctan2(y,x)


  # pygame.draw.polygon(screen, (0,255,0), new_point_set, width=3)
  # pygame.display.update()


def main():
  w,h = 500,500
  pygame.init()
  screen = create_display(w,h)
  origin = (100,100)
  length, width = 100, 20
  r = init_rectangle_rigid_body(length, width, origin)
  draw_rigid_body(screen, r.point_set)
  # for i in range(90):
  #   points = rotate(screen, origin, 1, points)
  #   time.sleep(0.01)
  #   pygame.Surface.fill(screen,(0,0,0))

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        rotation(screen, r, pygame.mouse.get_pos())
        #reorient

main()