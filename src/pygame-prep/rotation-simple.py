#!/usr/bin/python3
import time
import sys
import numpy as np
import pygame

class line:
  def __init__(self, origin = [0,0], r = 1, rad_angle = 0):
    self.origin = origin
    self.r = r
    self.rad_angle = rad_angle
    self.x_off_t = origin[0]
    self.y_off_t = origin[1]
  
  def get_point(self):
    x_o = self.x_off_t
    y_o = self.y_off_t
    x = np.cos(self.rad_angle) * self.r
    y = np.sin(self.rad_angle) * self.r
    return (x + x_o, y + y_o)


    
def create_display(width, height):
  return pygame.display.set_mode((width,height))

def init_line(screen, bl):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.line(screen, (255, 0, 0), bl.origin, bl.get_point(), width=3)
  pygame.display.update()

# x = r cos(theta)
def rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])
  
def draw_step(screen, origin, point):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.line(screen, (255, 0, 0), origin, point, width=3)
  # pygame.display.update()
  # time.sleep(0.01)

def rotate(screen, base_line, target_point):
  t_x, t_y = target_point
  
  target_rad = np.arctan2(t_y - base_line.y_off_t, t_x - base_line.x_off_t)
  rotation = target_rad - base_line.rad_angle
  moves = abs(rotation * 180 / np.pi)
  if abs(moves) > 180:
    moves = 360 - abs(moves)
  increment = rotation / moves
  
  new_point_set = []
  x_o,y_o = base_line.x_off_t, base_line.y_off_t
  new_point_set = [base_line.get_point()]
  print(f'moves: {moves}')
  for i in range(int(moves)):
    # for p in point_set:
    lp_x, lp_y = new_point_set[-1]
    step = np.matmul(rotation_matrix(increment),np.array([[lp_x - x_o], [lp_y - y_o]]))
    new_point_set.append((step[0][0] + x_o, step[1][0]+ y_o))
  
  base_line.rad_angle = target_rad
  new_point_set.append(base_line.get_point())

  for p in range(len(new_point_set)):
    print(f'{p}\t {new_point_set[p]}')
    draw_step(screen, base_line.origin, new_point_set[p])
    pygame.draw.circle(screen,(0,255,0), (t_x, t_y), 2)
    pygame.display.update()
    time.sleep(0.01)
  return 1

def deg_to_rad(deg):
  return deg * (np.pi / 180)

def rad_to_deg(rad):
  return rad * (180 / np.pi)


def main():
  w, h = 500,500
  pygame.init()
  screen = create_display(w, h)
  off_t = 250
  origin = [off_t,off_t]
  r = 50
  base_line = line(origin, r)
  
  # base_line.off_t = off_t
  

  init_line(screen, base_line)
  
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        posn = pygame.mouse.get_pos()
        rotate(screen, base_line, posn)

main()
