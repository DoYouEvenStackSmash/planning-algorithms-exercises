#!/usr/bin/python3
from vcd import *

def edge_region_test(edge, pt):
  a,b,c = cart2complex(pt,edge[0]),cart2complex(pt, edge[1]),cart2complex(edge[1],edge[0])
  if abs(np.angle(a / c)) < np.pi/2 and abs(np.angle(b / (c * np.exp(1j*np.pi)))) < np.pi / 2:
    return True
  return False

def break_edge(edge, pt):
  a1,a2 = pt
  a = [edge[1],(a1[0],a2[0])]
  edge = [edge[0],(a1[0],a2[0])]
  return a,edge

def get_normal_pt(edge, pt):
  a,b,c = cart2complex(pt,edge[0]),cart2complex(pt, edge[1]),cart2complex(edge[1],edge[0])
  h = mag(a)
  norm = lambda cv: cv / abs(cv)
  theta = abs(np.angle(a / c))
  d = h * np.cos(theta)
  npt = complex2cart(norm(c) * d,edge[0])
  return npt

def get_nearest_vertex(obstacle_list, vpt_list, pt):
  
  vertex_list = []
  vset = set()
  for i,v in enumerate(vpt_list):
    if v not in vset:
      vertex_list.append((mfn.euclidean_dist(v,pt),v,i))
      vset.add(v)

  sortkey = lambda e : e[0]
  vertex_list = sorted(vertex_list,key=sortkey)
  vtx_idx = 0
  while vtx_idx < len(vertex_list):
    if not check_valid(obstacle_list, pt, vertex_list[vtx_idx][1]):
      vtx_idx += 1
    else:
      return vertex_list[vtx_idx][1]
  
def get_nearest(obstacle_list, edges, pt,offt=0):
  edge_list = []
  vertex_list = []
  vset = set()
  for i,x in enumerate(edges):
    a,b = x[0],x[1]
    if a not in vset:
      vertex_list.append((mfn.euclidean_dist(a,pt),a,i))
      vset.add(a)
    if b not in vset:
      vertex_list.append((mfn.euclidean_dist(b,pt),b,i))
      vset.add(b)
    if edge_region_test((a,b), pt):
      edge_list.append((mfn.euclidean_dist(get_normal_pt((a,b),pt),pt),get_normal_pt((a,b),pt),i))
  sortkey = lambda e : e[0]
  
  edge_list = sorted(edge_list,key=sortkey)
  vertex_list = sorted(vertex_list,key=sortkey)
  edist = float('Inf')
  vdist = float('Inf')
  if len(edge_list):
    edist = edge_list[0][0]
  vdist = vertex_list[0][0]
  vtx_idx = 0
  edge_idx = 0
  while vtx_idx < len(vertex_list) or edge_idx < len(edge_list):
    if vtx_idx < len(vertex_list) and vertex_list[vtx_idx][0] < edist:
      if not check_valid(obstacle_list, pt, vertex_list[vtx_idx][1]):
        vtx_idx += 1
      else:
        return vertex_list[vtx_idx][1]
    if vtx_idx < len(vertex_list) and edist < vertex_list[vtx_idx][0]:
      if not check_valid(obstacle_list, pt,edge_list[edge_idx][1]):
        edge_idx += 1
      else:
        return (edge_list[edge_idx][1][0][0],edge_list[edge_idx][1][1][0])
      if edge_idx < len(edge_list):
        edist = edge_list[edge_idx][0]
      else: 
        edist = float('Inf')

  return None
        
def check_valid(edge_list, pt, ipt):
    
    for e in reversed(edge_list):
        a,b = mfn.car2pol(pt, ipt)
        if vcd.test_for_intersection(
            v2pt(edge_vtx(e)),
            v2pt(get_adj_succ(edge_vtx(e))),
            pt,
            a
        ):
            if mfn.euclidean_dist(get_normal_pt((v2pt(edge_vtx(e)),v2pt(get_adj_succ(edge_vtx(e)))),pt),pt) >= b:
                continue

            return False
    return True
