#!/usr/bin/python3
from support.render_support import PygameArtFxns as pafn
from support.render_support import GeometryFxns as gfn
from support.render_support import MathFxns
from support.render_support import TransformFxns as tfn
from support.Link import Link

class Chain:
  def __init__(self, origin = (0,0), anchor = Link()):
    self.links = [anchor]
    self.links[-1].prev = self.links[-1]
    self.links[-1].endpoint = origin
    self.origin = origin

  def get_chain_point_sets(self):
    '''
    Accessor for all points in the chain
    Returns a list of point sets
    '''
    ptlist = []
    for link in self.links:
      ptlist.append(link.get_points())
    return ptlist

  def get_chain_normals(self):
    '''
    Accessor for all coordinate axes in the chain
    Returns a list of pairs of points
    '''
    ptlist = []
    for link in self.links:
      ptlist.append(link.get_normals())
    return ptlist

  def add_link(self, link):
    '''
    Adds a link to the chain
    Does not return
    '''
    link.prev = self.links[-1]
    self.links[-1].next = link
    self.links.append(link)

  def get_anchor_origin(self):
    return self.origin