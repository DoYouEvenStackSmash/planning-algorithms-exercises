#!/usr/bin/python3
import numpy as np
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn

class VerticalCellDecomposition:
    def get_delta_theta(endpoint_1, vertex, endpoint_2):
        theta1, rad1 = mfn.car2pol(vertex, endpoint_1)
            
        theta2, rad2 = mfn.car2pol(vertex, endpoint_2)

        delta_theta = adjust_angle(theta2 - theta1)
        return delta_theta

    # def test_delta_theta(ept1, v, ept2):
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
        
        theta = gfn.test_get_delta_theta(A, B, C)
        
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
        M = VerticalCellDecomposition.get_normal_pt(A,B,C)
        
        T = mfn.pol2car(C, 10, theta)
        
        gamma = VerticalCellDecomposition.test_get_delta_theta(M,C,T)
        dist = mfn.euclidean_dist(C,M)
        h = dist / np.cos(gamma)

        I = mfn.pol2car(C,h,theta)
        return I
    
    def test_for_intersection(A,B,C,theta):
        T = mfn.pol2car(C,10,theta)

        d1 = mfn.euclidean_dist(A, C)
        d2 = mfn.euclidean_dist(B, C)
        d3 = mfn.euclidean_dist(A, T)
        d4 = mfn.euclidean_dist(B, T)
        
        if d3 > d1 and d4 > d2:
            return False
        
        I = VerticalCellDecomposition.get_intersection_pt(A,B,C,theta)
        d1 = mfn.euclidean_dist(A, I)
        d2 = mfn.euclidean_dist(B, I)
        base_d = mfn.euclidean_dist(A, B)
        if max(d1,d2) >= base_d:
            return False
        return True
            