#!/usr/bin/python3
import pygame
import numpy as np
import sys
import time


from linkage import *

colors = {
  "black" : (0,0,0),
  "yellow" : (255,255,0),
  "cyan" : (0,255,255),
  "green" : (0,255,0),
  "magenta" : (255, 0, 255)
}

def create_display(width, height):
  return pygame.display.set_mode((width, height))

def draw_circle(screen, radius, center, color = (0,0,0)):
  pygame.draw.circle(screen, color, center, radius, 1)
  pygame.display.update()

def draw_polygon(screen, point_set):  
  pygame.draw.polygon(screen, (255,0,0), point_set, width=2)
  pygame.display.update()

def draw_frame(screen, polygons):
  pygame.Surface.fill(screen, (0,0,0))
  for i in range(len(polygons)):
    draw_polygon(screen, [j.get_coord() for j in polygons[i].get_point_set()])
    draw_origin_dot(screen, polygons[i].get_origin().get_coord())
  pygame.display.update()

def draw_origin_dot(screen, dot_pt, color = (0,0,255)) :
  pygame.draw.circle(screen, color, dot_pt, 2)
  pygame.display.update()

def draw_dot(screen, dot_pt):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.circle(screen, (0,255,0), dot_pt, 2)
  pygame.display.update()

def draw_red_dot(screen, dot_pt):
  pygame.Surface.fill(screen, (0,0,0))
  pygame.draw.circle(screen, (255,0,0), dot_pt, 2)
  pygame.display.update()

'''
  computes counterclockwise rotation matrix.
'''
def get_cc_rotation_matrix(rad_theta):
  return np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])

'''
  rotate a single link object about some origin point, as described by the rotation_matrix
'''
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

'''
  apply a rotation to base_link to align with target_point, 
    and update coordinate systems of all attached links 
'''
  # return new_point_set
def rotate_chain(base_link, target_point, screen = None, cl = None):
  origin = base_link.get_origin()
  prev_rad = base_link.get_relative_rad_angle() - base_link.get_local_rad_angle()
  target_rad = base_link.compute_rotation_rad(target_point)

  moves = abs(target_rad * 180 / np.pi)
  
  if int(moves) == 0:
    moves = 1
  
  step_rad = target_rad / moves
  # if screen
  r_step_theta = get_cc_rotation_matrix(step_rad)
  # r_theta = get_cc_rotation_matrix(target_rad)
  for i in range(int(moves)):
    link = base_link
    while link != None:
      rotate_link(origin, link, r_step_theta)
      link = link.m_next
    # correct for constantly increasing radian thing
    if (base_link.get_local_rad_angle() + step_rad > np.pi):
      base_link.set_rad_angle( -2 * np.pi + base_link.get_local_rad_angle() + step_rad)
    elif (base_link.get_local_rad_angle() + step_rad < -np.pi):
      base_link.set_rad_angle( 2 * np.pi + base_link.get_local_rad_angle() + step_rad)
    else:
      base_link.set_rad_angle(step_rad + base_link.get_local_rad_angle())
    draw_frame(screen, cl)
    time.sleep(0.01)

'''
  embedding a point into the body frame of base_link, by rotating about base_link origin

  transforms a single point from world frame to body frame of base link
'''
def transform_point(base_link, target_point):
  o_x, o_y = base_link.get_origin().get_coord()
  lp_x, lp_y = target_point

  r_m = get_cc_rotation_matrix(base_link.get_local_rad_angle())
  step = np.matmul(r_m, np.array([[lp_x - o_x], [lp_y - o_y]]))
  return Point(step[0][0] + o_x, step[1][0] + o_y)

'''
  embedding a point set into the body frame of base_link, by rotating about base_link origin
'''
def transform_point_set(base_link, point_set):
  o_x, o_y = base_link.get_origin().get_coord()
  r_m = get_cc_rotation_matrix(base_link.get_local_rad_angle())
  nps = []
  for p in point_set:
    lp_x, lp_y = p
    step = np.matmul(r_m, np.array([[lp_x - o_x], [lp_y - o_y]]))
    nps.append(Point(step[0][0] + o_x, step[1][0] + o_y))
  return nps


'''
  using target_point from world frame as a guide, determines reachable target point for base_link end member
'''
def radius_target_point(base_link, target_point):
  pps = target_point_set(base_link, target_point)
  chosen_point = pps[0]
  if abs(base_link.compute_rotation_rad(pps[-1].get_coord())) < abs(base_link.compute_rotation_rad(chosen_point.get_coord())):
    chosen_point = pps[-1]
  if abs(base_link.compute_rotation_rad(pps[1].get_coord())) < abs(base_link.compute_rotation_rad(chosen_point.get_coord())):
    chosen_point = pps[1]
  return chosen_point

