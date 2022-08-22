#!/usr/bin/python3
class Obj:
  def __init__(self, x_min, x_max, y_min, y_max):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.x_identify = None
    self.y_identify = None
    self.next_segment = None
    self.end_flag = False

  # def get_next_x(self, x_curr):
  def get_x_borders(self):
    return [(self.x_min, self.y_min), (self.x_max, self.y_min), (self.x_min, self.y_max), (self.x_max, self.y_max)]
  
  def get_y_borders(self):
    return [(self.x_min, self.y_min),(self.x_min,self.y_max), (self.x_max, self.y_min), (self.x_max, self.y_max)]

  def is_complete(self):
    return self.end_flag

  def get_y_min(self):
    return self.y_min
  
  def get_x_min(self):
    return self.x_min

  def get_y_max(self):
    return self.y_max
  
  def get_x_max(self):
    return self.x_max

  def check_y_max(self, y_curr):
    return y_curr >= self.y_max  
  
  def check_x_max(self, x_curr):
    return x_curr >= self.x_max
  
  def check_y_min(self, y_curr):
    return y_curr <= self.y_min  
  
  def check_x_min(self, x_curr):
    return x_curr <= self.x_min
  
  def get_x_dist(self):
    return self.x_max - self.x_min
  
  def get_y_dist(self):
    return self.y_max - self.y_min
  
def blank_object(x_min, x_max, y_min, y_max):
  return Obj(x_min, x_max, y_min, y_max)