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


def triangulate(screen, dcel):
    pts = chain2vertex(dcel.construct_global_edge_list())
    stack = []
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
    check_pred_equal = lambda p1, p2: bool(get_rank(get_adj_pred(p1)) == get_rank(p2))
    check_succ_equal = lambda p1, p2: bool(get_rank(get_adj_succ(p1)) == get_rank(p2))
    norm = lambda cv: cv / abs(cv)
    tang = lambda ang: ang * np.exp(1j * np.pi / 2)
    atang = lambda ang: ang * np.exp(1j * -np.pi / 2)
    get_rank = lambda v: v.rank
    # sort the points by x coordinate
    sortkey = lambda x: x.get_point_coordinate()[0]
    angles = [np.pi / 2, -np.pi / 2]
    ranks = set()
    edge_list = []
    pts = sorted(pts, key=sortkey)
    for p in range(len(pts)):
        pts[p].rank = p + 1
    vpl = []
    # visit all points
    for idx, vtx in enumerate(pts):
        pt = vtx
        rank = get_rank(vtx)
        print(vpl)
        if len(vpl) > 0:
            for cp,nop in vpl[-1]:
            
                print(cp)
                theta, d = mfn.car2pol(v2pt(pt), nop)
                if vcd.check_for_free_path(edge_list, v2pt(pt), theta, d):
                    pafn.frame_draw_line(
                        screen, (v2pt(pt), nop), pafn.colors["silver"]
                    )
            for ranki in range(1, rank-1):
                theta, d = mfn.car2pol(v2pt(pt), v2pt(pts[ranki]))
                if vcd.check_for_free_path(edge_list, v2pt(pt), theta, d) and idx > 0:
                    pafn.frame_draw_line(
                        screen, (v2pt(pt), v2pt(pts[ranki])), pafn.colors["silver"]
                    )
            pygame.display.update()
        vpl.append([])
        

        # added_ranks.append(get_rank(vtx))

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
        print(vpl)

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
                pafn.frame_draw_cross(screen, curr_ep, pafn.colors["magenta"])
                pt = vtx
        print(vpl)
        if len(vpl) > 0:
            for cp,nop in vpl[-1]:
            
                print(cp)
                theta, d = mfn.car2pol(v2pt(pt), nop)
                if vcd.check_for_free_path(edge_list, v2pt(pt), theta, d):
                    pafn.frame_draw_line(
                        screen, (v2pt(pt), nop), pafn.colors["silver"]
                    )
            theta, d = mfn.car2pol(v2pt(pt), v2pt(pts[idx - 1]))
            if idx > 0 and vcd.check_for_free_path(edge_list, v2pt(pt), theta, d):
              
                pafn.frame_draw_line(
                    screen, (v2pt(pt), v2pt(pts[idx - 1])), pafn.colors["silver"]
                )
            pygame.display.update()
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

    # return vpl
    # pyga
    # for diag in diags:
    #     pafn.frame_draw_line(screen, [v2pt(d) for d in diag], pafn.colors["tangerine"])
    #     pygame.display.update()
    #     time.sleep(0.5)
    time.sleep(5)


def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    ID, dcel = textbook_obj()
    draw_face(screen, dcel, ID)
    pygame.display.update()
    triangulate(screen, dcel)


if __name__ == "__main__":
    main()
