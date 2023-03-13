#!/usr/bin/python3
import pygame
import time
from render_support import PygameArtFxns as pafn
from render_support import GeometryFxns as gfn
from render_support import MathFxns
from render_support import TransformFxns as tfn
from objects import *
import sys
SAMPLE_RATE = 400
LALT = 256
LSHIFT = 1
LCTRL = 64
SPACE = 32

def draw_all_normals(screen, chain):
  '''
  Render function for all coordinate frames in a chain
  Does not return
  '''
  nl = chain.get_chain_normals()
  points = chain.get_chain_point_sets()
  for l in chain.links:
    n = l.get_normals()
    pafn.frame_draw_line(screen, (l.get_origin(), n[0]), pafn.colors['tangerine'])
    pafn.frame_draw_line(screen, (l.get_origin(), n[1]), pafn.colors['yellow'])
  pafn.frame_draw_dot(screen, chain.get_anchor_origin(), pafn.colors["cyan"])
  pafn.frame_draw_dot(screen, chain.links[2].get_endpoint(), pafn.colors["cyan"])


def draw_all_links(screen, chain):
  '''
  Render function for all polygon links in the chain
  Does not return
  '''
  points = chain.get_chain_point_sets()
  for p in range(1,len(points)):
    pafn.frame_draw_polygon(screen, points[p], pafn.colors["red"])

def rotate_chain(screen, chain, target_point, steps = 30):
  '''
  Rotates links in the chain as influenced by a target point
  Does not return
  Calls update
  '''
  rad1 = chain.links[1].get_relative_rotation(target_point)
  rad2 = chain.links[2].get_relative_rotation(target_point)
  rad2 = rad2 - rad1
  rot_mat1 = tfn.calculate_rotation_matrix(rad1)
  rot_mat2 = tfn.calculate_rotation_matrix(rad2)
  step = np.divide(rad1, steps)
  step2 = np.divide(rad2, steps)
  origin = chain.links[0].get_origin()
  for i in range(steps):
    for l in chain.links[1:]:
      l.rotate(origin, rot_mat1)
      l.rel_theta += step

    chain.links[2].rotate(chain.links[2].get_origin(), rot_mat2)
    chain.links[2].rel_theta += step2
    pafn.clear_frame(screen)
    draw_all_normals(screen, chain)
    draw_all_links(screen, chain)
    pygame.display.update()
    time.sleep(0.01)
      

def rotate_link_to_point(screen, chain, target_point, steps = 30, link_index=2):
  '''
  Rotate a single link
  Does not return
  '''
  rad = chain.links[link_index].get_relative_rotation(target_point)
  rot_mat = tfn.calculate_rotation_matrix(rad)
  step = np.divide(rad, steps)
  for i in range(steps):
    pafn.clear_frame(screen)
    chain.links[link_index].rotate(chain.links[link_index].get_origin(), rot_mat)
    chain.links[link_index].rel_theta += step
    draw_all_normals(screen, chain)
    draw_all_links(screen, chain)
    pygame.display.update()
    time.sleep(0.01)

def pygame_chain_main(screen, chain):
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
        # draw_all_normals(screen, chain)
        # for i in range(2):
        rotate_chain(screen,chain,p,steps=30)
        # rotate_link_to_point(screen, chain, p, steps=30)
        # draw_all_normals(screen, chain)
        

def main():
  pygame.init()
  screen = pafn.create_display(1000,1000)
  pts = [(300, 375),(500,400),(300,425)]
  pts2 = [(700, 375),(500,400),(700,425)]
  origin = (300,400)
  a = Link(point_set=[origin])

  c = Chain(origin = origin, anchor=a)
  l = Link(point_set=pts, endpoint=pts[1])
  e = Link(point_set=pts2, endpoint=(700,400))
  c.add_link(l)
  c.add_link(e)
  points = c.get_chain_point_sets()

  pafn.frame_draw_dot(screen, origin, pafn.colors["cyan"])
  for p in range(1, len(points)):
    pafn.frame_draw_polygon(screen, points[p], pafn.colors["red"])
  pygame.display.update()
  pygame_chain_main(screen, c)

if __name__ == '__main__':
  main()

