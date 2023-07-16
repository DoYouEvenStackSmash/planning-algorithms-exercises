#!/usr/bin/python3
import pygame
import sys
sys.path.append("./support")
sys.path.append("./DCEL")
from env_init import *
# from BoundaryVertex import BoundaryVertex
# from DCEL import *

from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
# from cell_decomp_support import VerticalCellDecomposition as vcd
import numpy as np
import time
from V import V
def adjust_angle(theta):
  """
  adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
  """
  if theta > np.pi:
      theta = theta + -2 * np.pi
  elif theta < -np.pi:
      theta = theta + 2 * np.pi

  return theta

def draw_component(screen, edge_list, color=pafn.colors["white"]):
    # color = colors[x]
    pl = [e.get_source_vertex().get_point_coordinate() for e in edge_list]
    for i in range(1, len(pl)):
      pafn.frame_draw_ray(screen, pl[i - 1], pl[i], color)
    pafn.frame_draw_ray(screen, pl[-1], pl[0], color)
  # pygame.display.update()

# def calc_face_split(edge_list, C, angles=[np.pi/4, -3 * np.pi/4]):
#     # edge_list = face.get_half_edges()
#     split_vertices = []
#     for angle in angles:
#         for e in edge_list:
#           A = e.get_source_vertex()
#           B = e._next.get_source_vertex()          
#           if vcd.test_for_intersection(A.get_point_coordinate(), B.get_point_coordinate(), C, angle):
#               split_vertices.append(vcd.get_intersection_pt(A.get_point_coordinate(), B.get_point_coordinate(), C, angle))
#     return split_vertices  


def cut_face(screen, dcel):
  f_id = 0
  fr = dcel.face_records[f_id]

  ipl = fr.get_interior_component_chains()
  ipl.append(fr.get_boundary_chain())
  colors = [pafn.colors["cyan"], pafn.colors["magenta"], pafn.colors["white"]]
  for i,el in enumerate(ipl):
    draw_component(screen, el, colors[i])
  pygame.display.update()
  angle = np.pi / 4
  vert_line = lambda pt: (mfn.pol2car(pt, 500, angle), mfn.pol2car(pt, 500, adjust_angle(np.pi + angle)))
  # time.sleep(3)
  # sys.exit()
  while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pt = pygame.mouse.get_pos()
            for il in ipl:
              intersections = calc_face_split(il, pt)
              for ipt in intersections:
                  pafn.frame_draw_cross(screen, ipt, pafn.colors["red"])
            vl = vert_line(pt)
            pafn.frame_draw_line(screen, vl, pafn.colors["lightslategray"])
            pygame.display.update()

def calculated_face_cut(screen, dcel):
  distkey = lambda x: x[0]
  bv = vcd.get_boundary_vertices(dcel)
  print(len(bv))
  fr = dcel.face_records[0]
  ipl = fr.get_interior_component_chains()
  ipl.append(fr.get_boundary_chain())
  global_edge_list = []
  for il in ipl:
    for e in range(len(il)):
      global_edge_list.append(il[e])
  
  colors = [pafn.colors["cyan"], pafn.colors["magenta"], pafn.colors["white"]]
  for i,el in enumerate(ipl):
    draw_component(screen, el, colors[i])
  pygame.display.update()
  for v in bv:
    
    pt = v.vertex.get_point_coordinate()
    ipts = []
    print(v.angles)
    for va in v.angles:
      
      intersections = [[mfn.euclidean_dist(pt, i), i] for i in calc_face_split(global_edge_list, pt, [va])]
      # print(intersections)
      intersections = sorted(intersections, key=distkey)
      # for i in intersections:
        # ipts.append(i[1])
      # print(intersections[0][0])
      
      ipts.append(intersections[0][1])
    # print(ipts)
    print(len(ipts))
    for ipt in ipts:
      # print(ipt)
      mpt = gfn.get_midpoint(pt, ipt)
      pafn.frame_draw_cross(screen, mpt, pafn.colors["tangerine"])
      # pafn.frame_draw_bold_line(screen,[pt,ipt], pafn.colors["red"])
      
    
    # es = v.get_vertical_vectors()
    # for e in es:
    #   pafn.frame_draw_line(screen, e, pafn.colors["lightslategray"])
    pygame.display.update()
    time.sleep(0.5)
    # pafn.frame_draw_cross(screen, v.vertex.get_point_coordinate(), pafn.colors["cyan"])
  pygame.display.update()
  
  for curr_rank in range(len(dcel.vertex_records)):
    valid_edges = []
    pafn.clear_frame(screen)
    for i,el in enumerate(ipl):
      draw_component(screen, el, colors[i])
    for b in bv:
      seg_if_rank = b.get_segment_if_rank(curr_rank)
      for segment in seg_if_rank:
          valid_edges.append(segment)
      if len(seg_if_rank):
        pafn.frame_draw_dot(screen, b.vertex.get_point_coordinate(), pafn.colors["red"])
    for seg in valid_edges:
      pafn.frame_draw_bold_line(screen, seg, pafn.colors["green"])
    pygame.display.update()
    time.sleep(0.5)
  time.sleep(3)
  sys.exit()


