#!/usr/bin/python3

import numpy as np

class Point:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y
  
  def get_point(self):
    return (self.x, self.y)
  
  def dump(self):
    return f"{self.get_point()}"
