#!/usr/bin/python3
import numpy as np
import pygame
import pygame.gfxdraw
import time


def adjust_angle(theta):
    """
    adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
    """
    if theta > np.pi:
        theta = theta + -2 * np.pi
    elif theta < -np.pi:
        theta = theta + 2 * np.pi

    return theta


class TransformFxns:
    """
    Transform functions
    """

    def rotation_matrix(rad_theta):
        """
        Creates a rotation matrix
        Returns a 2x2 numpy array
        """
        return np.array(
            [
                [np.cos(rad_theta), -np.sin(rad_theta)],
                [np.sin(rad_theta), np.cos(rad_theta)],
            ]
        )

    def calculate_rotation_matrix(rad_theta, step_count=30):
        """
        Wrapper for rotation matrix calculation including step count
        Returns a 2x2 numpy array
        """
        return TransformFxns.rotation_matrix(np.divide(rad_theta, step_count))

    def calculate_rotation(origin, target, last_target):
        """
        Calculates rotation as a delta theta between last target and current target
        returns an angle theta
        """
        if last_target == target:
            return 0, target
        rad, r = MathFxns.car2pol(origin, target)
        rad2, r2 = MathFxns.car2pol(origin, last_target)
        rotation = rad - rad2
        # adjust to make sure rotation is in interval [-pi, pi]
        if rotation > np.pi:
            rotation = rotation - (2 * np.pi)
        if rotation < -np.pi:
            rotation = rotation + (2 * np.pi)

        return rotation, target

    def rotate_point_set(origin, point_set, rot_mat):
        """
        Rotates a set of points using rotation matrix
        Wrapper for rotate point

        Returns a list of points
        """
        nps = []
        for i in point_set:
            nps.append(TransformFxns.rotate_point(origin, i, rot_mat))
        return nps

    def rotate_point(origin, pt, rot_mat):
        """
        Rotates a single point about an origin based on the rotation matrix
        Returns a point (x, y)
        """
        x_o, y_o = origin
        lp_x, lp_y = pt

        step = np.matmul(rot_mat, np.array([[lp_x - x_o], [lp_y - y_o]]))
        return (step[0][0] + x_o, step[1][0] + y_o)

    def get_translation_function(origin, t, steps=1):
        """
        Derives incremental displacement for a polygon to reach a target point
        in some number of steps
        Returns a tuple containing displacement for x,y, and a constant
        """
        r, theta = MathFxns.car2pol(origin, t)
        d = MathFxns.euclidean_dist(origin, t)
        sign = 1
        if d < 0 and r < 0:
            sign = -1
        r = r * d * sign
        # d = MathFxns.euclidean_dist(origin, t)
        # print(r)
        # return MathFxns.pol2car(, r, theta)
        step_dist = r / steps
        x_step = step_dist * np.cos(theta)
        y_step = step_dist * np.sin(theta)
        val = (x_step, y_step)
        return val


class MathFxns:
    """
    Math helper functions
    """

    def euclidean_dist(p1, p2):
        """
        Calculates euclidean distance between two points
        Returns a scalar value
        """
        return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

    def car2pol(origin, pt):
        """
        Converts a pair of points into a vector
        returns a vector (radians, radius)
        """
        x, y = pt
        ox, oy = origin
        rad = np.arctan2(y - oy, x - ox)
        r = MathFxns.euclidean_dist(origin, pt)
        return (rad, r)

    def pol2car(pt, radius, theta):
        """
        Convert polar coordinate to cartesian
        Returns a point
        """
        ox, oy = pt
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        return (ox + x, oy + y)

    def correct_angle(rad_theta):
        """
        Normalizes a negative angle theta, created by arctan2
        Returns an angle between -pi/2 and 2pi
        """
        if rad_theta <= -np.pi / 2:
            rad_theta = rad_theta + 2 * np.pi
        return rad_theta

    def adjust_angle(theta):
        """
        adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
        """
        if theta > np.pi:
            theta = theta + -2 * np.pi
        elif theta < -np.pi:
            theta = theta + 2 * np.pi

        return theta


