#!/usr/bin/python3
import pygame
import sys
sys.path.append("./support")
#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import time
import sys
import numpy as np
from Polygon import *
from polygon_debugging import *
from BoundaryVertex import BoundaryVertex

de = DoublyConnectedEdgeList()

def get_polygons():
  rhombus = Polygon()
  rhombus.color = pafn.colors["red"]
  
  reversed(x)
  shape_1 = Polygon(x)
  shape_1.color = pafn.colors["green"]
  shape_2 = Polygon()
  shape_2.color = pafn.colors["cyan"]
  shapes = [rhombus, shape_1, shape_2]
  return shapes

def get_vertical_angles(p, n):
  PI_OVER_2 = np.divide(np.pi, 2)
  if n == p:
    if n < 3:
      return [PI_OVER_2]
    else:
      return [-PI_OVER_2]

  if n == 1 and p == 2:
    return [PI_OVER_2]

  if n == 1 and p == 3:
    return [PI_OVER_2, -PI_OVER_2]

  if n == 1 and p == 4:
    return []

  if n == 2 and p == 1:
    return [PI_OVER_2]

  if n == 2 and p == 2:
    return [PI_OVER_2]

  if n ==2 and p == 3:
    return [PI_OVER_2, -PI_OVER_2]

  if n == 2 and p == 4:
    return [PI_OVER_2, -PI_OVER_2]

  if n == 3 and p == 1:
    return [PI_OVER_2, -PI_OVER_2]

  if n == 3 and p == 2:
    return []

  if n == 3 and p == 3:
    return [-PI_OVER_2]

  if n == 3 and p == 4:
    return [-PI_OVER_2]

  if n == 4 and p == 1:
    return [PI_OVER_2, -PI_OVER_2]

  if n == 4 and p == 2:
    return [PI_OVER_2, -PI_OVER_2]

  if n == 4 and p == 3:
    return [-PI_OVER_2]


def get_norm_quadrant(v1, v2):
  unit_norm = gfn.get_unit_normal(v1.get_point_coordinate(), v2.get_point_coordinate())
  quad = gfn.get_cartesian_quadrant(unit_norm)
  return quad


def gen_bv(he, bv_list = []):
  v = he.source_vertex
  pv1, pv2 = he.get_prev_vertex_segment()
  pq = get_norm_quadrant(pv1,pv2)
  nv1, nv2 = he.get_next_vertex_segment()
  nq = get_norm_quadrant(nv1, nv2)
  angles = get_vertical_angles(pq, nq)
  if len(angles):
    bv_list.append(BoundaryVertex(v, angles))
  


  

def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    # s = get_polygons()
    # print(len(s))
    face_ids = []
    # for i in range(len(s)):
    #   s[i].dump_points()
    #   face_ids.append(de.create_new_face(s[i].dump_points()))
    de.create_new_face([(226, 280), (778, 284), (670, 711), (136, 706)])
    de.create_new_face([(285, 579), (430, 622), (345, 515), (485, 333),(260, 393)])
    de.create_new_face([(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)])


    fw = de.get_face_vertices_walk()
    boundary_vertices = []
    vlist = []
    for face_vertices in fw:
      for v in face_vertices:
        vlist.append(v)

      for vertex in face_vertices:
        pafn.frame_draw_ray(screen, vertex.get_point_coordinate(), vertex._half_edge._next.source_vertex.get_point_coordinate(), pafn.colors["white"])

    pygame.display.update()

    time.sleep(1)
    # generate boundary vertices from edge walks
    ew = de.get_face_edges_walk()
    for face_edges in ew:
      for he in face_edges:
        gen_bv(he, boundary_vertices)
    
    bsortkey = lambda bv: bv.vertex.rank
    
    vert_line = lambda pt: (mfn.pol2car(pt, 500, np.pi/2), mfn.pol2car(pt, 500, -np.pi/2))
    
    # rank the vertices by their x coordinate
    vsortkey = lambda v: v.get_point_coordinate()[0]
    vlist = sorted(vlist, key=vsortkey)
    for i in range(len(vlist)):
      vlist[i].rank = i
    
    for curr_rank in range(len(vlist)):
    
      valid_edges = []
      pafn.clear_frame(screen)
      
      for face_vertices in fw:
        for vertex in face_vertices:
          pafn.frame_draw_ray(screen, vertex.get_point_coordinate(), vertex._half_edge._next.source_vertex.get_point_coordinate(), pafn.colors["white"])
      cr = curr_rank
      
      
      for bv in boundary_vertices: 
        
        # check if boundary vertex rank is at least and at most curr_rank
        seg_if_rank = bv.get_segment_if_rank(curr_rank)

        for segment in seg_if_rank:
          valid_edges.append(segment)

        if len(seg_if_rank):
          pafn.frame_draw_dot(screen, bv.vertex.get_point_coordinate(), pafn.colors["red"])
        if bv.vertex.rank == curr_rank:
          # pafn.frame_draw_cross(screen, bv.vertex.get_point_coordinate(), pafn.colors["yellow"])
          vec_list = bv.get_vertical_vectors()
          for vl in vec_list:
            pafn.frame_draw_line(screen, vl, pafn.colors["lightslategray"])
          
      for seg in valid_edges:
        pafn.frame_draw_bold_line(screen, seg, pafn.colors["green"])
      pafn.frame_draw_cross(screen, vlist[cr].get_point_coordinate(), pafn.colors["tangerine"])
      pygame.display.update()
      
      time.sleep(0.5)
    
    
    time.sleep(5)
    
    sys.exit()

if __name__ == '__main__':
  main()