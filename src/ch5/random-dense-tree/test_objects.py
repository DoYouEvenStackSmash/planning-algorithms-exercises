#!/usr/bin/python3
import pygame
import sys

# from BoundaryVertex import BoundaryVertex
from DCEL import *

from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn

# from graph_processing import *
# from cell_decomp_support import VerticalCellDecomposition as vcd
import numpy as np
import time

# from V import V
from aux_functions import *


def test_obj_1():
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
    # print(a)
    a.reverse()
    # print(a)
    # sys.exit()
    b.reverse()
    c.reverse()
    ID = dcel.create_face(
        bc, [[(308, 609), (257, 591), (323, 424), (199, 619)], x, a, b, c]
    )
    return ID, dcel


def test_obj_2():
    bc = [(137, 86), (965, 56), (920, 944), (75, 930)]
    obs_1 = [
        (879, 116),
        (782, 160),
        (668, 154),
        (535, 174),
        (424, 221),
        (301, 361),
        (245, 515),
        (286, 648),
        (403, 727),
        (560, 757),
        (694, 734),
        (788, 616),
        (814, 491),
        (783, 361),
        (712, 278),
        (599, 267),
        (474, 349),
        (411, 474),
        (434, 546),
        (549, 560),
        (589, 528),
        (579, 462),
        (541, 392),
        (580, 314),
        (658, 319),
        (718, 361),
        (750, 474),
        (729, 576),
        (686, 633),
        (599, 668),
        (500, 671),
        (360, 604),
        (341, 495),
        (358, 406),
        (444, 317),
        (568, 237),
        (686, 195),
        (833, 236),
        (913, 440),
        (879, 656),
        (733, 838),
        (504, 873),
        (224, 772),
        (142, 565),
        (198, 308),
        (422, 151),
        (759, 106),
    ]
    # #
    obs_1.reverse()
    # #
    dcel = DCEL()
    ID = dcel.create_face(bc, [obs_1])
    return ID, dcel


def textbook_obj():
    dcel = DCEL()
    bc = [(226, 280), (778, 284), (670, 711), (136, 706)]
    obs_1 = [(285, 579), (430, 622), (345, 515), (485, 333), (260, 393)]
    obs_2 = [(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)]
    ID = dcel.create_face(bc, [obs_1, obs_2])
    return ID, dcel


def sq_test_obj():
    bc = [
        (150, 150),
        (800, 101),
        (799, 800),
        (201, 799),
    ]
    dcel = DCEL()
    a = [(436, 754), (401, 674), (501, 667)]
    b = [(437, 326), (422, 380), (396, 334), (430, 291), (487, 286)]
    c = [(590, 242), (556, 163), (680, 198)]
    x = [(397, 605), (319, 661), (368, 549), (290, 570), (395, 458)]
    x.reverse()
    # print(a)
    a.reverse()
    # print(a)
    # sys.exit()
    b.reverse()
    c.reverse()
    obs_2 = [(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)]

    ID = dcel.create_face(
        bc, [[(308, 609), (257, 591), (323, 424), (199, 619)], x, a, b, c, obs_2]
    )
    return ID, dcel
