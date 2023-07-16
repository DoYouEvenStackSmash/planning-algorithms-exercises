#!/usr/bin/python3
from support.render_support import PygameArtFxns as pafn
from support.render_support import GeometryFxns as gfn
from support.render_support import MathFxns as mfn
from support.render_support import TransformFxns as tfn
from support.Link import Link
import CollisionDetection as ColDet


class Chain:
    def __init__(self, origin=(0, 0), parent=None, anchor=Link()):
        self.links = [anchor]
        self.links[-1].prev = self.links[-1]
        self.links[-1].endpoint = origin
        self.origin = origin
        # self.parent = parent

    def get_chain_point_sets(self):
        """
        Accessor for all points in the chain
        Returns a list of point sets
        """
        ptlist = []
        for link in self.links:
            ptlist.append(link.get_points())
        return ptlist

    def get_chain_normals(self):
        """
        Accessor for all coordinate axes in the chain
        Returns a list of pairs of points
        """
        ptlist = []
        for link in self.links:
            ptlist.append(link.get_normals())
        return ptlist

    def get_anchor_origin(self):
        """
        Accessor for chain anchor (link 0)
        Returns anchor origin
        """
        return self.origin

    def add_link(self, link):
        """
        Adds a link to the chain
        Does not return
        """
        link.prev = self.links[-1]
        self.links[-1].next = link
        self.links.append(link)

    def translate_chain(self, target_point):
        """
        Translates a chain of links to a target point
        """
        theta, r = mfn.car2pol(self.get_anchor_origin(), target_point)
        step_r = r
        x_step = step_r * np.cos(theta)
        y_step = step_r * np.sin(theta)
        total_x, total_y = 0, 0

        total_x += x_step
        total_y += y_step
        for link in self.links:
            link.translate_body(x_step, y_step)
        ax, ay = self.get_anchor_origin()
        self.origin = (ax + total_x, ay + total_y)

    def rotate_single_link(
        self, target_point, steps=10, Olist=[], COLLISION_SENSITIVE=True
    ):
        """
        Rotates a single chain link
        """
        rad2 = self.links[-1].get_relative_rotation(target_point)
        rot_mat2 = tfn.calculate_rotation_matrix(rad2, step_count=steps)
        step2 = np.divide(rad2, steps)
        origin = self.links[0].get_origin()
        total_rotation = 0
        for i in range(steps):
            for A in Olist:
                v = ColDet.check_contact(self.links[0].get_body(), A)
                if v < COLLISION_THRESHOLD:
                    return total_rotation
            self.links[-1].rotate_body(self.links[-1].get_origin(), rot_mat2)
            self.total_rotation += step2

        return total_rotation

    def rotate_two_link_chain(
        self,
        target_point,
        intermediate_point,
        steps=10,
        Olist=[],
        A=None,
        VERBOSE=False,
    ):
        """
        Rotates links in the chain as influenced by a target point
        Does not return
        Calls update
        """
        rad2 = self.links[-1].get_relative_rotation(intermediate_point)
        # rotate first link from circle intersection to target
        rad1, tp = tfn.calculate_rotation(
            self.get_anchor_origin(), target_point, intermediate_point
        )

        # calculate rotation matrices by number of steps
        rot_mat1 = tfn.calculate_rotation_matrix(rad1, step_count=steps)
        rot_mat2 = tfn.calculate_rotation_matrix(rad2, step_count=steps)
        step = np.divide(rad1, steps)
        step2 = np.divide(rad2, steps)
        origin = self.links[0].get_origin()
        """
      For each step
        for each link
          check collision against each obstacle
          If none, rotate
          else return
        for last link
          rotate by remainder
    """

        v = 0
        for i in range(steps):
            for j in range(1, len(self.links)):
                l = self.links[j]
                for A in Olist:
                    v = ColDet.check_contact(l.get_body(), A, VERBOSE)
                    if v < COLLISION_THRESHOLD:
                        return v
                l.rotate_body(origin, rot_mat1)
                l.rel_theta += step

            for A in Olist:
                v = ColDet.check_contact(l.get_body(), A, VERBOSE)
                if v < COLLISION_THRESHOLD:
                    return v
                # continue
            self.links[-1].rotate_body(self.links[-1].get_origin(), rot_mat2)
            self.links[-1].rel_theta += step2

        return 0

    def preprocess_circles(self, p):
        """
        Preprocesses circle circle intersection for a chain and a target point
        Returns a point
        """
        ps = calculate_circles(self, p)
        r, t = tfn.calculate_rotation(
            self.get_anchor_origin(), self.links[1].get_endpoint(), ps[1]
        )

        rot_mat = tfn.calculate_rotation_matrix(r, step_count=1)
        ps = tfn.rotate_point_set(self.get_anchor_origin(), ps, rot_mat)
        mpt1 = min_pt(ps[0], ps[2], p)
        mpt2 = min_pt(ps[1], mpt1, p)
        return mpt2

    def calculate_circles(self, target_point, DRAW=None):
        """
        Calculates intersection point of outermost circle
        https://mathworld.wolfram.com/Circle-CircleIntersection.html

        Returns a list of 3 points, which describe the chord going through the lens.
        """
        t_x, t_y = target_point
        rad, inner_len = MathFxns.car2pol(
            self.links[1].get_origin(), self.links[1].get_endpoint()
        )
        rad2, outer_len = MathFxns.car2pol(
            self.links[-1].get_origin(), self.links[-1].get_endpoint()
        )

        o_x, o_y = self.get_anchor_origin()

        target_distance = np.sqrt(np.square(t_x - o_x) + np.square(t_y - o_y))
        x = np.divide(
            (np.square(inner_len) + np.square(target_distance) - np.square(outer_len)),
            (2 * inner_len),
        )

        y = np.sqrt(
            np.square(target_distance)
            - (
                np.divide(
                    np.square(
                        np.square(inner_len)
                        + np.square(target_distance)
                        - np.square(outer_len)
                    ),
                    (4 * np.square(target_distance)),
                )
            )
        )
        max_radius = abs(outer_len)
        curr_radius = abs(outer_len - x)
        y = min(np.sqrt(abs(np.square(max_radius) - np.square(curr_radius))), y)
        ps = [(o_x + x, o_y + y), (o_x + x, o_y), (o_x + x, o_y - y)]

        return ps
