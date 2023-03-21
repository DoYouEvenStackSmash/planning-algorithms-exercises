#!/usr/bin/python3
import pygame
from support.Polygon import Polygon
from polygon_debugging import *

from pygame_rendering.render_support import PygameArtFxns as pafn
from pygame_rendering.render_support import GeometryFxns as gfn
from pygame_rendering.render_support import MathFxns
from pygame_rendering.render_support import TransformFxns as tfn

LALT = 256
LSHIFT = 1
LCTRL = 64
SPACE = 32

def pygame_transform_voronoi_system_loop(screen, A, Olist):
  '''
  Driver function interactions between two polygons A and static O
  Mouse driven path following
  '''
  pts = []
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        # LCTRL for exit hotkey
        if pygame.key.get_mods() == LCTRL:
          sys.exit()
        
        ptlist = []
        
        counter = 0
        # construct the path
        while pygame.MOUSEBUTTONUP not in [event.type for event in pygame.event.get()]:
          continue
        p = pygame.mouse.get_pos()
        pts.append(p)

def main():
  pygame.init()
  screen = pafn.create_display(1000,1000)
  
  A = build_polygon(sys.argv[1])
  A.color = pafn.colors["green"]
  A.v_color = pafn.colors["cyan"]
  A.e_color = pafn.colors["tangerine"]
  sanity_check_polygon(screen,A)
  pygame.display.update()
  pygame_transform_voronoi_system_loop(screen, A, [])

if __name__ == '__main__':
  main()