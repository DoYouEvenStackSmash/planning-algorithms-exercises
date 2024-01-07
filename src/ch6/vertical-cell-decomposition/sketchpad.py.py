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

# def get_nearest(edge_list, pt):
#   el = []
#   vl = []
#   vset = set()
#   for a,b in edge_list:
#     if a not in vset:
#       vl.append((mfn.euclidean_dist(a,pt),a))
#       vset.add(a)
#     if b not in vset:
#       vl.append((mfn.euclidean_dist(b,pt),b))
#       vset.add(b)
#     if edge_region_test((a,b), pt):
#       el.append((mfn.euclidean_dist((get_normal_pt((a,b)),pt)),(a,b)))
#   sortkey = lambda e : e[0]
  
#   el = sorted(el,key=sortkey)
#   vl = sorted(vl,key=sortkey)
#   edist = float('Inf')
#   vdist = float('Inf')
#   if len(el):
#     edist = el[0][0]
#   vdist = vl[0][0]
#   if vdist < edist:
#     edge_list.append()
      
  
def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    e = [(300,600),(600,700)]
    pafn.frame_draw_line(screen, e, pafn.colors["white"]) 
    pt = (500,200)     
    pafn.frame_draw_cross(screen, pt, pafn.colors["cyan"])
    if edge_region_test(e,pt):
      ipt = get_normal_pt(e, pt)
      pafn.frame_draw_cross(screen, pt, pafn.colors["cyan"])
      pafn.frame_draw_line(screen, (pt, ipt), pafn.colors["tangerine"])
      print(ipt)
      b,e = break_edge(e,ipt)
      print(b)
      pafn.frame_draw_bold_line(screen, b, pafn.colors["red"])
      pafn.frame_draw_bold_line(screen, e, pafn.colors["yellow"])
    pygame.display.update()

    time.sleep(3)
    
if __name__ == '__main__':
  main()


