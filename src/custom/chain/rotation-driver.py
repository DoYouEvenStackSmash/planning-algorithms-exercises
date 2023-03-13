#!/usr/bin/python3
import pygame
import time
from render_support import PygameArtFxns as pafn
from render_support import GeometryFxns as gfn
from render_support import MathFxns
from render_support import TransformFxns as tfn
import sys
SAMPLE_RATE = 400
LALT = 256
LSHIFT = 1
LCTRL = 64
SPACE = 32

def gradual_rotation(screen, new_point_set, origin, p, lt, step_count = 30):
  '''
  Computes and renders an animated rotation of a point set from 
  last target to new target.
  Returns a new point set and the new target point
  '''
  new_theta,lt = tfn.calculate_rotation(origin,p,lt)
  rot_mat = tfn.calculate_rotation_matrix(new_theta, step_count)
  for i in range(step_count):
    pafn.clear_frame(screen)
    new_point_set = tfn.rotate_point_set(origin, new_point_set, rot_mat)
    pafn.frame_draw_polygon(screen, new_point_set, pafn.colors["red"])
    pafn.frame_draw_dot(screen, origin, pafn.colors["yellow"])
    pafn.frame_draw_line(screen, (origin,lt), pafn.colors["indigo"])
    pygame.display.update()
    time.sleep(0.001)
  return new_point_set,lt



def pygame_path_main(screen, point_set):
  '''
  Driver function interactions between two polygons A and static O
  Mouse driven path following
  '''
  step_count = 100
  k = 400
  new_theta = 0
  segment = 1
  origin = (k,k)
  lt = origin
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        # LCTRL for exit hotkey
        if pygame.key.get_mods() == LCTRL:
          sys.exit()
        if pygame.key.get_mods() == LALT:
          pafn.clear_frame(screen)
          pafn.frame_draw_polygon(screen, point_set, pafn.colors["red"])
          pygame.display.update()
          continue
        while pygame.MOUSEBUTTONUP not in [event.type for event in pygame.event.get()]:
          continue
        p = pygame.mouse.get_pos()
        point_set,lt = gradual_rotation(screen, point_set, origin, p, lt, step_count)

def main():
  pygame.init()
  screen = pafn.create_display(800,800)
  pts = [(300, 375),(500,400),(300,425)]
  reversed(pts)
  pafn.frame_draw_polygon(screen, pts, pafn.colors["red"])
  pygame.display.update()
  pygame_path_main(screen, pts)

if __name__ == '__main__':
  main()
  