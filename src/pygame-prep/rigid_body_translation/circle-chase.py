#!/usr/bin/python3
import time
import pygame
import sys
import numpy as np

# def translation((x, y), xt=0, yt=0):
# return (x + xt, y + yt)

def create_display(width, height):
  return pygame.display.set_mode((width,height))

def init_circle(screen):
  pygame.draw.circle(screen, (255,0,0), (0,0), 5)
  pygame.display.update()

def relocate_circle(screen, orig_center, new_center, max_y):
  pts = point_slope(orig_center, new_center)
  x2,y2 = int(new_center[0]),int(new_center[1])
  carry_x,carry_y = -1,-1
  for i in range(len(pts)):
    x,y = pts[i]
    if int(x) == carry_x and int(y) == carry_y:
      continue
    else:
      carry_x,carry_y = int(x), int(y)
    pygame.draw.circle(screen,(255,0,0), (carry_x, carry_y), 5)
    pygame.draw.circle(screen,(0,255,0), (x2, y2), 2)
    pygame.display.update()
    time.sleep(0.01)
    pygame.Surface.fill(screen,(0,0,0))
  
  return new_center


def point_slope(p1, p2):
  x1,y1 = p1
  x2,y2 = p2
  
  distance = np.sqrt(np.square((x2 - x1)) + np.square((y2 - y1)))
  delta_x = (x2 - x1) / int(distance)
  delta_y = (y2 - y1) / int(distance)
  # slope = (y2 - y1) / (x2 - x1)
  pts = [(x1, y1)]
  for i in range(int(distance)):
    pts.append((pts[-1][0] + delta_x, pts[-1][1] + delta_y))

  pts.append(p2)
  return pts
  

  
def main():
  w,h = 500,500
  pygame.init()
  screen = create_display(w,h)
  init_circle(screen)
  last_p = (0,0)
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      if event.type == pygame.MOUSEBUTTONUP: 
        last_p = relocate_circle(screen, last_p, pygame.mouse.get_pos(), h)
main()