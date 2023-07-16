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
from cell_decomp_support import VerticalCellDecomposition as vcd
import time
import sys
import numpy as np
from Polygon import *
from polygon_debugging import *
from BoundaryVertex import BoundaryVertex

de = DoublyConnectedEdgeList()

def rhombus_cut(screen):
    # create test face
    # rhombus
    de.create_new_face([(226, 280), (778, 284), (670, 711), (136, 706)])
    el = de.get_face_edges(0)
    for e in el:
        p1, p2 = [v.get_point_coordinate() for v in e.get_next_vertex_segment()]
        pafn.frame_draw_ray(screen, p1, p2, pafn.colors["green"])
        pygame.display.update()
        # time.sleep(1)
    
    # # isolate target edges
    active_edges = [el[0], el[2]]
    for e in active_edges:
        p1, p2 = [v.get_point_coordinate() for v in e.get_next_vertex_segment()]
        pafn.frame_draw_ray(screen, p1, p2, pafn.colors["magenta"])
        pygame.display.update()
        # time.sleep(1)
    
    vtx = (500,500)
    # A,B = [v.get_point_coordinate() for v in el[2].get_next_vertex_segment()]
    
    A1 = (100,300)
    B1 = (650,450)
    L1 = [A1,B1]
    A2 = (400,510)
    B2 = (620,700)
    L2 = [A2,B2]
    sortkey = lambda pt: pt[1]
    # pts = sorted(pts)
    
    
    A,B = L1
    print(gfn.test_for_intersection(B,A,vtx,-np.pi/2))
    # pafn.frame_draw_ray(screen, A,B, pafn.colors["green"])
    A,B = [v.get_point_coordinate() for v in el[0].get_next_vertex_segment()]
    print(gfn.test_for_intersection(A,B,vtx,-np.pi/2))
    # ip = gfn.get_intersection_pt(A,B,vtx, -np.pi / 2)
    # pafn.frame_draw_cross(screen, ip, pafn.colors["cyan"])
    A,B = [v.get_point_coordinate() for v in el[0].get_next_vertex_segment()]
    print(gfn.test_for_intersection(A,B,vtx,np.pi/2))
    ip = gfn.get_intersection_pt(A,B,vtx, np.pi / 2)
    pafn.frame_draw_cross(screen, ip, pafn.colors["cyan"])
    # print(ip)
    # print(mfn.car2pol(v,ip))
    # pafn.frame_draw_line(screen, (v,ip), pafn.colors["white"])
    pafn.frame_draw_cross(screen, vtx, pafn.colors["yellow"])
    
    pygame.display.update()

    time.sleep(3)

    sys.exit()

def calc_face_split(face, C, angles=[np.pi/2, -np.pi/2]):
    edge_list = face.get_half_edges()
    split_vertices = []
    for angle in angles:
        for e in edge_list:
            A,B = e.get_next_vertex_segment()
            if vcd.test_for_intersection(A.get_point_coordinate(), B.get_point_coordinate(), C.get_point_coordinate(), angle):
                split_vertices.append(vcd.get_intersection_pt(A.get_point_coordinate(), B.get_point_coordinate(), C.get_point_coordinate(), angle))
    return split_vertices    
        
def calc_intersections(dcel, pt):
    f = de.get_faces(0)
    sv = calc_face_split(f[0], Vertex(pt))
    return sv

def triangle_cut(screen):
    de.create_new_face([(208, 497), (763, 136), (645, 666)])
    el = de.get_face_edges(0)
    for e in el:
        p1, p2 = [v.get_point_coordinate() for v in e.get_next_vertex_segment()]
        pafn.frame_draw_ray(screen, p1, p2, pafn.colors["green"])
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pt = pygame.mouse.get_pos()
                intersections = calc_intersections(de, pt)
                for ipt in intersections:
                    pafn.frame_draw_line(screen, (pt,ipt), pafn.colors["white"])
                pygame.display.update()
            
    pygame.display.update()
    time.sleep(3)
    sys.exit()


def insert_front_edge(curr_edge, new_vertex):

def edge_cut_test(screen):
    de.create_new_face([(208, 497), (763, 136), (645, 666)])
    el = de.get_face_edges(0)
    for e in el:
        p1, p2 = [v.get_point_coordinate() for v in e.get_next_vertex_segment()]
        pafn.frame_draw_ray(screen, p1, p2, pafn.colors["green"])
    pygame.display.update()
    e = el[0]
    p1, p2 = [v.get_point_coordinate() for v in e.get_next_vertex_segment()]
    mpt = gfn.get_midpoint(p1,p2)
    vmpt = Vertex(mpt)



def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    triangle_cut(screen)

if __name__ == '__main__':
    main()
