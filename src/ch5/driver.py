#!/usr/bin/python3
from ctypes import sizeof
from polygon import *
from render_support import *
from point_file_loader import *
from primitive_support import *
from world import *
import sys
import time



# def draw_test_vectors(point_list):
  

def draw_polygon_by_points(screen, P):
  pts = P.dump_points()
  
  # draw_test_vectors(pts)
  color_arr = [colors["red"], colors["yellow"], colors["white"]]
  for i in range(1, len(pts)):
    frame_draw_dot(screen, pts[i - 1], color_arr[(i - 1) % len(color_arr)])
    frame_draw_dot(screen, pts[i - 1], colors["red"])
    pygame.display.update()
    time.sleep(.1)
    frame_draw_line(screen, (pts[i - 1], pts[i]), colors["green"])
    pygame.display.update()
    time.sleep(.1)
  frame_draw_dot(screen, pts[-1], colors["red"])
  frame_draw_line(screen, (pts[-1], pts[0]), colors["green"])
  pygame.display.update()

def adjust_points(point_list, center):
  adj_point_list = []
  for i in range(len(point_list)):
    x,y = point_list[i]
    adj_point_list.append([x + center, y + center])
  return adj_point_list




def main():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  p = load_json_file(sys.argv[1])
  if not len(p):
    print(f"json file did not load.")
    sys.exit()
  p = adjust_points(p, 250)
  # return
  
  P = Polygon(p)
  
  pygame.init()
  w, h = 500,500
  screen = create_display(w, h)
  draw_polygon_by_points(screen, P)
  W = World()
  pts = P.dump_points()
  s = P.dump_segments()
  for i,j in s:
    W.create_half_plane(i, j)
  # W.create_half_plane(pts[0], pts[1])
  for i,j in enumerate(pts):
    print(f"{i}:\t{j}")
  # frame_draw_polygon(screen, pts, colors["magenta"])
  lalt = 256
  lshift = 1
  ctrl = 64

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEBUTTONUP:
        p = pygame.mouse.get_pos()
        print(p)
        # if pygame.key.get_mods() == ctrl:
        val = W.test_set_of_planes(p)
        # val = W.test_plane(p, 0)
        if val < 0:
          print(f"{p} is right of the line")
          frame_draw_dot(screen, p, colors["cyan"])
        elif val > 0:
          print(f"{p} is left of the line")
          frame_draw_dot(screen, p, colors["magenta"])
        else:
          print(f"{p} is unknown?")
        pygame.display.update()
          


main()