def active_edge_traversal(screen,dcel):
  colors = [pafn.colors["cyan"], pafn.colors["magenta"], pafn.colors["white"]]
  
  bv = vcd.get_boundary_vertices(dcel)
  fr = dcel.face_records[0]
  ipl = fr.get_interior_component_chains()
  ipl.append(fr.get_boundary_chain())
  global_edge_list = []
  for il in ipl:
    for e in range(len(il)):
      global_edge_list.append(il[e])
  get_seg = lambda edge: (edge.source_vertex.get_point_coordinate(), edge._next.source_vertex.get_point_coordinate())
  
  for curr_rank in range(len(dcel.vertex_records)):
    #  = []
    pafn.clear_frame(screen)
    for i,el in enumerate(ipl):
      draw_component(screen, el, colors[i])
    valid_edges = get_active_edges(global_edge_list, curr_rank)
    for edge in valid_edges:
      pafn.frame_draw_bold_line(screen, get_seg(edge), pafn.colors["tangerine"])
    pygame.display.update()
    time.sleep(0.5)
  time.sleep(3)
  sys.exit()

def calculate_free_points(edge_list, boundary_vertex):
  ipts = []
  distkey = lambda x: x[0]
  pt = boundary_vertex.vertex.get_point_coordinate()
  for va in boundary_vertex.angles:
    intersections = [[mfn.euclidean_dist(pt, i), i] for i in calc_face_split(edge_list, pt, [va])]
    intersections = sorted(intersections, key=distkey)
    mpt = gfn.get_midpoint(boundary_vertex.vertex.get_point_coordinate(), intersections[0][1])
    ipts.append(mpt)
  return ipts

def check_for_free_path(edge_list, origin, angle, distance):
  distkey = lambda x: x[0]
  intersections = [[mfn.euclidean_dist(origin, i), i] for i in calc_face_split(edge_list, origin, [angle])]
  intersections = sorted(intersections, key=distkey)
  for dist,pts in intersections:
    if dist < distance:
      return False
    else:
      break
  return True

def construct_global_edge_list(dcel):
  gel = []
  for face in dcel.face_records:
    interior_chains = face.get_interior_component_chains()
    interior_chains.append(face.get_boundary_chain())
    for edge_list in interior_chains:
      for edge in edge_list:
        gel.append(edge)
  return gel


