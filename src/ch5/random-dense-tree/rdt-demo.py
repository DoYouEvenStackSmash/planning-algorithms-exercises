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

sys.path.append("./DCEL")
from helpers import *

from test_objects import *

GOAL_SEEK_PROB = 0.33
rng = np.random.default_rng()
rand_val = lambda: (int(rng.uniform(0, int(GOAL_SEEK_PROB * 100))))

DEBUG = True


def RDT_loop(screen, start, goal, obs_edge_set, input_points, obstacle_vertex_list):
    """
    Given a start and goal, construct an RDT over the world in search of the goal
    """
    vlist = [V(start)]
    edge_set = set()
    global rand_val
    el = None
    # randvals = [rand_val() for _ in range(len(input_points))]
    i = 0

    # i+=1
    while i < len(input_points):
        tpt = input_points[i]
        # beeline for the goal
        if rand_val() == 1:
            tpt = goal
            i = i - 1
        else:
            f2 = get_nearest_feature(obstacle_vertex_list, obs_edge_set, tpt)
            n = None
            if len(f2) > 1:
                n = get_normal_pt(
                    (obstacle_vertex_list[f2[0]].pt, obstacle_vertex_list[f2[1]].pt),
                    tpt,
                )
            else:
                n = obstacle_vertex_list[f2[0]].pt
            if dist(tpt, n) < 1:
                i += 1
                continue

        f = get_nearest_feature(vlist, edge_set, tpt)

        # nearest feature is an edge
        if len(f) > 1:
            # vl1, vl2 = f
            # v1, v2 = vlist[f[0]], vlist[f[1]]
            n = get_normal_pt((vlist[f[0]].pt, vlist[f[1]].pt), tpt)
            # nv = V(n)
            nv_idx = len(vlist)
            vlist.append(V(n))
            # break the edge at the normal point
            addV2E(vlist, edge_set, f, nv_idx)

            # set nearest feature to the new vertex breaking the edge
            f = [nv_idx]

        # set source vertex to the nearest feature
        sv_idx = f[0]

        # add the new edge if it exists
        flag = check_path(
            vlist, obs_edge_set, sv_idx, tpt, edge_set, obstacle_vertex_list
        )

        i += 1

        # finish
        if tpt == goal and flag:
            # render the current tree
            if DEBUG:
                for e in list(edge_set):
                    p1, p2 = vlist[e[0]].pt, vlist[e[1]].pt
                    pafn.frame_draw_line(screen, (p1, p2), pafn.colors["red"])
            # compute the path between start and goal
            pth = get_path(build_inverted_tree(list(edge_set), 0), 0, len(vlist) - 1)
            for j, p in enumerate(pth):
                pafn.frame_draw_bold_line(
                    screen, [vlist[p[0]].pt, vlist[p[1]].pt], pafn.colors["lawngreen"]
                )
            return


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
    opl = {v2pt(e.get_source_vertex()): i for i, e in enumerate(oel)}
    ovl = [V(k) for k, v in opl.items()]

    # print(opl[0].pt)
    obs_edge_set = set()
    for e in oel:
        val = v2pt(edge_vtx(e))
        val2 = v2pt(get_adj_succ(edge_vtx(e)))
        # obs_edge_set.add((v2pt(edge_vtx(e)), v2pt(get_adj_succ(edge_vtx(e)))))
        if (opl[val2], opl[val]) not in obs_edge_set:
            obs_edge_set.add((opl[val], opl[val2]))

    # sample the input space
    input_points = get_rand_sequence(300)
    ips = set(input_points)
    for tpt in input_points:
        f2 = get_nearest_feature(ovl, obs_edge_set, tpt)
        n = None
        if len(f2) > 1:
            n = get_normal_pt((ovl[f2[0]].pt, ovl[f2[1]].pt), tpt)
        else:
            n = ovl[f2[0]].pt
        if dist(tpt, n) < 1:
            ips.remove(tpt)
    input_points = list(ips)

    draw_face(screen, dcel, ID)
    pygame.display.update()

    s = (330, 600)
    g = (750, 400)
    last = None
    # time.sleep(3)
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
            RDT_loop(screen, goal, g, obs_edge_set, input_points, ovl)
            pafn.frame_draw_cross(screen, g, pafn.colors["red"])
            pafn.frame_draw_cross(screen, goal, pafn.colors["green"])
            pygame.display.update()

    pygame.display.update()
    time.sleep(3)


if __name__ == "__main__":
    main()
