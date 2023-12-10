#!/usr/bin/python3
import numpy as np

from env_init import *


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

        T = mfn.pol2car(C, 10, theta)

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

    def is_active_edge(edge, curr_rank):
        """
        Test function for determining whether half edge is active in the interval of curr_rank
        Returns True/False
        """
        maxrank = lambda vpair: max(vpair[0].rank, vpair[1].rank)
        minrank = lambda vpair: min(vpair[0].rank, vpair[1].rank)
        vpair = (edge.get_source_vertex(), edge._next.get_source_vertex())
        return minrank(vpair) <= curr_rank and maxrank(vpair) > curr_rank

    def was_active_edge(edge, curr_rank):
        """
        Test function for determining whether half edge was active prior to curr_rank
        Returns True/False
        """
        vpair = (edge.get_source_vertex(), edge._next.get_source_vertex())
        minrank = lambda vpair: min(vpair[0].rank, vpair[1].rank)
        return minrank(vpair) <= curr_rank

    def get_norm_quadrant(v1, v2):
        """
        Wrapper function for determining quadrant of unit normal vector
        Returns an integer in {1,2,3,4}
        """
        unit_norm = gfn.get_unit_normal(
            v1.get_point_coordinate(), v2.get_point_coordinate()
        )
        quad = gfn.get_cartesian_quadrant(unit_norm)
        return quad

    def gen_bv(v, bv_list=[]):
        """
        Wrapper function for determining whether vertex V is a boundary vertex
        Adds to a list of boundary vertices
        """

        prv = lambda v: v._half_edge._prev.get_source_vertex()
        nxt = lambda v: v._half_edge._next.get_source_vertex()
        # pv1, pv2 = he.get_prev_vertex_segment()
        pv1, pv2 = prv(v), v
        pq = VerticalCellDecomposition.get_norm_quadrant(pv1, pv2)
        nv1, nv2 = v, nxt(v)
        nq = VerticalCellDecomposition.get_norm_quadrant(nv1, nv2)
        angles = VerticalCellDecomposition.get_vertical_angles(pq, nq)
        if len(angles):
            bv_list.append(BoundaryVertex(v, angles))

    def get_boundary_vertices(dcel):
        """
        Constructs the set of boundary vertices from all vertices in dcel
        Returns a list of BoundaryVertices
        """
        vertex_list = dcel.vertex_records
        edge_list = dcel.construct_global_edge_list()
        sortkey = lambda v: v.get_point_coordinate()[0]

        sorted_vl = sorted(vertex_list, key=sortkey)
        bv = []
        for i in range(len(sorted_vl)):
            sorted_vl[i].rank = i
            VerticalCellDecomposition.gen_bv(sorted_vl[i], bv)
        return bv

    def get_vertical_angles(p, n):
        """
        Helper function for determining valid vertical angles using quadrants
        Returns a list of valid angles
        """
        PI_OVER_2 = np.divide(np.pi, 2)
        if n == p:
            if n < 3:
                return [PI_OVER_2]
            else:
                return [-PI_OVER_2]

        if n == 1 and p == 2:
            return [PI_OVER_2]

        if n == 1 and p == 3:
            return [PI_OVER_2, -PI_OVER_2]

        if n == 1 and p == 4:
            return []

        if n == 2 and p == 1:
            return [PI_OVER_2]

        if n == 2 and p == 2:
            return [PI_OVER_2]

        if n == 2 and p == 3:
            return [PI_OVER_2, -PI_OVER_2]

        if n == 2 and p == 4:
            return [PI_OVER_2, -PI_OVER_2]

        if n == 3 and p == 1:
            return []
            # return [PI_OVER_2, -PI_OVER_2]

        if n == 3 and p == 2:
            return []

        if n == 3 and p == 3:
            return [-PI_OVER_2]

        if n == 3 and p == 4:
            return [-PI_OVER_2]

        if n == 4 and p == 1:
            return [PI_OVER_2, -PI_OVER_2]

        if n == 4 and p == 2:
            return [PI_OVER_2, -PI_OVER_2]

        if n == 4 and p == 3:
            return [-PI_OVER_2]

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

    def get_active_edges(edge_list, curr_rank):
        """
        Accessor function for active edges by rank
        returns a list of half_edges
        """
        valid_edges = []
        for e in edge_list:
            if VerticalCellDecomposition.is_active_edge(e, curr_rank):
                valid_edges.append(e)
        return valid_edges

    def get_past_edges(edge_list, curr_rank):
        """
        Accessor function for edges which have min_rank < curr_rank
        returns a list of half_edges
        """
        valid_edges = []
        for e in edge_list:
            if VerticalCellDecomposition.was_active_edge(e, curr_rank):
                valid_edges.append(e)
        return valid_edges

    def build_roadmap(dcel):
        """
        driver for vertical cell decomposition. Constructs a list of pairs representing roadmap
        returns a list of pairs of (x,y) points
        """
        boundary_events = VerticalCellDecomposition.get_boundary_vertices(dcel)
        global_edge_list = dcel.construct_global_edge_list()

        sortkey = lambda bv: bv.vertex.rank

        boundary_events = sorted(boundary_events, key=sortkey)

        rank = sortkey(boundary_events[0])

        valid_edges = VerticalCellDecomposition.get_active_edges(global_edge_list, rank)
        free_points = VerticalCellDecomposition.calculate_free_points(
            valid_edges, boundary_events[0]
        )
        pairs = []
        curr_layer = []
        last_layer = []
        for pt in free_points:
            last_layer.append(pt)
        last_active_edges = valid_edges

        for i in range(1, len(boundary_events)):
            bv = boundary_events[i]
            rank = sortkey(bv)

            valid_edges = VerticalCellDecomposition.get_active_edges(
                global_edge_list, rank
            )
            last_active_edges = VerticalCellDecomposition.get_past_edges(
                global_edge_list, rank
            )

            free_points = VerticalCellDecomposition.calculate_free_points(
                valid_edges, bv
            )
            intermediate_pts = []
            for fp in free_points:
                intermediate_pts.append(mfn.pol2car(fp, 5, np.pi))
            # print(intermediate_pts)

            for j in range(len(intermediate_pts)):
                pt = intermediate_pts[j]
                for k in range(len(last_layer)):
                    lpt = last_layer[k]
                    if lpt == None:
                        continue
                    theta, radius = mfn.car2pol(pt, lpt)
                    if VerticalCellDecomposition.check_for_free_path(
                        last_active_edges, pt, theta, radius
                    ):  # and check_for_free_path(last_active_edges, pt, theta, radius):
                        pairs.append([last_layer[k], pt])
                        last_layer[k] = None

            for pt in intermediate_pts:
                last_layer.append(pt)

            for j in range(len(free_points)):
                pt = free_points[j]
                if pt == None:
                    continue
                for k in range(len(last_layer)):
                    lpt = last_layer[k]
                    if lpt == None:
                        continue
                    theta, radius = mfn.car2pol(pt, lpt)
                    if VerticalCellDecomposition.check_for_free_path(
                        last_active_edges, pt, theta, radius
                    ):  # and check_for_free_path(last_active_edges, pt, theta, radius):
                        pairs.append([last_layer[k], pt])
                        last_layer[k] = None

            for pt in free_points:
                if pt != None:
                    curr_layer.append(pt)

            for lpt in last_layer:
                if lpt == None:
                    continue
                else:
                    curr_layer.append(lpt)

            last_layer = curr_layer
            curr_layer = []
        return pairs