class GeometryFxns:
    """
    Geometry helper functions
    """

    def get_equilateral_vertex(pt1, pt2, sign=1):
        """
        Calculates the vertex of an equilateral triangle
        Returns a point
        """
        rad, r = MathFxns.car2pol(pt1, pt2)
        nx = r * np.cos(rad + np.pi * sign / 3)
        ny = r * np.sin(rad + np.pi * sign / 3)
        return (nx + pt1[0], ny + pt1[1])

    def get_isosceles_vertex(pt1, pt2, sign=1, theta=45):
        rad, r = MathFxns.car2pol(pt1, pt2)
        radians = theta * (np.pi / 180) * sign
        nx = r * np.cos(rad + radians)
        ny = r * np.sin(rad + radians)
        return (nx + pt1[0], ny + pt1[1])

    def get_midpoint(pt1, pt2):
        """
        Calculates the midpoint of the segment connecting two points
        Returns a point
        """
        rad, r = MathFxns.car2pol(pt1, pt2)
        nx = r / 2 * np.cos(rad)
        ny = r / 2 * np.sin(rad)
        return (nx + pt1[0], ny + pt1[1])

    def lerp(pt1, pt2, t):
        """
        Lerp between two points
        Returns a point
        """
        rad, r = MathFxns.car2pol(pt1, pt2)
        nx = r * t * np.cos(rad)
        ny = r * t * np.sin(rad)
        return (nx + pt1[0], ny + pt1[1])

    def lerp_list(p1, p2, n=100):
        """
        Lerp helper function for two points
        Returns a list of points
        """
        pts = []
        step = 1 / n
        for i in range(n):
            pts.append(GeometryFxns.lerp(p1, p2, step * i))
        pts.append(p2)
        return pts

    def get_unit_norm_angle(ray_origin, ray_target, switch=False):
        """
        Returns the angle in radians of the vector normal to the line between two
        points.
        Switch is used by caller functions to flip the angle around the unit circle.
        """
        x1, y1 = ray_origin
        x2, y2 = ray_target

        rad_theta = np.arctan2(y2 - y1, x2 - x1)
        # print(rad_theta)
        rad_prime = rad_theta
        if rad_prime < -np.pi / 2:
            rad_prime = 2 * np.pi + rad_prime
        rad_prime = rad_prime - np.pi / 2

        if switch:
            if rad_prime > 0:
                return rad_prime - np.pi
            return rad_prime + np.pi
        return rad_prime

    def cubic_lerp_calculate(pts, n=100):
        """
        Cubic lerp function for a list of at least 4 points
        Returns linear interpolation between pairs of points
          l1=(A,B)
          l2=(B,C)
          l3=(C,D)
          m1 = (l1,l2)
          m2 = (l2,l3)
          p1 = (m1, m2)
        """
        l1 = GeometryFxns.lerp_list(pts[0], pts[1])
        l2 = GeometryFxns.lerp_list(pts[1], pts[2])
        l3 = GeometryFxns.lerp_list(pts[2], pts[3])
        m1 = []
        m2 = []
        step = 1 / n

        for i in range(n):
            m1.append(GeometryFxns.lerp(l1[i], l2[i], i * step))
            m2.append(GeometryFxns.lerp(l2[i], l3[i], i * step))
        m1.append(GeometryFxns.lerp(l1[-1], l2[-1], 1))
        m2.append(GeometryFxns.lerp(l2[-1], l3[-1], 1))

        p1 = []
        for i in range(n):
            p1.append(GeometryFxns.lerp(m1[i], m2[i], i * step))
        p1.append(GeometryFxns.lerp(m1[-1], m2[-1], 1))
        return l1, l2, l3, m1, m2, p1

    def get_unit_normal(pt1, pt2):
        """
        Accessor for normal vector
        """
        theta, r = MathFxns.car2pol(pt1, pt2)
        theta = adjust_angle(theta + np.pi / 2)

        return theta

    def get_cartesian_quadrant(theta):
        """
        Check function for determining the quadrant of the unit vector with angle theta
             -pi/2
          +-----+-----+
          |     |     |
        - |   3 | 4   | -
        pi|-----+-----+ 0
        + |   2 | 1   | +
          |     |     |
          +-----+-----+
               pi/2

        """

        PI_OVER_2 = np.divide(np.pi, 2)
        if theta == -np.pi:
            theta = np.pi
        if 0 < theta and theta <= PI_OVER_2:
            return 1
        if PI_OVER_2 < theta and theta <= np.pi:
            return 2
        if -np.pi < theta and theta <= -PI_OVER_2:
            return 3
        if -PI_OVER_2 < theta and theta < 0:
            return 4
        return 1