'''
  transforms world frame target point to body_frame target point set.
'''
def target_point_set(base_link, target_point):
  t_x, t_y = target_point
  link = base_link
  while link.m_prev != None:
    link = link.m_prev
  
  o_x, o_y = link.get_origin().get_coord()
  inner_len = link.link_len
  outer_len = base_link.link_len

  target_distance = np.sqrt(np.square(t_x - o_x) + np.square(t_y - o_y))
  x = np.divide((np.square(inner_len) + np.square(target_distance) - np.square(outer_len)), (2 * inner_len))
  
  y = np.sqrt(np.square(target_distance) - (np.divide(np.square(np.square(inner_len) + np.square(target_distance) - np.square(outer_len)), (4 * np.square(target_distance)))))
  max_radius = abs(outer_len)
  curr_radius = abs(outer_len - x)
  # print(f"y:\t{y}\nmax_r:\t{max_radius}\ncurr_r:\t{curr_radius}")
  y = min(np.sqrt(abs(np.square(max_radius) - np.square(curr_radius))), y)
  ps = [(o_x + x, o_y + y), (o_x + x, o_y), (o_x + x, o_y - y)]
  pps = transform_point_set(link, ps)
  return pps

'''
  draw target circles
'''
def target_circle(screen, base_link, target_point):
  t_x, t_y = target_point
  link = base_link
  while link.m_prev != None:
    link = link.m_prev
  
  o_x, o_y = link.get_origin().get_coord()
  inner_len = link.link_len
  outer_len = base_link.link_len

  target_distance = np.sqrt(np.square(t_x - o_x) + np.square(t_y - o_y))
  x = np.divide((np.square(inner_len) + np.square(target_distance) - np.square(outer_len)), (2 * inner_len))
  
  y = np.sqrt(np.square(target_distance) - (np.divide(np.square(np.square(inner_len) + np.square(target_distance) - np.square(outer_len)), (4 * np.square(target_distance)))))
  max_radius = abs(outer_len)
  curr_radius = abs(outer_len - x)
  y = min(np.sqrt(abs(np.square(max_radius) - np.square(curr_radius))), y)
  draw_circle(screen, target_distance, (o_x, o_y), colors["yellow"])
  draw_circle(screen, outer_len, base_link.get_origin().get_coord(), colors["cyan"])
  draw_circle(screen, x, (o_x, o_y), colors["green"])

  ps = [(o_x + x, o_y + y), (o_x + x, o_y), (o_x + x, o_y - y)]
  pps = transform_point_set(link, ps)
  # tp = transform_point(link, (o_x + x, o_y))
  for i in pps:
    draw_origin_dot(screen, i.get_coord(), colors["magenta"])
  # draw_circle(screen, y, tp.get_coord(), colors["magenta"])

'''
  create a single rectangular link
'''
def create_link(origin, side_length, side_width, link_len = 0):
  back_two = [Point(origin.x - side_length/10, origin.y - side_width/2), Point(origin.x - side_length/10, origin.y + side_width/2)]
  front_two = [Point(origin.x + side_length + 5, origin.y - side_width/2), Point(origin.x + side_length + 5, origin.y + side_width/2)]
  point_set = [back_two[0], front_two[0], front_two[1], back_two[1]]
  new_link = Link(origin, link_len, 0, point_set)
  return new_link

def cheat_target_point(origin, rad_theta, end_point):
  r_m = get_cc_rotation_matrix(rad_theta)
  o_x, o_y = origin
  lp_x, lp_y = end_point
  step = np.matmul(r_m, np.array([[lp_x - o_x], [lp_y - o_y]]))
  return Point(step[0][0] + o_x, step[1][0] + o_y)

def cheat_target_angle(origin, start_point, target_point):
  o_x, o_y = origin
  a_x, a_y = start_point
  b_x, b_y = target_point
  base_rad = np.arctan2((a_y - o_y), (a_x - o_x))
  target_rad = np.arctan2((b_y - o_y), (b_x - o_x))
  rotation = target_rad - base_rad
  if rotation > np.pi:
    rotation = rotation - (2 * np.pi)
  if rotation < -np.pi:
    rotation = rotation + (2 * np.pi)
  
  return rotation
  

def calculate_angle(origin, start_point, target_point):
  o_x, o_y = origin
  a_x, a_y = start_point

  b_x, b_y = target_point

  h = np.sqrt(np.square(b_x - a_x) + np.square(b_y - a_y))

  r = np.sqrt(np.square(a_x - o_x) + np.square(a_y - o_y))

  theta = np.arcsin(h / (2 * r)) * 2

  return theta

