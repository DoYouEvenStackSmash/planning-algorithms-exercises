#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import time
import sys
import numpy as np
from graph_processing import *
sys.path.append("./support")
sys.path.append("./DCEL")
from helpers import *

from test_objects import *


def get_rand_sequence(k=32, ub=1000):
    """
    Generates a random sequence of floats between 0,1000
    returns a sequence of points
    """
    rng = np.random.default_rng(12345)
    rand_val = lambda: (rng.uniform()) *700 + 130
    pl = []
    for i in range(k):
        x = rand_val()-10
        y = rand_val()-10
        pl.append((x, y))
    return pl

rng = np.random.default_rng()
rand_val = lambda: (int(rng.uniform(0, 10)))

def ml(screen, start, goal, obs_edge_set, input_points):
    vlist = [V(start)]
    edge_set = set()
    global rand_val
    # reversed(input_points)
    el = None
    
    for i in range(len(input_points)):
        tpt = input_points[i]
        if rand_val() == 1:
            tpt = goal
        f = get_nearest_feature(vlist, edge_set, tpt)
        oreal = 0
        if len(f) > 1:
            vl1, vl2 = f
            v1, v2 = vlist[vl1], vlist[vl2]
            n = get_normal_pt((v1.pt, v2.pt), tpt)
            nv = V(n)
            nv_idx = len(vlist)
            vlist.append(nv)
            addV2E(vlist, edge_set, f, nv_idx)
            oreal+=1
            f = [nv_idx]
        sv_idx = f[0]
        foreal = len(edge_set)
        flag = check_path(vlist, obs_edge_set, sv_idx, tpt,edge_set)
        oreal += foreal - len(edge_set)
        for e in list(edge_set)[-oreal:]:
            p1, p2 = vlist[e[0]].pt, vlist[e[1]].pt
            pafn.frame_draw_line(screen, (p1,p2),pafn.colors["red"])
        if tpt == goal and flag:
            pth = get_path(build_inverted_tree(list(edge_set), 0), 0, len(vlist)-1)
            for j,p in enumerate(pth):
                pafn.frame_draw_bold_line(screen, [vlist[p[0]].pt, vlist[p[1]].pt], pafn.colors["lawngreen"])                
            break
    
        
get_adj_succ = lambda p: p.get_half_edge().get_next_half_edge().get_source_vertex()
get_adj_pred = lambda p: p.get_half_edge().get_prev_half_edge().get_source_vertex()
v2pt = lambda p: p.get_point_coordinate()
edge_vtx = lambda e: e.get_source_vertex()

def main():

    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    ID, dcel = sq_test_obj()
    oel = dcel.construct_global_edge_list()
    obs_edge_set = set()
    for e in oel:
        obs_edge_set.add((v2pt(edge_vtx(e)), v2pt(get_adj_succ(edge_vtx(e)))))
    input_points = get_rand_sequence(200)

    draw_face(screen, dcel, ID)
    pygame.display.update()
    s = (330,600)
    g = (700,400)
    last = None
    time.sleep(3)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
            goal = pygame.mouse.get_pos()
            if goal == last:
                continue
            last = goal
            pafn.clear_frame(screen)
            draw_face(screen, dcel, ID)
            ml(screen, g,goal,obs_edge_set,input_points)
            pafn.frame_draw_cross(screen, goal, pafn.colors["red"])

            pygame.display.update()
    
    pygame.display.update()
    time.sleep(3)


if __name__ == "__main__":
    main()