class PygameArtFxns:
    """set of colors"""

    colors = {
        "black": (0, 0, 0),
        "indigo": (48, 79, 254),
        "faded-blue": (15, 173, 237),
        "sky-blue": (111, 205, 244),
        "darker-green": (47, 178, 35),
        "yellow": (255, 255, 0),
        "tangerine": (255, 119, 34),
        "pink": (255, 122, 173),
        "cyan": (0, 255, 255),
        "green": (0, 255, 0),
        "magenta": (255, 0, 255),
        "red": (255, 0, 0),
        "white": (255, 255, 255),
        "dimgray": (105, 105, 105),
        "lightslategray": (119, 136, 153),
        "silver": (192, 192, 192),
        "forestgreen": (34, 139, 34),
        "seagreen": (46, 139, 87),
        "lawngreen": (124, 252, 0),
    }

    def create_display(width, height):
        """
        Initializes a pygame display
        width, height := pixel dimensions of the display
        Returns a pygame display object

        """
        return pygame.display.set_mode((width, height))

    def frame_draw_polygon(screen, point_set, color=(0, 0, 0)):
        """
        Draws a polygon of specified color
        Returns nothing
        """
        pygame.draw.polygon(screen, color, point_set, width=2)

    def frame_draw_line(screen, point_set, color=(0, 0, 0)):
        """
        Draws a thin line given a pair of points (start, end)
        Returns nothing
        """
        s, e = point_set
        pygame.draw.aaline(screen, color, s, e)

    def frame_draw_bold_line(screen, point_set, color=(0, 0, 0)):
        """
        Draws a bold line given a pair of points (start, end)
        Returns nothing
        """
        s, e = point_set
        pygame.draw.line(screen, color, s, e, width=4)

    def frame_draw_dot(screen, point, color=(255, 0, 0), width=0, thickness=4):
        """
        Draws a single dot given a point (x, y)
        Returns nothing
        """
        pygame.draw.circle(screen, color, point, thickness, width)

    def clear_frame(screen, color=(255, 255, 255)):
        """
        Resets the pygame display to a given color
        Returns nothing
        """
        pygame.Surface.fill(screen, PygameArtFxns.colors["lightslategray"])

    def draw_lines_between_points(screen, pts, color=(255, 255, 255)):
        """
        Given an ordered list of points, draws lines connecting each pair
        Returns nothing
        """
        color_arr = [
            PygameArtFxns.colors["red"],
            PygameArtFxns.colors["yellow"],
            PygameArtFxns.colors["white"],
        ]
        for i in range(1, len(pts)):
            # frame_draw_dot(screen, pts[i - 1], PygameArtFxns.colors["red"])

            PygameArtFxns.frame_draw_line(screen, (pts[i - 1], pts[i]), color)

        # frame_draw_dot(screen, pts[-1], PygameArtFxns.colors["red"])
        PygameArtFxns.frame_draw_line(screen, (pts[-1], pts[0]), color)

    def frame_draw_filled_polygon(screen, pts, color=(255, 255, 255)):
        """
        Draws a filled polygon
        Does not return
        """
        pygame.gfxdraw.filled_polygon(screen, pts, color)

    def frame_draw_cross(screen, pt, color=(255, 255, 255), size=10):
        """
        Draws a small cross
        Does not return
        """
        x, y = pt
        sz = size
        l1 = [(x + sz, y), (x - sz, y)]
        l2 = [(x, y + sz), (x, y - sz)]
        PygameArtFxns.frame_draw_bold_line(screen, l1, color)
        PygameArtFxns.frame_draw_bold_line(screen, l2, color)

    def frame_draw_ray(screen, pt1, pt2, color, BOLD=False):
        """
        Draws a ray from pt1 to pt2
        Does not return
        """
        # print(pt1, pt2)
        theta, r = MathFxns.car2pol(pt1, pt2)
        ip = MathFxns.pol2car(pt1, r - 20, theta)

        theta_left = adjust_angle(theta - np.pi / 2)
        theta_right = adjust_angle(theta + np.pi / 2)
        lpt = MathFxns.pol2car(ip, 6, theta_left)
        rpt = MathFxns.pol2car(ip, 6, theta_right)
        cpt = pt2
        if BOLD:
            PygameArtFxns.frame_draw_bold_line(screen, (pt1, pt2), color)
        else:
            PygameArtFxns.frame_draw_line(screen, (pt1, pt2), color)
        PygameArtFxns.frame_draw_filled_polygon(screen, [lpt, cpt, rpt], color)
