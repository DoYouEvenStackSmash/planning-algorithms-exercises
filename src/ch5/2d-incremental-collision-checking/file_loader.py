#!/usr/bin/python3

from cgitb import text
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
    pts.append([p['x'], p['y']])
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

def unpack_text_point(text_point,delimiter = ','):
  point = text_point.split(delimiter)
  if text_point[0] == '(' and text_point[-1] == ')':
    point[0] = point[0].lstrip('(')
    point[-1] = point[-1].rstrip(')')
  return point

def load_text_file(filename):
  f = None
  f = open(filename, 'r')
  if not f:
    print(f"could not find {filename}.")
    return []
  s = f.readlines()
  f.close()
  
  delimiter = s[0].rstrip('\n')
  point_list = []
  for i in range(1,len(s)):
    # s[i] = s[i].rstrip('\n')
    point_list.append([int(i) for i in unpack_text_point(s[i].rstrip('\n'), delimiter)])
  return point_list

def build_point_list(filename):
  filetype = filename.split(".")[-1]
  if (filetype == "json"):
    point_list = load_json_file(filename)
  elif (filetype == "txt"):
    point_list = load_text_file(filename)
  else:
    print(f"file type not recognized:\t{filename}")
    point_list = []
  return point_list

def load_point_set(filename):
  return build_point_list(filename)
