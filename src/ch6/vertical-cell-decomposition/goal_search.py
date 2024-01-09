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

def get_nearest_vertex(ol, vpt_list, pt):
  
  vl = []
  vset = set()
  for i,x in enumerate(vpt_list):
    a = x
    if a not in vset:
      vl.append((mfn.euclidean_dist(a,pt),a,i))
      vset.add(a)

  sortkey = lambda e : e[0]
  vl = sorted(vl,key=sortkey)
  vc = 0
  while vc < len(vl):
    if not check_valid(ol, pt, vl[vc][1]):
      vc += 1
    else:
      return vl[vc][1]
  
def get_nearest(ol, edge_list, pt,offt=0):
  el = []
  vl = []
  vset = set()
  for i,x in enumerate(edge_list):
    a,b = x[0],x[1]
    if a not in vset:
      vl.append((mfn.euclidean_dist(a,pt),a,i))
      vset.add(a)
    if b not in vset:
      vl.append((mfn.euclidean_dist(b,pt),b,i))
      vset.add(b)
    if edge_region_test((a,b), pt):
      el.append((mfn.euclidean_dist(get_normal_pt((a,b),pt),pt),get_normal_pt((a,b),pt),i))
  sortkey = lambda e : e[0]
  
  el = sorted(el,key=sortkey)
  vl = sorted(vl,key=sortkey)
  edist = float('Inf')
  vdist = float('Inf')
  if len(el):
    edist = el[0][0]
  vdist = vl[0][0]
  vc = 0
  ec = 0
  while vc < len(vl) or ec < len(el):
    if vc < len(vl) and vl[vc][0] < edist:
      if not check_valid(ol, pt, vl[vc][1]):
        vc += 1
      else:
        return vl[vc][1]
    if vc < len(vl) and edist < vl[vc][0]:
      if not check_valid(ol, pt,el[ec][1]):
        ec += 1
      else:
        return (el[ec][1][0][0],el[ec][1][1][0])
      if ec < len(el):
        edist = el[ec][0]
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
