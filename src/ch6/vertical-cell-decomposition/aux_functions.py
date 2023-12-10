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
from V import V


def draw_shape(screen, bc, maxs=(1000, 1000)):
    """Renders the elements of a body chain onto a screen
    Calls updates

    Args:
        screen (_type_): _description_
        bc (_type_): _description_
        maxs (tuple, optional): _description_. Defaults to (1000,1000).
    """

    for p in range(1, len(bc)):
        pafn.frame_draw_dot(screen, bc[p - 1])
        ptx = cart2complex(bc[p], bc[p - 1]) * np.exp(1j * np.pi / 2) * 0.5
        new_pt = complex2cart(ptx, bc[p - 1])
        pafn.frame_draw_ray(screen, bc[p - 1], bc[p], pafn.colors["magenta"])
        pygame.display.update()
        time.sleep(0.5)
        pafn.frame_draw_ray(screen, bc[p - 1], new_pt, pafn.colors["green"])
        pygame.display.update()
        time.sleep(0.5)

    # handle last edge
    pafn.frame_draw_dot(screen, bc[-1])
    ptx = cart2complex(bc[0], bc[-1]) * np.exp(1j * np.pi / 2) * 0.5
    new_pt = complex2cart(ptx, bc[-1])
    pafn.frame_draw_ray(screen, bc[-1], bc[0], pafn.colors["cyan"])
    pygame.display.update()
    time.sleep(0.5)
    pafn.frame_draw_ray(screen, bc[-1], new_pt, pafn.colors["green"])
    pygame.display.update()


def draw_last_point(screen, point_list):
    pafn.frame_draw_ray(screen, point_list[-1], point_list[0], pafn.colors["cyan"])
    pygame.display.update()
    time.sleep(0.5)


def chain2vertex(chain):
    """Unpacks vertices from a chain

    Args:
        chain (_type_): list of HalfEdge objects

    Returns:
        _type_: list of Vertex objects
    """
    return [e.get_source_vertex() for e in chain]


def chain2points(chain):
    """Unpacks points from a chain

    Args:
        chain (_type_): List of Half Edge objects

    Returns:
        _type_: list of points
    """
    return [e.get_point_coordinate() for e in chain2vertex(chain)]


def draw_face(screen, dcel, f_id=0):
    """Draws a face on a screen

    Args:
        screen (_type_): _description_
        dcel (_type_): _description_
        f_id (int, optional): _description_. Defaults to 0.
    """
    face = dcel.face_records[f_id]
    point_list = chain2points(face.get_boundary_chain())

    for p in range(1, len(point_list)):
        pafn.frame_draw_ray(
            screen, point_list[p - 1], point_list[p], pafn.colors["magenta"]
        )

        pygame.display.update()
        time.sleep(0.2)
    draw_last_point(screen, point_list)
    pygame.display.update()

    for ic in face.get_interior_component_chains():
        ic_point_list = chain2points(ic)
        for p in range(1, len(ic_point_list)):
            pafn.frame_draw_ray(
                screen, ic_point_list[p - 1], ic_point_list[p], pafn.colors["magenta"]
            )

        draw_last_point(screen, ic_point_list)
        pygame.display.update()
