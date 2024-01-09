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

THRES = 1e-8
xval = lambda m, p: 0 if abs(m) < THRES else m * np.cos(p)
yval = lambda m, p: 0 if abs(m) < THRES else m * np.sin(p)
mag = lambda complex_val: np.sqrt(complex_val.real**2 + complex_val.imag**2)
get_adj_succ = lambda p: p.get_half_edge().get_next_half_edge().get_source_vertex()
get_adj_pred = lambda p: p.get_half_edge().get_prev_half_edge().get_source_vertex()
v2pt = lambda p: p.get_point_coordinate()
get_rank = lambda v: v.rank
is_active = (
    lambda rank, e: min(get_rank(edge_vtx(e)), get_rank(get_adj_succ(edge_vtx(e))))
    <= rank
    and max(get_rank(edge_vtx(e)), get_rank(get_adj_succ(edge_vtx(e)))) >= rank
)
edge_vtx = lambda e: e.get_source_vertex()
norm = lambda cv: cv / abs(cv)
tang = lambda ang: ang * np.exp(1j * np.pi / 2)
atang = lambda ang: ang * np.exp(1j * -np.pi / 2)


def phase(complex_val):
    checkfxn = lambda x: [0 if abs(x) < THRES else x]

    r, i = checkfxn(complex_val.real), checkfxn(complex_val.imag)

    if r != 0:
        return np.arctan2(i, r)
    if i == 0:
        return 0
    return [np.pi / 2 if i > 0 else -np.pi / 2]


def cart2complex(cart_pt, center=(0, 0)):
    """Transforms a cartesian coordinate into a complex number with a center

    Args:
        cart_pt (_type_): _description_
        center (tuple, optional): _description_. Defaults to (0,0).

    Returns:
        _type_: complex exponential
    """
    ox, oy = cart_pt[0] - center[0], cart_pt[1] - center[1]
    r = np.sqrt(ox**2 + oy**2)
    theta = np.arctan2(oy, ox)
    return r * np.exp(1j * theta)


def complex2cart(complex_pt, center=(0, 0)):
    """Transforms a complex number into an x,y coordinate

    Args:
        complex_pt (_type_): _description_
        center (tuple, optional): _description_. Defaults to (0,0).

    Returns:
        _type_: pair of coordinates
    """
    m = mag(complex_pt)
    p = phase(complex_pt)
    x = xval(m, p) + center[0]
    y = yval(m, p) + center[1]
    return x, y


def vertical_cell_decomposition(screen, dcel, VERBOSE=False):
    # #

    # initialize things
    vpl = []
    pts = chain2vertex(dcel.construct_global_edge_list())

    # sort the points by x coordinate
    sortkey = lambda x: x.get_point_coordinate()[0]
    pts = sorted(pts, key=sortkey)
    for p in range(len(pts)):
        pts[p].rank = p + 1

    # initializers
    added_ranks = [0]
    angles = [np.pi / 2, -np.pi / 2]
    ranks = set()
    edge_list = []

    # visit all points
    for vtx in pts:
        vpl.append([])
        rank = get_rank(vtx)

        added_ranks.append(get_rank(vtx))

        nxt = get_adj_succ(vtx)
        prev = get_adj_pred(vtx)

        pt = vtx
        p1 = cart2complex(v2pt(prev), v2pt(pt))
        p2 = cart2complex(v2pt(nxt), v2pt(pt))

        # compute bisecting vector
        bounds = [norm(atang(p1)), norm(tang(p2))]
        delta = np.mean(bounds)

        # check for valid edges at angles of incidence
        alist = []
        for i in range(len(angles)):
            a = np.exp(1j * angles[i])

            if np.angle(delta / a) < 0 and np.angle(p1 / a) > 0:
                alist.append(a)

            if np.angle(delta / a) > 0 and np.angle(p2 / a) < 0:
                alist.append(a)

        # find closest edge intersection for valid angles
        el = []
        for a in alist:
            curr_ep = None
            curr_dist = float("inf")

            # shortcut for searching active edges only
            for e in reversed(edge_list):
                if not is_active(rank, e):
                    continue
                # test for intersection with an active edge
                if vcd.test_for_intersection(
                    v2pt(edge_vtx(e)),
                    v2pt(get_adj_succ(edge_vtx(e))),
                    v2pt(pt),
                    np.angle(a),
                ):
                    I = vcd.get_intersection_pt(
                        v2pt(edge_vtx(e)),
                        v2pt(get_adj_succ(edge_vtx(e))),
                        v2pt(pt),
                        np.angle(a),
                    )
                    if mfn.euclidean_dist(I, v2pt(pt)) <= curr_dist:
                        curr_dist = mfn.euclidean_dist(I, v2pt(pt))
                        curr_ep = I

            # store the intersection point
            if curr_ep != None:
                vpl[-1].append((v2pt(pt), curr_ep))

        # add new active edges
        if is_active(rank, vtx.get_half_edge()) and vtx.rank not in ranks:
            ranks.add(get_rank(vtx))
            edge_list.append(vtx.get_half_edge())
        if get_adj_succ(vtx).rank > rank and get_adj_succ(vtx).rank not in ranks:
            ranks.add(get_adj_succ(vtx).rank)
            edge_list.append(get_adj_succ(vtx).get_half_edge())
        if get_adj_pred(vtx).rank > rank and get_adj_pred(vtx).rank not in ranks:
            ranks.add(get_adj_pred(vtx).rank)
            edge_list.append(get_adj_pred(vtx).get_half_edge())

    return vpl


