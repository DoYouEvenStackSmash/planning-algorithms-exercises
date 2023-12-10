#!/usr/bin/python3
import sys

sys.path.append("./DCEL")
import numpy as np
from DCEL import *

# from BoundaryVertex import BoundaryVertex
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn

# from V import V
from cell_decomp_support import VerticalCellDecomposition as vcd

import collections


def draw_component(screen, edge_list, color=pafn.colors["white"]):
    pl = [e.get_source_vertex().get_point_coordinate() for e in edge_list]
    for i in range(1, len(pl)):
        pafn.frame_draw_ray(screen, pl[i - 1], pl[i], color)
    pafn.frame_draw_ray(screen, pl[-1], pl[0], color)


def gen_textbook_dcel():
    dcel = DCEL()
    bc = [(226, 280), (778, 284), (670, 711), (136, 706)]
    obs_1 = [(285, 579), (430, 622), (345, 515), (485, 333), (260, 393)]
    obs_2 = [(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)]
    dcel.create_face(bc, [obs_1, obs_2])
    return dcel


def gen_dcel_2():
    bc = [
        (159, 629),
        (332, 196),
        (427, 260),
        (581, 82),
        (765, 148),
        (628, 329),
        (534, 269),
        (460, 391),
        (608, 638),
        (427, 832),
    ]
    dcel = DCEL()
    a = [(436, 754), (401, 674), (501, 667)]
    b = [(437, 326), (422, 380), (396, 334), (430, 291), (487, 286)]
    c = [(590, 242), (556, 163), (680, 198)]
    x = [(397, 605), (319, 661), (368, 549), (290, 570), (395, 458)]
    x.reverse()
    print(a)
    a.reverse()
    print(a)
    # sys.exit()
    b.reverse()
    c.reverse()
    dcel.create_face(bc, [[(308, 609), (257, 591), (323, 424), (199, 619)], x, a, b, c])
    return dcel
