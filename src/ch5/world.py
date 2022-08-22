#!/usr/bin/python3

import numpy as np
from primitive_support import *

class World:
  def __init__(self):
    self.half_planes = []
    # self.
  
  def create_half_plane(self, p1, p2):
    self.half_planes.append(create_edge(p1, p2))
  
  def test_points(self, p1, hp_id = 0):
    if len(self.half_planes) == 0:
      print("there are no half planes to test!")
      return None
    val = self.half_planes[hp_id].test_point(p1)
    print(val)
    return val