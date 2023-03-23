#!/usr/bin/python3

import pygame
import time

# support functions
from support.unit_norms import *
from support.Polygon import *

from support.World import *
from support.star_algorithm import *
from support.doubly_connected_edge_list import *

# useful geometry functions
from pygame_rendering.render_support import PygameArtFxns as pafn
from pygame_rendering.render_support import GeometryFxns as gfn
from pygame_rendering.render_support import MathFxns
from pygame_rendering.render_support import TransformFxns as tfn

from voronoi_regions import *
from feature_markers import *
from polygon_debugging import *
from region_tests import *
from file_loader import *
from transform_polygon import *
from transform_system import *
from objects import *
import sys

VERBOSE = False
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
  # pafn.frame_draw_dot(screen, chain.links[2].get_endpoint(), pafn.colors["cyan"])


def draw_all_links(screen, chain):
  '''
  Render function for all polygon links in the chain
  Does not return
  '''
  points = chain.get_chain_point_sets()
  for p in range(len(points)):
    pafn.frame_draw_polygon(screen, points[p], pafn.colors["red"])

def construct_star_diagram(A, O):
  '''
  Get the minkowski sum of the two polygons
  Returns a list of points 
  '''
  sl = build_star(A.get_front_edge(),O.get_front_edge())

  obs_spc = derive_obstacle_space_points(sl)
  return obs_spc

def translate_chain(screen, chain, target_point, steps=30):
  link = chain.links[1]
  # x_disp, y_disp = tfn.get_translation_function(chain.get_anchor_origin(), target_point, steps)
  r,theta = get_polar_coord(chain.get_anchor_origin(), target_point)
  step_r = r / steps
  x_step = step_r * np.cos(theta)
  y_step = step_r * np.sin(theta)
  total_x, total_y = 0,0
  for i in range(steps):
    pafn.clear_frame(screen)
    total_x+=x_step
    total_y+=y_step
    for link in chain.links:
      
      pafn.clear_frame(screen)
      link.translate_body(x_step, y_step)
      
      draw_all_normals(screen, chain)
      draw_all_links(screen, chain)
      pygame.display.update()
      time.sleep(0.005)
  ax, ay = chain.get_anchor_origin()
  chain.origin = (ax + total_x, ay + total_y)
  # chain.anchor_origin = chain.origin
  

def pygame_chain_move(screen, chain):
  '''
  Driver function interactions between two polygons A and static O
  Mouse driven path following
  '''
  pts = []
  mod = 0
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
        translate_chain(screen, chain, p, 1)


def triple_polygon_mod():
  pygame.init()
  screen = pafn.create_display(1000,1000)
  pts = [(300, 375),(500,400),(300,425)]
  pts2 = [(700, 375),(520,400),(700,425)]
  origin = (300,400)
  opts = [origin, (301,401), (302,402)]
  ap = Polygon(opts)
  ap.color = pafn.colors["green"]
  ap.v_color = pafn.colors["cyan"]
  ap.e_color = pafn.colors["tangerine"]
  a = Link(endpoint = origin, rigid_body = ap)
  A = Polygon(pts)
  B = Polygon(pts2)
  A.color = pafn.colors["green"]
  A.v_color = pafn.colors["cyan"]
  A.e_color = pafn.colors["tangerine"]
  # sanity_check_polygon(screen,A)
  c = Chain(origin = origin, anchor=a)
  l = Link(endpoint=pts2[1], rigid_body = A)
  B.color = pafn.colors["green"]
  B.v_color = pafn.colors["cyan"]
  B.e_color = pafn.colors["tangerine"]
  e = Link(endpoint = (700,400), rigid_body = B)
  c.add_link(l)
  c.add_link(e)
  # draw_bundle(screen, chain, A)
  draw_all_normals(screen, c)
  draw_all_links(screen, c)
  
  pygame.display.update()
  # start pygame loop
  pygame_chain_move(screen, c)

def main():
  triple_polygon_mod()

if __name__ == '__main__':
  main()
