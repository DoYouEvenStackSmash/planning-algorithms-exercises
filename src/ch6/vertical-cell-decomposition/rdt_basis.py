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
from graph_processing import *
from cell_decomp_support import VerticalCellDecomposition as vcd
import numpy as np
import time
from goal_search import *

# from V import V
from aux_functions import *
from test_objects import *
from collections import deque
from graph_processing import *

def get_rand_sequence(k=32,ub = 1000):
    """
    Generates a random sequence of floats between 0,1000
    returns a sequence of points
    """
    rng = np.random.default_rng(12345)
    rand_val = lambda: (rng.uniform()) * ub
    pl = []
    for i in range(k):
        x = rand_val()
        y = rand_val()
        pl.append((x, y))
    return pl
  
def scale(pl,center=500, factor = 2):
    scalar = lambda val, c,f: (val - c) * f + c
    pl = [(scalar(x,center,factor),scalar(y,center,factor)) for (x,y) in pl]
    return pl

def get_nearest_landmark(obstacle_list, edges, pt, offt=0):
    """Given a list of edges and obstacles, finds the nearest valid point on the roadmap
        to pt. Could be a point on an edge, could be a vertex.

    Args:
        obstacle_list (_type_): half edge list
        edges (_type_): half edge list
        pt (_type_): point as (x,y)
        offt (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: point(x,y)
    """
    edge_list = []
    vertex_list = []
    vtx_set = set()
    for i, x in enumerate(edges):
        a, b = x[0], x[1]
        if a not in vtx_set:
            vertex_list.append((mfn.euclidean_dist(a, pt), a, i))
            vtx_set.add(a)
        if b not in vtx_set:
            vertex_list.append((mfn.euclidean_dist(b, pt), b, i))
            vtx_set.add(b)
        if edge_region_test((a, b), pt):
            edge_list.append(
                (
                    mfn.euclidean_dist(get_normal_pt((a, b), pt), pt),
                    get_normal_pt((a, b), pt),
                    (a,b),
                    i
                )
            )
    sortkey = lambda e: e[0]

    edge_list = sorted(edge_list, key=sortkey)
    vertex_list = sorted(vertex_list, key=sortkey)
    edist = float("Inf")
    vdist = float("Inf")
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
            if not check_valid(obstacle_list, pt, edge_list[edge_idx][1]):
                edge_idx += 1
            else:
                new_vtx = [edge_list[edge_idx][1][0][0], edge_list[edge_idx][1][1][0]]
                ne1, ne2 = break_edge(edge_list[edge_idx][2],new_vtx)
                edges[edge_list[edge_idx][-1]] = ne2
                edges.append(ne1)
                return new_vtx
            if edge_idx < len(edge_list):
                edist = edge_list[edge_idx][0]
            else:
                edist = float("Inf")

    return None

def textbook_obj_scaled():
    dcel = DCEL()
    bc = [(1, 1), (999, 1), (999, 999), (1, 999)]
    obs_1 = scale([(285, 579), (430, 622), (345, 515), (485, 333), (260, 393)])
    obs_2 = scale([(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)])
    ID = dcel.create_face(bc, [obs_1, obs_2])
    return ID, dcel
  
def main():
    pl = get_rand_sequence(100)
    
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    ID, dcel = textbook_obj_scaled()
    draw_face(screen, dcel, ID)
    obstacle_space = dcel.construct_global_edge_list()
    edge_list = [(700,800),(800,700)]
    start = (700,800)
    for p in pl:
        pafn.frame_draw_dot(screen, p, pafn.colors["tangerine"])
    pygame.display.update()
    time.sleep(3)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
            goal = tuple(pygame.mouse.get_pos())
            pafn.clear_frame(screen)
            draw_face(screen, dcel, ID)
            nearest_landmark = get_nearest_landmark(obstacle_space, edge_list, goal)
            if nearest_landmark == None:
                pafn.frame_draw_cross(screen, start, pafn.colors["red"])
                pafn.frame_draw_dot(screen, goal, pafn.colors["red"], True)
                pygame.display.update()
                continue
            
            

if __name__ == '__main__':
    main()