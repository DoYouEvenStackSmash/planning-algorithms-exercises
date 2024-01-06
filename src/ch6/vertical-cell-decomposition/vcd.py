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

# from V import V
from aux_functions import *
from test_objects import *
from collections import deque
from graph_processing import *

THRES = 1e-8
xval = lambda m, p: 0 if abs(m) < THRES else m * np.cos(p)
yval = lambda m, p: 0 if abs(m) < THRES else m * np.sin(p)
mag = lambda complex_val: np.sqrt(complex_val.real**2 + complex_val.imag**2)


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


def vertical_edge_loop(screen, dcel):
    # #

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
                # pafn.frame_draw_cross(screen, curr_ep, pafn.colors["magenta"])

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

        pygame.display.update()

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
            for m1 in orig_point_set:
                for m2 in target_point_set:
                    theta, d = mfn.car2pol(m1, m2)
                    if vcd.check_for_free_path(el, m1, theta, d):
                        pair_list.append([m1, m2])
    keyval = lambda e: e[0]
    pair_list = set(tuple(sorted([tuple(sorted(p,key=keyval)) for p in pair_list], key=keyval)))
    pair_list = [Edge(a, b, mfn.euclidean_dist(a, b)) for (a, b) in pair_list]
    pair_list = [(e.u, e.v, e.weight) for e in kruskal(pair_list)]
    
    return pair_list

        
def draw_roadmap(screen,pair_list,color=pafn.colors["black"]):
    for p in pair_list:
        pafn.frame_draw_bold_line(screen, (p[0],p[1]), color)
        pygame.display.update()
        time.sleep(0.01)

def draw_path(screen, pair_list, color = pafn.colors["lawngreen"]):
    for p in pair_list:
        pafn.frame_draw_ray(screen, p[0],p[1], color,True)
        pygame.display.update()
        time.sleep(0.1)
    
    
def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    ID, dcel = test_obj_1()

    draw_face(screen, dcel, ID)
    pygame.display.update()
    time.sleep(2)
    vpl = vertical_edge_loop(screen, dcel)
    pl = refine_roadmap(dcel, vpl)
    draw_roadmap(screen, pl)
    keyval = lambda e: e[0]

    print(len(pl))
    print(len(vpl))

    el = build_inverted_tree(pl, pl[0][0])

    s,e =  pl[0][0],pl[len(pl)-1][0]
    
    el = get_path(el,s,e)
    pafn.frame_draw_cross(screen, s, pafn.colors["white"])
    pafn.frame_draw_cross(screen, e, pafn.colors["red"])
    draw_path(screen, el)

    pygame.display.update()
    time.sleep(5)


if __name__ == "__main__":
    main()
