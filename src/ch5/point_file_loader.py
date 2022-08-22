#!/usr/bin/python3

import sys
import json

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

def load_json_file(filename):
  f = None
  f = open(filename, 'r')
  if not f:
    print(f"could not find {filename}.")
    # sys.exit()
    return []
  
  s = json.load(f)
  # print(s)
  f.close()
  if "points" not in s:
    print(f"No points field in s!\n{s}")
    return []
  p = json_point_unpack(s['points'])
  return p
  