def event_active_edge_traversal(screen, dcel):
  colors = []
  for i in pafn.colors:
    if i == "black":
      continue
    colors.append(pafn.colors[i])
  boundary_events = vcd.get_boundary_vertices(dcel)
  fr = dcel.face_records[0]
  ipl = fr.get_interior_component_chains()
  ipl.append(fr.get_boundary_chain())
  global_edge_list = []
  for il in ipl:
    for e in range(len(il)):
      global_edge_list.append(il[e])
  # global_edge_list = dcel.construct_global_edge_list()

  get_seg = lambda edge: (edge.source_vertex.get_point_coordinate(), edge._next.source_vertex.get_point_coordinate())
  sortkey = lambda bv: bv.vertex.rank
  
  boundary_events = sorted(boundary_events, key=sortkey)
  
  last_layer = []
  curr_layer = []
  rank = sortkey(boundary_events[0])
  valid_edges = vcd.get_active_edges(global_edge_list, rank)
  fps = vcd.calculate_free_points(valid_edges, boundary_events[0])
  pairs = []
  for pt in fps:
    last_layer.append(pt)
  last_active_edges = valid_edges
  
  for i in range(1, len(boundary_events)):

    bv = boundary_events[i]
    pafn.clear_frame(screen)
    pafn.frame_draw_cross(screen, bv.vertex.get_point_coordinate(), pafn.colors["magenta"])
    for i,el in enumerate(ipl):
      draw_component(screen, el, colors[i])
    
    rank = sortkey(bv)
    
    valid_edges = vcd.get_active_edges(global_edge_list, rank)
    last_active_edges = vcd.get_past_edges(global_edge_list, rank)
    
    fps = vcd.calculate_free_points(valid_edges, bv)

    for j in range(len(fps)):
      pt = fps[j]
      if pt == None:
        continue
      pafn.frame_draw_cross(screen, pt, pafn.colors["cyan"])
      # ADDED = False
      for k in range(len(last_layer)):
        lpt = last_layer[k]
        if lpt == None:
          continue
        pafn.frame_draw_dot(screen, lpt, pafn.colors["red"])
        pygame.display.update()
        # time.sleep(0.5)
        theta, radius = mfn.car2pol(pt, lpt)
        if vcd.check_for_free_path(last_active_edges, pt, theta, radius):# and check_for_free_path(last_active_edges, pt, theta, radius):
          pairs.append([last_layer[k], pt])
          last_layer[k] = None
          # break
        
    for pt in fps:
      if pt != None:
        curr_layer.append(pt)

    for lpt in last_layer:
      # lpt = last_layer[j]
      if lpt == None:
        continue
      else:
        curr_layer.append(lpt)
    for pair in pairs:
      pafn.frame_draw_line(screen, (pair[0], pair[1]), pafn.colors["tangerine"])
    
    last_layer = curr_layer
    curr_layer = []

    pygame.display.update()
    time.sleep(0.5)

  pygame.display.update()
  # time.sleep(3)
  pafn.clear_frame(screen)
  for i,el in enumerate(ipl):
    draw_component(screen, el, colors[i])
  pygame.display.update()
  counter = 0
  # print(len(pairs))
  # while len(pairs) > 10 + len(last_layer) and counter < 1:
  pairs = clean_graph(pairs)
  #   counter += 1
  print(counter)
  # pl = clean_graph(pl)
  # pl = clean_graph(pl)
  
  return pairs
  # sys.exit()


def generically_display_face(screen, dcel):
  f_id = 0
  fr = dcel.face_records[f_id]
  el = fr.get_boundary_chain()
  pl = [e.get_source_vertex().get_point_coordinate() for e in el]
  for i in range(1, len(pl)):
    pafn.frame_draw_ray(screen, pl[i - 1], pl[i], pafn.colors["white"])
  pafn.frame_draw_ray(screen, pl[-1], pl[0], pafn.colors["white"])
  
  int_comp_list = fr.get_interior_component_chains()
  iptl = []
  for el in int_comp_list:
    iptl.append([e.get_source_vertex().get_point_coordinate() for e in el])
  colors = []
  for i in pafn.colors:
    if i == "black":
      continue
    colors.append(pafn.colors[i])
  for x in range(len(iptl)):
    interior_component = iptl[x]
    color = colors[x]
    for i in range(1, len(interior_component)):
      pafn.frame_draw_ray(screen, interior_component[i - 1], interior_component[i], color)
    pafn.frame_draw_ray(screen, interior_component[-1], interior_component[0], color)
  
  pygame.display.update()
  time.sleep(3)

