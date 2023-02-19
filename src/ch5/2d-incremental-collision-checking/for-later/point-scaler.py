#!/usr/bin/python3

import sys
import json
import numpy as np
from file_loader import *

def get_polar_coord(origin, target):
  ox,oy = origin
  tx,ty = target
  dist = np.sqrt(np.square(tx - ox) + np.square(ty - oy))
  theta = np.arctan2(ty - oy, tx - ox)
  return (dist,theta)

def get_rectangular_coord(origin, radius, rad_theta):
  ox, oy = origin
  x = np.cos(rad_theta) * radius
  y = np.sin(rad_theta ) * radius
  return (ox + x, oy + y)

def move_point_list(point_list, x = 0, y = 0):
  for i in range(len(point_list)):
    px,py = point_list[i]
    point_list[i] = [px + x, py + y]
  return point_list


def scale(point_list, factor):
  
  origin = point_list[0]
  scaled_list = [origin]
  for i in point_list[1:]:
    r, theta = get_polar_coord(origin, i)
    scaled_list.append(get_rectangular_coord(origin, r * factor, theta))
  return scaled_list


# def build_multi_point_list():
  # for i in range(1, len(sys.argv)):
def build_point_list(i):
  filetype = sys.argv[i].split(".")[-1]
  if (filetype == "json"):
    point_list = load_json_file(sys.argv[i])
  elif (filetype == "txt"):
    point_list = load_text_file(sys.argv[i])
  else:
    print(f"file type not recognized:\t{sys.argv[i]}")
    point_list = []
  return point_list

def json_serializer(point_list, filename):
  new_filename = f"{filename.split('.')[0]}.json"
  pt_template = ['\"x\" : ', '\"y\" : ']
  f = open(new_filename, 'w')
  head = "{\n  \"points\": [\n"
  f.write(head)
  tail = "  ]\n}"
  for pt in point_list[0:-1]:
    pt_str = "    {" + f"{pt_template[0]}{pt[0]},{pt_template[1]}{pt[1]}" + "},\n"
    f.write(pt_str)
  pt = point_list[-1]
  pt_str = "    {" + f"{pt_template[0]}{pt[0]},{pt_template[1]}{pt[1]}" + "}\n"
  f.write(pt_str)
  f.write(tail)
  f.close()
  print(f"wrote new json file: {new_filename}")

def get_filename(i):
  return sys.argv[i]

def main():
  if len(sys.argv) < 2:
    print("Please enter a filename")
    sys.exit()
  i = 1
  pl = build_point_list(i)
  # pl = [i for i in reversed(pl)]
  pl = scale(pl, .8)
  # pl = move_point_list(pl, 200, 40)
  json_serializer(pl, get_filename(i))
  # pl = scale
  print(pl)

main()