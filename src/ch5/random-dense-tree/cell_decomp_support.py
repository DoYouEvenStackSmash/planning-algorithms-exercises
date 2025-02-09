#!/usr/bin/python3
import numpy as np

# from env_init import *
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn


def adjust_angle(theta):
    """
    adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
    """
    if theta > np.pi:
        theta = theta + -2 * np.pi
    elif theta < -np.pi:
        theta = theta + 2 * np.pi

    return theta


class VerticalCellDecomposition:
    """
    Class abstraction for defining vertical cell decomposition behaviors
    """

    def test_get_delta_theta(A, B, C):
        """
        Get the angle ABC
        """
        theta1, rad1 = mfn.car2pol(B, A)
        theta2, rad2 = mfn.car2pol(B, C)
        delta_theta = abs(adjust_angle(theta2 - theta1))
        return delta_theta

    def get_normal_pt(A, B, C):
        """
        Get a point on the segment AB 90 degrees from C
        """
        h = mfn.euclidean_dist(B, C)

        theta = VerticalCellDecomposition.test_get_delta_theta(A, B, C)

        direction, r = mfn.car2pol(B, A)
        d = h * np.cos(theta)
        normal_pt = mfn.pol2car(B, d, direction)
        return normal_pt

    def get_intersection_pt(A, B, C, theta):
        """
        Calculate an intersection point between a vector originating at C with angle theta
        and the line segment AB
        Returns a point
        """
        M = VerticalCellDecomposition.get_normal_pt(A, B, C)

        T = mfn.pol2car(C, 1, theta)

        gamma = VerticalCellDecomposition.test_get_delta_theta(M, C, T)
        dist = mfn.euclidean_dist(C, M)
        h = dist / np.cos(gamma)

        I = mfn.pol2car(C, h, theta)
        return I

    def test_for_intersection(A, B, C, theta):
        """
        Test function for determining whether vector at origin C with angle theta
        intersects with the segment AB
        Returns True/False
        """
        I = VerticalCellDecomposition.get_intersection_pt(A, B, C, theta)
        T = mfn.pol2car(C, 1, theta)
        test_distance = mfn.euclidean_dist(T, I)
        curr_distance = mfn.euclidean_dist(C, I)

        if test_distance > curr_distance:
            return False

        d1 = mfn.euclidean_dist(A, I)
        d2 = mfn.euclidean_dist(B, I)
        base_d = mfn.euclidean_dist(A, B)
        if max(d1, d2) >= base_d:
            return False
        return True

    def calc_face_split(edge_list, C_pt, angles=[np.pi / 2, -np.pi / 2]):
        """
        Calculates intersection points between vectors with origin C_pt and angles theta
        and active edges

        Returns a list of (x,y) points
        """
        split_vertices = []
        for angle in angles:
            for e in edge_list:
                A = e.get_source_vertex()
                B = e._next.get_source_vertex()
                if VerticalCellDecomposition.test_for_intersection(
                    A.get_point_coordinate(), B.get_point_coordinate(), C_pt, angle
                ):
                    split_vertices.append(
                        VerticalCellDecomposition.get_intersection_pt(
                            A.get_point_coordinate(),
                            B.get_point_coordinate(),
                            C_pt,
                            angle,
                        )
                    )
        return split_vertices

    def calculate_free_points(edge_list, boundary_vertex):
        """
        calculates points in C_free using midpoints of vertex,intersection_pt pairs
        at boundary angles

        Returns a list of (x,y) points
        """
        ipts = []
        distkey = lambda x: x[0]
        pt = boundary_vertex.vertex.get_point_coordinate()
        for va in boundary_vertex.angles:
            intersections = [
                [mfn.euclidean_dist(pt, i), i]
                for i in VerticalCellDecomposition.calc_face_split(edge_list, pt, [va])
            ]
            intersections = sorted(intersections, key=distkey)
            mpt = gfn.get_midpoint(
                boundary_vertex.vertex.get_point_coordinate(), intersections[0][1]
            )
            ipts.append(mpt)
        return ipts

    def check_for_free_path(edge_list, origin, angle, distance):
        """
        Determines whether vector with origin, angle, of length distance is free of obstacles
        Returns True/False
        """
        distkey = lambda x: x[0]
        intersections = [
            [mfn.euclidean_dist(origin, i), i]
            for i in VerticalCellDecomposition.calc_face_split(
                edge_list, origin, [angle]
            )
        ]
        intersections = sorted(intersections, key=distkey)
        for dist, pts in intersections:
            if dist < distance:
                return False
            else:
                break
        return True
