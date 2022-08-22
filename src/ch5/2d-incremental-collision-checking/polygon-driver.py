#!/usr/bin/python3

from polygon import *

import sys
import json
# def polygon_test(point_list):
class Point:
  def __init__(self, vec = []):
    self.vec = vec
  
  def get_component_vec(self):
    return self.vec

def json_point_unpack(json_point_list):
  pts = []
  for p in json_point_list:
    pts.append(Point([p['x'], p['y']]))
  return pts

def load_json_file(f):
  s = json.load(f)
  # print(s)
  f.close()
  if "points" not in s:
    print(f"No points field in s!\n{s}")
    sys.exit()
  p = json_point_unpack(s['points'])
  return p

def init_polygon(point_list):
  P = Polygon(point_list)
  print(P._id)
  print(P.dump_points())

def main():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  f = None
  f = open(sys.argv[1], 'r')
  if not f:
    print(f"could not find {sys.argv[1]}.")
    sys.exit()
  
  init_polygon([i.get_component_vec() for i in load_json_file(f)])
  
  

main()