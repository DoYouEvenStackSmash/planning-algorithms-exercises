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

de = DoublyConnectedEdgeList()

def get_polygons():
  rhombus = Polygon([(800.0, 400.0), (706.8251437630926, 747.7332974640647), (306.82514376309257, 747.7332974640647), (400.0, 400.00000000000006)])
  rhombus.color = pafn.colors["red"]
  shape_1 = Polygon([(521, 590), (561, 697), (445, 646), (428, 497), (596, 442)], -1)
  shape_1.color = pafn.colors["green"]
  shape_2 = Polygon([(568, 563), (661, 499), (682, 652), (600, 673), (623, 608)], -1)
  shape_2.color = pafn.colors["cyan"]
  shapes = [rhombus, shape_1, shape_2]
  return shapes

def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    s = get_polygons()
    print(len(s))
    face_ids = []
    for i in range(len(s)):
      s[i].dump_points()
      face_ids.append(de.create_new_face(s[i].dump_points()))
    
    

    # fp =
    # print(fp[0]._half_edge._bounded_face._id)
    # sys.exit()
    # print(de.face_records)
    # print(face_ids)
    hel = de.get_other_faces_edges(face_ids[0])
    # for el in hel:
    #   print(el)
    # sys.exit()
    for el in hel:
      for edge in el:
        vertex = edge.source_vertex
        print(vertex._half_edge._next.source_vertex)
        pafn.frame_draw_ray(screen, vertex.get_point_coordinate(), vertex._half_edge._next.source_vertex.get_point_coordinate(), pafn.colors["white"])
        pygame.display.update()
        time.sleep(0.3)

    # fw = de.get_faces_walk()
    # for face_vertices in fw:
    #   for vertex in face_vertices:
    #     pafn.frame_draw_ray(screen, vertex.get_point_coordinate(), vertex._half_edge._next.source_vertex.get_point_coordinate(), pafn.colors["white"])
    #     pygame.display.update()
    #     time.sleep(0.3)
    #   time.sleep(2)
    time.sleep(5)
    sys.exit()

if __name__ == '__main__':
  main()