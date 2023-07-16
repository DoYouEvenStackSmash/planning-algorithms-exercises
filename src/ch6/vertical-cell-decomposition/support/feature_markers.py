#!/usr/bin/python3
import pygame
from support.render_support import PygameArtFxns as pafn
from support.render_support import GeometryFxns as gfn
from support.render_support import MathFxns
from support.render_support import TransformFxns as tfn
from support.unit_norms import *
from support.star_algorithm import *


def mark_vertex_clear(v, screen):
    """ """
    pafn.frame_draw_dot(screen, v.get_point_coordinates(), pafn.colors["tangerine"], 1)
    pygame.display.update()


def mark_edge_clear(edge, screen):
    """ """
    e_p1 = edge.source_vertex.get_point_coordinate()
    e_p2 = edge._next.source_vertex.get_point_coordinate()
    pafn.frame_draw_line(screen, [e_p1, e_p2], pafn.colors["tangerine"])
    pygame.display.update()


def VV_found(v1, v2, screen, VERBOSE=False):
    """
    Draws a bold line between two vertices
    Returns the distance between two points
    """
    p1 = v1.get_point_coordinate()
    p2 = v2.get_point_coordinate()
    # print(f"VV distance {distance_between_points(p1, p2)}")
    if VERBOSE:
        pafn.frame_draw_bold_line(screen, [p1, p2], pafn.colors["magenta"])
    return distance_between_points(p1, p2)
    # pygame.display.update()


def EV_found(edge, v1, screen, VERBOSE=False):
    """
    Draws a bold line between an edge and a vertex
    Returns the distance between two points
    """
    v_p = v1.get_point_coordinate()
    mp = calc_line_point(edge, v1)
    # print(f"EV distance {distance_between_points(v_p, mp)}")
    if VERBOSE:
        pafn.frame_draw_bold_line(screen, [mp, v_p], pafn.colors["cyan"])
    return distance_between_points(v_p, mp)
    # pygame.display.update()


def calc_line_point(edge, v1):
    """
    Calculates the nearest point on an edge to vertex v1
    Returns a (x,y) point
    """
    a = edge.source_vertex.get_point_coordinate()
    b = edge._next.source_vertex.get_point_coordinate()
    t = v1.get_point_coordinate()
    theta_ab = get_ray_angle(a, b)
    theta_at = get_ray_angle(a, t)
    if theta_ab < -np.pi / 2:
        theta_ab = 2 * np.pi + theta_ab
        if theta_at < 0:
            theta_at = 2 * np.pi + theta_at
    theta_E = abs(theta_ab - theta_at)
    rho_at = distance_between_points(a, t)
    r = np.cos(theta_E) * rho_at
    x = r * np.cos(theta_ab) + a[0]
    y = r * np.sin(theta_ab) + a[1]
    return (x, y)