def refine_roadmap(dcel, vpl):
    """Given a pointset which covers the input space, constructs
        a roadmap graph and computes the minimum spanning tree over that

    Args:
        screen (_type_): _description_
        dcel (_type_): _description_
        vpl (_type_): _description_
    """
    el = dcel.construct_global_edge_list()
    pair_list = []
    for idx in range(len(vpl) - 1):
        orig_point_set = [gfn.get_midpoint(a, b) for a, b in vpl[idx]]
        for vl in vpl[idx + 1 :]:
            target_point_set = [gfn.get_midpoint(a, b) for a, b in vl]
            for midpt_1 in orig_point_set:
                for midpt_2 in target_point_set:
                    theta, d = mfn.car2pol(midpt_1, midpt_2)
                    if vcd.check_for_free_path(el, midpt_1, theta, d):
                        pair_list.append([midpt_1, midpt_2])

    keyval = lambda e: e[0]
    pair_list = list(
        set(
            tuple(sorted([tuple(sorted(p, key=keyval)) for p in pair_list], key=keyval))
        )
    )
    pair_list = [Edge(a, b, mfn.euclidean_dist(a, b)) for (a, b) in pair_list]
    pair_list = [[e.u, e.v, e.weight] for e in kruskal(pair_list)]
    pair_list = deque(pair_list)
    return pair_list


def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    ID, dcel = textbook_obj()

    vpl = vertical_cell_decomposition(screen, dcel)
    pair_list = refine_roadmap(dcel, vpl)

    draw_face(screen, dcel, ID)
    draw_roadmap(screen, pair_list)
    # pygame.display.update()

    keyval = lambda e: e[0]
    tree_list = build_inverted_tree(pair_list, pair_list[0][0])

    last = None
    vtx_pt_set = set()
    for e in tree_list:
        for v in e:
            vtx_pt_set.add(v)
    vol = list(vtx_pt_set)
    start, goal = pair_list[0][0], pair_list[len(pair_list) - 1][0]
    obstacle_space = dcel.construct_global_edge_list()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
            goal = tuple(pygame.mouse.get_pos())
            if goal == last:
                continue
            last = goal

        pafn.clear_frame(screen)
        draw_face(screen, dcel, ID)

        for ed in tree_list:
            p1, p2 = ed[0], ed[1]
            pafn.frame_draw_line(screen, (p1, p2), pafn.colors["black"])

        nearest_landmark = get_nearest_landmark(obstacle_space, pair_list, goal)
        if nearest_landmark == None:
            pafn.frame_draw_cross(screen, start, pafn.colors["red"])
            pafn.frame_draw_dot(screen, goal, pafn.colors["red"], True)
            pygame.display.update()
            continue

        nearest_vertex = get_nearest_vertex(obstacle_space, vol, nearest_landmark)
        pair_list.append((nearest_landmark, nearest_vertex))
        pair_list.append((goal, nearest_landmark))

        tree_list = build_inverted_tree(pair_list, start)
        path_to_goal = get_path(tree_list, start, goal)

        pair_list.pop()
        pair_list.pop()

        draw_path(screen, path_to_goal, pafn.colors["darker-green"])
        pafn.frame_draw_cross(screen, start, pafn.colors["red"])
        pygame.display.update()


if __name__ == "__main__":
    main()
