#!/usr/bin/python3
import pygame
import sys

sys.path.append("./support")
#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import time
import sys
import numpy as np
from Polygon import *
from polygon_debugging import *

LALT = 256
LSHIFT = 1


def shape_draw(screen, A=None):
    pts = []
    polygons = []

    colors = []
    for i in pafn.colors:
        if i == "black":
            continue
        colors.append(pafn.colors[i])

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.key.get_mods() == LALT:
                    polygons.append(Polygon(pts))
                    polygons[-1].color = colors[len(polygons)]
                    pts = []
                    pafn.clear_frame(screen)
                    for p in polygons:
                        sanity_check_polygon(screen, p)
                    pygame.display.update()
                elif pygame.key.get_mods() == LSHIFT:
                    for p in polygons:
                        print(p.dump_points())
                    sys.exit()
                else:
                    pts.append(pygame.mouse.get_pos())
                    pafn.frame_draw_dot(screen, pts[-1], pafn.colors["green"])
                    pygame.display.update()


def adjust_angle(theta):
    """
    adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
    """
    if theta > np.pi:
        theta = theta + -2 * np.pi
    elif theta < -np.pi:
        theta = theta + 2 * np.pi

    return theta


def draw_rays(screen, A):
    pts = A.dump_points()
    for i in range(1, len(pts)):
        pafn.frame_draw_ray(screen, pts[i - 1], pts[i], A.color)
        # theta, r = mfn.car2pol(pts[i - 1], pts[i])
    pafn.frame_draw_ray(screen, pts[-1], pts[0], A.color)


def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    shape_draw(screen)
    sys.exit()


if __name__ == "__main__":
    main()