def clean_graph(pairlist):
  
  sortkey = lambda pt: pt[0]
  adj_dict = {}
  vertex_list = []
  for pair in pairlist:
    pair = sorted(pair, key=sortkey)
    pt1, pt2 = pair
    if pt1 not in adj_dict:
      adj_dict[pt1] = len(vertex_list)
      vertex_list.append(V(pt1))
    v1 = vertex_list[adj_dict[pt1]]

    if pt2 not in adj_dict:
      adj_dict[pt2] = len(vertex_list)
      vertex_list.append(V(pt2))
    v2 = vertex_list[adj_dict[pt2]]
    v1.neighbor_dict[adj_dict[pt2]] = False
    v2.neighbor_dict[adj_dict[pt1]] = False
  
  edge_list = []
  q = [0]
  # while len(q):
  for k,v_idx in adj_dict.items():
    # v_idx = q.pop(0)
    v = vertex_list[v_idx]
    # while v.neighbor_counter < len(v.neighbor_dict)
    vlist = []
    for i in v.neighbor_dict:
      if not v.neighbor_dict[i]:
        vlist.append((mfn.euclidean_dist(vertex_list[i].pt, v.pt),i))
      vlist = sorted(vlist, key=sortkey)
      if len(vlist):
        # print(vlist)
        neighbor_idx = vlist[0][1]
        neighbor = vertex_list[neighbor_idx]
        neighbor.neighbor_dict[v_idx] = True
        v.neighbor_dict[neighbor_idx] = True
        edge_list.append((v.pt, neighbor.pt))
        # q.append(neighbor_idx)
  return edge_list




def gen_dcel():
  bc = [(159, 629), (332, 196), (427, 260), (581, 82), (765, 148), (628, 329), (534, 269), (460, 391), (608, 638), (427, 832)]
  dcel = DCEL()
  a = [(436, 754), (401, 674), (501, 667)]
  b = [(437, 326), (422, 380), (396, 334), (430, 291), (487, 286)]
  c = [(590, 242), (556, 163), (680, 198)]
  x = [(397, 605), (319, 661), (368, 549), (290, 570), (395, 458)]
  x.reverse()
  print(a)
  a.reverse()
  print(a)
  # sys.exit()
  b.reverse()
  c.reverse()
  dcel.create_face(bc, [
  [(308, 609), (257, 591), (323, 424), (199, 619)],
  x,
  a,
  b,
  c])
  return dcel
    

def main():
  pygame.init()
  screen = pafn.create_display(1000, 1000)
  pafn.clear_frame(screen)
  # dcel = DCEL()
  # time.sleep(2)
  # bc = [(226, 280), (778, 284), (670, 711), (136, 706)]
  # obs_1 = [(285, 579), (430, 622), (345, 515), (485, 333),(260, 393)]
  # obs_2 = [(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)]
  # f_id = dcel.create_face(bc, [obs_1, obs_2])
  dcel = gen_dcel()
  # generically_display_face(screen, dcel)
  # time.sleep(4)
  # sys.exit()
  # active_edge_traversal(screen, dcel)
  # pl = event_active_edge_traversal(screen, dcel)
  pl = vcd.build_roadmap(dcel)
  pl = clean_graph(pl)
  fr = dcel.face_records[0]
  ipl = fr.get_interior_component_chains()
  ipl.append(fr.get_boundary_chain())
  # colors = [pafn.colors["cyan"], pafn.colors["magenta"], pafn.colors["white"]]
  colors = []
  for i in pafn.colors:
    if i == "black":
      continue
    colors.append(pafn.colors[i])
  # colors.reverse()
  # c = []
  # for i in range(0, len(colors), 2):
  #   c.append(colors[i])
  # colors = c
  for i,el in enumerate(ipl):
      draw_component(screen, el, colors[i])
  for pair in pl:
    pafn.frame_draw_line(screen, pair, pafn.colors["white"])
    
  pygame.display.update()
  time.sleep(4)
  # cut_face(screen, dcel)
  # calculated_face_cut(screen, dcel)
  sys.exit()

if __name__ == '__main__':
  main()
  