def two_link():
  lalt = 256
  lshift = 1
  ctrl = 64
  w,h = 1000,1000
  screen = create_display(w,h)

  origin = Point(500,500)
  l,w = 100, 20
  link_1 = create_link(origin, l, w, 95)
  link_1.absolute_offset = origin
  x, y = link_1.get_end_point()
  link_2 = create_link(Point(x,y), l, w, 95)
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
        if pygame.key.get_mods() == ctrl:
          draw_origin_dot(screen, p, colors["yellow"])
          target_circle(screen, link_2, p)
          pt = radius_target_point(link_2, p)
          rotate_chain(link_2, pt.get_coord(), screen, cl)
          a = cheat_target_angle(link_1.get_origin().get_coord(), link_2.get_end_point(), p)
          apt = cheat_target_point(link_1.get_origin().get_coord(), a, link_1.get_end_point())
          rotate_chain(link_1, apt.get_coord(), screen, cl)
          draw_origin_dot(screen, p, colors["yellow"])
          draw_origin_dot(screen,pt.get_coord(), colors["cyan"])
          # print(f"angle: {a}")
          # print(f"{pt.get_coord()}, vs {link_2.get_end_point()}")
          
          continue
        # elif pygame.key.get_mods() == lalt:
        #   draw_origin_dot(screen, p)
        #   rotate_chain(link_2, p)
        #   print(f"link2:{link_2.get_local_rad_angle()}\nlink1:{link_1.get_local_rad_angle()}")
        #   # print(link_2.compute_rotation_rad(p))
        # # if pygame.key.get_pressed()[] == True:
        #   # draw_dot(screen, p)
        # elif pygame.key.get_mods() == lshift:
        #   draw_origin_dot(screen, p)
        #   rotate_chain(link_1, p)
        #   print(link_1.get_local_rad_angle())
        #   # print(link_1.compute_rotation_rad(p))
        #   # draw_red_dot(screen,p)
        # elif pygame.key.get_mods() == ctrl:

        #   print("nothing pressed")
        draw_frame(screen, cl)


def three_link():
  lalt = 256
  lshift = 1
  ctrl = 64
  w,h = 1000,1000
  screen = create_display(w,h)

  origin = Point(500,500)
  l,w = 100, 20
  link_1 = create_link(origin, l, w, 95)
  link_1.absolute_offset = origin
  x, y = link_1.get_end_point()
  link_2 = create_link(Point(x,y), l, w, 95)
  link_2.absolute_offset = origin
  link_2.m_prev = link_1
  link_1.m_next = link_2
  cl = [link_1, link_2]
  draw_frame(screen, cl)


def main():
  # w,h = 1000,1000
  pygame.init()
  two_link()
  # lalt = 256
  # lshift = 1
  # ctrl = 64

  # origin = [w/2,h/2]
  # screen = create_display(w,h)
  
  # origin = Point(500,500)
  # l,w = 100, 20
  # link_1 = create_link(origin, l, w, 95)
  # link_1.absolute_offset = origin
  # x, y = link_1.get_end_point()
  # link_2 = create_link(Point(x,y), l, w, 95)
  # link_2.absolute_offset = origin
  # link_2.m_prev = link_1
  # link_1.m_next = link_2
  # cl = [link_1, link_2]
  # draw_frame(screen, cl)


  # while 1:
  #   for event in pygame.event.get():
  #     if event.type == pygame.QUIT: 
  #       sys.exit()
  #     if event.type == pygame.MOUSEBUTTONUP:
  #       p = pygame.mouse.get_pos()
  #       if pygame.key.get_mods() == ctrl:
  #         draw_origin_dot(screen, p, colors["yellow"])
  #         target_circle(screen, link_2, p)
  #         pt = radius_target_point(link_2, p)
  #         rotate_chain(link_2, pt.get_coord(), screen, cl)
  #         a = cheat_target_angle(link_1.get_origin().get_coord(), link_2.get_end_point(), p)
  #         apt = cheat_target_point(link_1.get_origin().get_coord(), a, link_1.get_end_point())
  #         rotate_chain(link_1, apt.get_coord(), screen, cl)
  #         draw_origin_dot(screen, p, colors["yellow"])
  #         draw_origin_dot(screen,pt.get_coord(), colors["cyan"])
  #         # print(f"angle: {a}")
  #         # print(f"{pt.get_coord()}, vs {link_2.get_end_point()}")
          
  #         continue
  #       # elif pygame.key.get_mods() == lalt:
  #       #   draw_origin_dot(screen, p)
  #       #   rotate_chain(link_2, p)
  #       #   print(f"link2:{link_2.get_local_rad_angle()}\nlink1:{link_1.get_local_rad_angle()}")
  #       #   # print(link_2.compute_rotation_rad(p))
  #       # # if pygame.key.get_pressed()[] == True:
  #       #   # draw_dot(screen, p)
  #       # elif pygame.key.get_mods() == lshift:
  #       #   draw_origin_dot(screen, p)
  #       #   rotate_chain(link_1, p)
  #       #   print(link_1.get_local_rad_angle())
  #       #   # print(link_1.compute_rotation_rad(p))
  #       #   # draw_red_dot(screen,p)
  #       # elif pygame.key.get_mods() == ctrl:

  #       #   print("nothing pressed")
  #       draw_frame(screen, cl)

main()