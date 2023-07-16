#!/usr/bin/python3
import numpy as np
from support.render_support import PygameArtFxns as pafn
from support.render_support import GeometryFxns as gfn
from support.render_support import MathFxns
from support.render_support import TransformFxns as tfn
from support.transform_polygon import *
from support.Polygon import *


class Link:
    LINE_LEN = 30
    """ A class which contains a geometric representation of a rigid body, which 
        can be connected to other Links to form a Chain

    Args:
        point_set (List[points]): A legacy abstraction for holding the representative
        points of a link
        endpoint ((int, int)): endpoint of the link in a global coordinate frame
        _prev (Link): reference to previous link for use in a chain
        _next (Link): reference to next link for use in a chain
        theta (float): angle of the link relative to some coordinate frame
        rigid_body (Polygon): Abstraction containing geometric representation 
        of a link
    """

    def __init__(
        self,
        point_set=None,
        endpoint=(0, 0),  #
        _prev=None,  #
        _next=None,  #
        theta=0,  #
        rigid_body=None,  # rigid body of the link
    ):
        self.point_set = point_set if point_set != None else []
        self.body = rigid_body
        self.rel_theta = theta
        self.prev = _prev
        self.next = _next
        self.endpoint = endpoint

    def get_body(self):
        """
        Accessor for internal polygon
        Returns a polygon object or None
        """
        return self.body

    def get_points(self):
        """
        Wrapper for points access
        """
        if self.body == None:
            return self.get_point_set()
        return self.get_body_points()

    def get_point_set(self):
        """
        Accessor for the point set which is constrained to the link
        Returns a list of points
        """
        return self.point_set

    def get_body_points(self):
        """
        Get internal point set
        returns a list of points
        """
        return self.body.dump_points()

    def get_relative_angle(self):
        """
        Accessor for the link's angle relative to previous link
        Returns an angle theta
        """
        return self.rel_theta

    def get_origin(self):
        """
        Accessor for the link's origin
        returns a point
        """
        return self.prev.get_endpoint()

    def get_endpoint(self):
        """
        Accessor for the link endpoint
        Returns a point
        """
        return self.endpoint

    def rotate(self, origin, rot_mat):
        """
        Given a rotation matrix, rotate the link about the given origin
        Does not return
        """
        self.endpoint = tfn.rotate_point(origin, self.get_endpoint(), rot_mat)
        self.point_set = tfn.rotate_point_set(origin, self.point_set, rot_mat)

    def rotate_body(self, origin, rot_mat):
        """
        Rotates internal polygon
        Does not return
        """
        self.endpoint = tfn.rotate_point(origin, self.get_endpoint(), rot_mat)
        rotate_polygon(self.body, rot_mat, origin)

    def translate_body(self, x_disp, y_disp):
        """
        Translates internal polygon
        Does not return
        """
        self.endpoint = (self.endpoint[0] + x_disp, self.endpoint[1] + y_disp)
        translate_polygon(self.body, x_disp, y_disp)

    def update_orientation(self, point_set, theta):
        """
        TODO rotate by angle
        """
        self.point_set = point_set
        self.rel_theta = theta

    def update_point_set(self, point_set):
        """
        Replace existing point set with a new point set.
        Used during rotations
        Does not return
        """
        self.point_set = point_set

    def get_normals(self):
        """
        Calculates coordinate axes x,y in R2
        Returns a pair of points representing axis unit endpoints
        """
        ox, oy = self.get_origin()
        theta = self.rel_theta
        xx, xy = Link.LINE_LEN * np.cos(theta), Link.LINE_LEN * np.sin(theta)
        yx, yy = Link.LINE_LEN * np.cos(theta + np.pi / 2), Link.LINE_LEN * np.sin(
            theta + np.pi / 2
        )
        return ((xx + ox, xy + oy), (yx + ox, yy + oy))

    def get_relative_rotation(self, target_point):
        """
        Given a target point, computes the angle theta between the current
        endpoint and the target point for use during rotation

        Returns a normalized angle theta
        """

        norm, dist = MathFxns.car2pol(self.get_origin(), self.get_endpoint())
        rad, r = MathFxns.car2pol(self.get_origin(), target_point)

        norm = MathFxns.correct_angle(norm)
        rad = MathFxns.correct_angle(rad)

        rotation = np.subtract(rad, norm)

        # correction for arctan identification
        if rotation > np.pi:
            rotation = rotation - 2 * np.pi
        if rotation < -np.pi:
            rotation = rotation + 2 * np.pi

        return rotation
