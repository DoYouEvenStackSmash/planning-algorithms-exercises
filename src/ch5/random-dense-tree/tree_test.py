#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import time
import sys
import numpy as np

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
    rand_val = lambda: (rng.uniform()) * ub#700 + 130
    pl = []
    for i in range(k):
        x = rand_val()-10
        y = rand_val()-10
        pl.append((x, y))
    return pl


def ml(screen, start, goal, obs_edge_set):
    input_points = get_rand_sequence(400)
    vlist = [V(start)]
    edge_set = set()
    rng = np.random.default_rng(32345)
    rand_val = lambda: (int(rng.uniform(0, 100)))
    for i in range(len(input_points)):
        tpt = input_points[i]
        if rand_val() == 1:
            tpt = goal
        f = get_nearest_feature(vlist, edge_set, tpt)
        # print(f)
        if len(f) > 1:
            vl1, vl2 = f
            v1, v2 = vlist[vl1], vlist[vl2]
            n = get_normal_pt((v1.pt, v2.pt), tpt)
            nv = V(n)
            # n = get_normal_pt()
            nv_idx = len(vlist)
            vlist.append(nv)
            addV2E(vlist, edge_set, f, nv_idx)
            f = [nv_idx]
        sv_idx = f[0]
        flag = check_path(vlist, obs_edge_set, sv_idx, tpt,edge_set)
        for e in edge_set:
            p1, p2 = vlist[e[0]].pt, vlist[e[1]].pt
            pafn.frame_draw_line(screen, (p1,p2),pafn.colors["red"])
        pygame.display.update()
        if tpt == goal and flag:
            print(i)
            break
    
        
get_adj_succ = lambda p: p.get_half_edge().get_next_half_edge().get_source_vertex()
get_adj_pred = lambda p: p.get_half_edge().get_prev_half_edge().get_source_vertex()
v2pt = lambda p: p.get_point_coordinate()
edge_vtx = lambda e: e.get_source_vertex()

def main():
    pl = get_rand_sequence(200)

    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    ID, dcel = sq_test_obj()
    oel = dcel.construct_global_edge_list()
    # el = []
    obs_edge_set = set()
    print(oel)
    for e in oel:
        obs_edge_set.add((v2pt(edge_vtx(e)), v2pt(get_adj_succ(edge_vtx(e)))))
        obs_edge_set.add((v2pt(edge_vtx(e)), v2pt(get_adj_pred(edge_vtx(e)))))

    # el =
    # screen = pafn.create_display(1000, 1000)
    draw_face(screen, dcel, ID)
    s = (330,600)
    g = (700,400)
    ml(screen, g,s,obs_edge_set)
    pafn.frame_draw_cross(screen, g, pafn.colors["green"])
    for p in pl:
        pafn.frame_draw_dot(screen, p, pafn.colors["tangerine"])
    pygame.display.update()
    time.sleep(3)


if __name__ == "__main__":
    main()
