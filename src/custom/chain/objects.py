class Link:
  def __init__(self, point_set, dist = 1, origin = (0,0), _prev = None, _next = None, theta=0):
    self.origin = origin
    self.point_set = point_set
    self.rel_theta = theta
    self.dist = dist
    self.prev = _prev
    self.next = _next
  
  def get_point_set(self):
    return self.point_set
  
  def get_relative_angle(self):
    return self.rel_theta
  
  def get_origin(self):
    return self.origin
  
  def get_endpoint(self):
    return MathFxns.pol2car(self.origin, self.dist, self.rel_theta)[1]

  def new_orientation(self, origin, pts, theta):
    self.origin = origin
    self.point_set = point_set
    self.rel_theta = theta

class Chain:
  def __init__(self, origin = (0,0)):
    self.origin = origin
    self.links = []
  
  def get_links(self):
    ptlist = []
    for link in self.links:
      ptlist.append(link.get_point_set()):
    return ptlist
  
  def add_link(self, link):
    if not len(self.links):
      link.origin = self.origin
      self.links.append(link)
    else:
      link.origin = self.links[-1].get_endpoint()
      link.prev = self.links[-1]
      self.links[-1].next = link
      self.links.append(link)
