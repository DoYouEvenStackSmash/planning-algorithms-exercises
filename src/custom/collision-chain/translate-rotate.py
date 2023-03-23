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

def calculate_circles(screen, chain,target_point,DRAW=None):
  '''
  Calculates intersection point of outermost circle
  https://mathworld.wolfram.com/Circle-CircleIntersection.html
  
  Returns a list of 3 points, which describe the chord going through the lens.
  '''
  t_x,t_y = target_point
  rad,inner_len = MathFxns.car2pol(chain.links[1].get_origin(), chain.links[1].get_endpoint())
  rad2,outer_len = MathFxns.car2pol(chain.links[2].get_origin(), chain.links[2].get_endpoint())

  o_x,o_y = chain.get_anchor_origin()

  target_distance = np.sqrt(np.square(t_x - o_x) + np.square(t_y - o_y))
  x = np.divide((np.square(inner_len) + np.square(target_distance) - np.square(outer_len)), (2 * inner_len))
  
  y = np.sqrt(np.square(target_distance) - (np.divide(np.square(np.square(inner_len) + np.square(target_distance) - np.square(outer_len)), (4 * np.square(target_distance)))))
  max_radius = abs(outer_len)
  curr_radius = abs(outer_len - x)
  y = min(np.sqrt(abs(np.square(max_radius) - np.square(curr_radius))), y)
  ps = [(o_x + x, o_y + y), (o_x + x, o_y), (o_x + x, o_y - y)]
  if DRAW == None:
    return ps

  # # pps = transform_point_set(link, ps)
  pafn.clear_frame(screen)
  for i in ps:
    pafn.frame_draw_dot(screen, i, pafn.colors["magenta"])
  # return pps
  
  pafn.draw_circle(screen, target_distance, (o_x, o_y), pafn.colors["yellow"])
  pafn.draw_circle(screen, outer_len, chain.links[2].get_origin(), pafn.colors["cyan"])
  pafn.draw_circle(screen, x, (o_x, o_y), pafn.colors["green"])
  pygame.display.update()
  return ps

def draw_bundle(screen, chain, A = None):
  if A != None:
    sanity_check_polygon(screen, A)
  draw_all_normals(screen, chain)
  draw_all_links(screen, chain)

def rotate_two_link_chain(screen, chain, target_point, intermediate_point, steps = 30, A=None):
  '''
  Rotates links in the chain as influenced by a target point
  Does not return
  Calls update
  '''
  # rad1 = chain.links[1].get_relative_rotation(target_point)
  rad2 = chain.links[2].get_relative_rotation(intermediate_point) # exac
  rad1,tp = tfn.calculate_rotation(chain.get_anchor_origin(), target_point, intermediate_point)
  
  rot_mat1 = tfn.calculate_rotation_matrix(rad1,step_count=steps)
  rot_mat2 = tfn.calculate_rotation_matrix(rad2,step_count=steps)
  step = np.divide(rad1, steps)
  step2 = np.divide(rad2, steps)
  origin = chain.links[0].get_origin()
  v = 0
  for i in range(steps):
    for j in range(1,len(chain.links)):
      l = chain.links[j]
      # v = check_contact(screen, l, A)
      # if v < COLLISION_THRESHOLD:
      #   return v

      l.rotate_body(origin, rot_mat1)
      l.rel_theta += step
    # v = check_contact(screen, l, A)
    # if v < COLLISION_THRESHOLD:
    #   return v
      # continue
    chain.links[2].rotate_body(chain.links[2].get_origin(), rot_mat2)
    chain.links[2].rel_theta += step2
    
    if steps > 1:
      pafn.clear_frame(screen)
      draw_bundle(screen, chain, A)
      # sanity_check_polygon(screen, A)
      # draw_all_normals(screen, chain)
      # draw_all_links(screen, chain)
      pygame.display.update()
      time.sleep(0.005)
  return 0


def check_contact(screen, link, O):
  val = find_contact(build_star(link.get_body().get_front_edge(), O.get_front_edge()), screen, VERBOSE=True)
  return val

def pygame_chain_rotate(screen, chain):
  '''
  Driver function interactions between two polygons A and static O
  Mouse driven path following
  '''
  A = None
  step_count = 100
  k = 400
  new_theta = 0
  segment = 1
  pts = []
  origin = (k,k)
  lt = origin
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        # LCTRL for exit hotkey
        if pygame.key.get_mods() == LCTRL:
          sys.exit()
        if pygame.key.get_mods() == LALT:
          p = pygame.mouse.get_pos()

          ps = calculate_circles(screen, chain, p,DRAW=1)
          pygame.display.update()
          continue
        while pygame.MOUSEBUTTONUP not in [event.type for event in pygame.event.get()]:
          continue
        p = pygame.mouse.get_pos()
        
        pts.append(p)
        for i in range(1,len(pts)):
          pafn.frame_draw_line(screen, (pts[i-1],pts[i]), pafn.colors['green'])
        pafn.frame_draw_dot(screen, p, pafn.colors['green'])
        if len(pts) < 4:
          pygame.display.update()
          continue
        else:
          pafn.clear_frame(screen)
          ps = calculate_circles(screen, chain, pts[0])
          r,t = tfn.calculate_rotation(chain.get_anchor_origin(), chain.links[1].get_endpoint(), ps[1])
          rot_mat = tfn.calculate_rotation_matrix(r,step_count=1)
          ps = tfn.rotate_point_set(chain.get_anchor_origin(), ps, rot_mat)
          
          tp2 = ps[0]
          tp1 = pts[0]
          # rotate_chain(screen,chain,p,steps=30)
          v = rotate_two_link_chain(screen, chain, tp1,tp2, steps=40,A=A)
          draw_bundle(screen, chain, A)

          pygame.display.update()
  
          l1,l2,l3,m1,m2,mpts = gfn.cubic_lerp_calculate(pts)
          
          for i in range(len(mpts)):
            pafn.clear_frame(screen)
            p = mpts[i]
            for j in range(i,len(mpts)):
              pafn.frame_draw_dot(screen, mpts[j], pafn.colors["cyan"])

            ps = calculate_circles(screen, chain, p)
            r,t = tfn.calculate_rotation(chain.get_anchor_origin(), chain.links[1].get_endpoint(), ps[1])
            rot_mat = tfn.calculate_rotation_matrix(r,step_count=1)
            ps = tfn.rotate_point_set(chain.get_anchor_origin(), ps, rot_mat)
            
            tp2 = ps[0]
            tp1 = p

            v = rotate_two_link_chain(screen, chain, tp1,tp2, steps=1,A=A)
            draw_bundle(screen, chain, A)
            pygame.display.update()

              # continue
            for j in range(i,len(mpts)):
              pafn.frame_draw_dot(screen, mpts[j], pafn.colors["cyan"])
            pygame.display.update()
            time.sleep(0.01)
            # COLLISION_THRESHOLD = 5
          pts = []
        return

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
        return


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
  while 1:
    pygame_chain_move(screen, c)
    pygame_chain_rotate(screen, c)

def main():
  triple_polygon_mod()

if __name__ == '__main__':
  main()
