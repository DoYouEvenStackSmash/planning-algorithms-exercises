from support.star_algorithm import *
from support.render_support import PygameArtFxns as pafn
from support.render_support import GeometryFxns as gfn
from support.render_support import MathFxns as mfn
from support.render_support import TransformFxns as tfn

DEBUG = False
COLLISION_THRESHOLD = 10


class CollisionDetection:
    def __init__(self, screen=None):
        self.screen = screen

    def check_contact(self, A, O, VERBOSE=False):
        """
        Collision detection wrapper for an Agent and an obstacle
        Returns the distance between closest pair of points on agent and obstacle
        """
        val = self.find_contact(build_star(A.get_front_edge(), O.get_front_edge()))

        # if collision, draw boundary region(minkowski sum)
        if val < COLLISION_THRESHOLD:
            obs_spc = construct_star_diagram(A, O)
            pafn.frame_draw_polygon(self.screen, obs_spc, pafn.colors["yellow"])
        return val

    def find_contact(self, SL, VERBOSE=False):
        """
        Algorithm for finding overlapping voronoi regions
        Returns a scalar distance between the closest pair of points
        """
        i1, i2 = 0, 0
        end_marker = 0
        while SL[i1][1]._bounded_face == SL[i2][1]._bounded_face and i2 < len(SL):
            i2 += 1
        # this is the wrapper position when we terminate the first while loop
        end_marker = i2
        wrap = lambda x: x % len(SL)

        T_OOB_HYPOTENUSE = -3
        T_OOB_NORM = -1
        T_OOB_EDGE = -2
        T_IN_VOR_EDGE = 1
        END_FIRST_FLAG = False
        """
      i is chasing j
    """
        ev_records = []
        vv_records = []
        while 1:
            E = SL[wrap(i1)][1]
            V = SL[wrap(i2)][1].source_vertex
            val = self.t_in_vor_edge(E, V.get_point_coordinate())
            if val == T_IN_VOR_EDGE:
                if self.t_in_V_region(V, self.calc_line_point(E, V)):
                    if DEBUG:
                        print("EV found!")
                    ev_records.append((E, V))
                    return self.EV_found(E, V, VERBOSE)

            if val == T_OOB_NORM:  # candidate for VV, seeking symmetry
                if self.t_in_V_region(
                    E.source_vertex, V.get_point_coordinate()
                ) and self.t_in_V_region(V, E.source_vertex.get_point_coordinate()):
                    if DEBUG:
                        print("VV found")
                    vv_records.append((E.source_vertex, V))
                    return self.VV_found(E.source_vertex, V, VERBOSE)

            if val == T_OOB_HYPOTENUSE:
                E2 = E._next
                if self.t_in_V_region(
                    E2.source_vertex, V.get_point_coordinate()
                ) and self.t_in_V_region(V, E2.source_vertex.get_point_coordinate()):
                    if DEBUG:
                        print("VV found")
                    vv_records.append((E2.source_vertex, V))
                    return self.VV_found(E2.source_vertex, V, VERBOSE)
            e_hold = E._next
            while SL[wrap(i1)][1] != e_hold:
                i1 += 1
            if i1 > i2:
                temp = i1
                i1 = i2
                i2 = temp
                if i2 == end_marker:
                    break

        END_SECOND_FLAG = False
        while wrap(i1) != 0:
            E = SL[wrap(i1)][1]
            V = SL[wrap(i2)][1].source_vertex
            val = self.t_in_vor_edge(E, V.get_point_coordinate())
            if val == T_IN_VOR_EDGE:
                if self.t_in_V_region(V, self.calc_line_point(E, V)):
                    if DEBUG:
                        print("EV found!")
                    ev_records.append((E, V))
                    return self.EV_found(E, V, VERBOSE)

            if val == T_OOB_NORM:  # candidate for VV, seeking symmetry
                if self.t_in_V_region(
                    E.source_vertex, V.get_point_coordinate()
                ) and self.t_in_V_region(V, E.source_vertex.get_point_coordinate()):
                    if DEBUG:
                        print("VV found")
                    vv_records.append((E.source_vertex, V))
                    return self.VV_found(E.source_vertex, V, VERBOSE)

            if val == T_OOB_HYPOTENUSE:
                E2 = E._next
                if self.t_in_V_region(
                    E2.source_vertex, V.get_point_coordinate()
                ) and self.t_in_V_region(V, E2.source_vertex.get_point_coordinate()):
                    if DEBUG:
                        print("VV found")
                    vv_records.append((E2.source_vertex, V))
                    return self.VV_found(E2.source_vertex, V, VERBOSE)
            i1 += 1

    def mark_vertex_clear(self, v):
        """ """
        if self.screen != None:
            pafn.frame_draw_dot(
                self.screen, v.get_point_coordinates(), pafn.colors["tangerine"], 1
            )

        return

    def mark_edge_clear(self, edge):
        """ """
        e_p1 = edge.source_vertex.get_point_coordinate()
        e_p2 = edge._next.source_vertex.get_point_coordinate()
        if self.screen != None:
            pafn.frame_draw_line(self.screen, [e_p1, e_p2], pafn.colors["tangerine"])
            # pygame.display.update()
        return

    def VV_found(self, v1, v2, VERBOSE=False):
        """
        Draws a bold line between two vertices
        Returns the distance between two points
        """
        p1 = v1.get_point_coordinate()
        p2 = v2.get_point_coordinate()
        # print(f"VV distance {mfn.euclidean_dist(p1, p2)}")
        if self.screen != None:
            pafn.frame_draw_bold_line(self.screen, [p1, p2], pafn.colors["magenta"])
        return mfn.euclidean_dist(p1, p2)
        # pygame.display.update()

    def EV_found(self, edge, v1, VERBOSE=False):
        """
        Draws a bold line between an edge and a vertex
        Returns the distance between two points
        """
        v_p = v1.get_point_coordinate()
        mp = self.calc_line_point(edge, v1)
        # print(f"EV distance {mfn.euclidean_dist(v_p, mp)}")
        if self.screen != None:
            pafn.frame_draw_bold_line(self.screen, [mp, v_p], pafn.colors["cyan"])
        return mfn.euclidean_dist(v_p, mp)
        # pygame.display.update()

    def calc_line_point(self, edge, v1):
        """
        Calculates the nearest point on an edge to vertex v1
        Returns a (x,y) point
        """
        a = edge.source_vertex.get_point_coordinate()
        b = edge._next.source_vertex.get_point_coordinate()
        t = v1.get_point_coordinate()
        theta_ab, r = mfn.car2pol(a, b)
        theta_at, r = mfn.car2pol(a, t)

        if theta_ab < -np.pi / 2:
            theta_ab = 2 * np.pi + theta_ab
            if theta_at < 0:
                theta_at = 2 * np.pi + theta_at

        theta_E = abs(theta_ab - theta_at)
        rho_at = mfn.euclidean_dist(a, t)
        r = np.cos(theta_E) * rho_at
        x = r * np.cos(theta_ab) + a[0]
        y = r * np.sin(theta_ab) + a[1]
        return (x, y)

    # determines whether a point is within either of the adjacent regions
    def t_in_adj_e_vor(self, E, t):
        """
        Determines whether point t is in one of two neighboring edge regions
        Equivalently determines whether t is in voronoi region of their shared vertex
        """
        pE = self.t_in_vor_edge(E._prev, t)
        nE = self.t_in_vor_edge(E, t)
        if pE < 0 and nE < 0:
            return True
        return False

    def t_in_V_region(self, V, t):
        """
        Determines whether t is in voronoi region of V
        """
        E = V._half_edge
        pt1 = V.get_point_coordinate()
        pt2 = E._next.source_vertex.get_point_coordinate()
        ub = gfn.get_unit_norm_angle(pt1, pt2)
        pt3 = E._prev.source_vertex.get_point_coordinate()
        lb = gfn.get_unit_norm_angle(pt3, pt1)
        tb, radius = mfn.car2pol(pt1, t)
        if ub < 0:
            ub = 2 * np.pi + ub
            if lb < 0:
                lb = 2 * np.pi + lb
            if tb < 0:
                tb = 2 * np.pi + tb
        return lb < tb and tb < ub

    def t_in_overlapping_edges(self, E, t):
        """
        Determines whether a point is a member of two overlapping half planes
        """
        pt1 = E.source_vertex.get_point_coordinate()
        pt2 = E._next.source_vertex.get_point_coordinate()
        pt3 = E._prev.source_vertex.get_point_coordinate()
        # print(f"pt1:{pt1}\npt2:{pt2}\npt3:{pt3}\nt:{t}")
        H_prev_31 = self.check_half_plane(pt3, pt1, t)
        H_next_12 = self.check_half_plane(pt1, pt2, t)
        return H_next_12 or H_prev_31

    def check_half_plane(self, a, b, t):
        """
        Determines whether point t is a member of the half plane, as an angle
        offset from the vector normal to the segment ab
        """
        lead = mfn.car2pol(a, b)[0]
        target = mfn.car2pol(a, t)[0]

        if lead < 0:
            lead = 2 * np.pi + lead
            if target < 0:
                target = 2 * np.pi + target

        trail = lead - np.pi
        return trail < target and target < lead

    def t_in_E_region(self, E, t):
        """
        Wrapper function
        Determines whether t is in voronoi region of E
        """
        if self.t_in_vor_edge(E, t) > 0:
            return True
        return False

    def t_in_vor_edge(self, half_edge, t):
        """
        Determines whether t is in voronoi region of E
        """
        a = half_edge.source_vertex.get_point_coordinate()
        b = half_edge._next.source_vertex.get_point_coordinate()
        # print(f"edge {a} - {b} checking {t}...")
        r = mfn.euclidean_dist(a, b)

        theta_ab = mfn.car2pol(a, b)[0]
        theta_ab_norm = gfn.get_unit_norm_angle(a, b)
        theta_at = mfn.car2pol(a, t)[0]

        # print(f"ab:\t{theta_ab}\nnorm:\t{theta_ab_norm}\nt:\t{theta_at}")
        # if (self.screen != None):
        #   pafn.frame_draw_line(self.screen, [mfn.pol2car(a, r, theta_ab)], pafn.colors["red"])
        #   pafn.frame_draw_line(self.screen, [mfn.pol2car(a, r, theta_ab_norm)], pafn.colors["yellow"])
        # pygame.display.update()

        if theta_ab < -np.pi / 2:
            # print("adjusting ab")
            theta_ab = 2 * np.pi + theta_ab
            if theta_at < 0:
                theta_at = 2 * np.pi + theta_at

        if not (theta_ab_norm <= theta_at):
            if self.screen != None:
                pafn.frame_draw_line(self.screen, [a, t], pafn.colors["tangerine"])
            # print("outside ab_norm!")
            # print(f"norm: {theta_ab_norm} >= {theta_at}")
            # print(f"{t} is out of region by angle test.")
            return -1
        if not (theta_at <= theta_ab):
            if self.screen != None:
                pafn.frame_draw_line(self.screen, [a, t], pafn.colors["tangerine"])
            # print("outside ab!")
            # print(f"{theta_ab} <= {theta_at}")
            # print(f"{t} is out of region by angle test.")
            return -2

        theta_E = abs(theta_ab - theta_at)
        rho_at = mfn.euclidean_dist(a, t)
        h_max = r / np.cos(theta_E)

        if rho_at < h_max:
            # print(f"{t} is in vor(E)")
            if self.screen != None:
                pafn.frame_draw_line(self.screen, [a, t], pafn.colors["green"])
            return 1
        if self.screen != None:
            pafn.frame_draw_line(self.screen, [a, t], pafn.colors["indigo"])
        # print(f"{t} is out of region due to maximum hypotenuse_test.")
        return -3
