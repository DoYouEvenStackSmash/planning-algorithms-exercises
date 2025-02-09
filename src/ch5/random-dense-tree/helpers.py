import numpy as np
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
from cell_decomp_support import *
import random


class V:
    def __init__(self, pt=None):
        self.pt = pt
        self.adj = set()


THRES = 1e-8
xval = lambda m, p: 0 if abs(m) < THRES else m * np.cos(p)
yval = lambda m, p: 0 if abs(m) < THRES else m * np.sin(p)
mag = lambda complex_val: np.sqrt(complex_val.real**2 + complex_val.imag**2)


def phase(complex_val):
    checkfxn = lambda x: 0 if abs(x) < THRES else x

    r, i = checkfxn(complex_val.real), checkfxn(complex_val.imag)

    if r != 0:
        return np.arctan2(i, r)
    if i == 0:
        return 0
    return [np.pi / 2 if i > 0 else -np.pi / 2]


def cart2complex(cart_pt, center=(0, 0)):
    """Transforms a cartesian coordinate into a complex number with a center

    Args:
        cart_pt (_type_): _description_
        center (tuple, optional): _description_. Defaults to (0,0).

    Returns:
        _type_: complex exponential
    """
    ox, oy = cart_pt[0] - center[0], cart_pt[1] - center[1]
    r = np.sqrt(ox**2 + oy**2)
    theta = np.arctan2(oy, ox)
    return r * np.exp(1j * theta)


def complex2cart(complex_pt, center=(0, 0)):
    """Transforms a complex number into an x,y coordinate

    Args:
        complex_pt (_type_): _description_
        center (tuple, optional): _description_. Defaults to (0,0).

    Returns:
        _type_: pair of coordinates
    """
    m = mag(complex_pt)
    p = phase(complex_pt)
    x = xval(m, p) + center[0]
    y = yval(m, p) + center[1]
    return (x, y)


# Define a lambda function to normalize a complex number
norm = lambda cv: cv / abs(cv)

# Import the NumPy library and define a constant for PI
PI = np.pi

# Define lambda functions for exponential, angle, and distance calculations using NumPy
exp = lambda x: np.exp(x)
ang = lambda x: np.angle(x)
dist = lambda p1, p2: np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))


def addV2E(vlist, edge_set, edge, v_idx):
    """
    Adds a vertex to a chosen edge. removes the chosen edge
    """
    edge_set.remove(edge)
    # vlist[edge[1]].adj.remove(edge[0])
    # vlist[edge[1]].adj.add(v_idx)
    # vlist[v_idx].adj.add(edge[0])
    # vlist[v_idx].adj.add(edge[1])
    edge_set.add((edge[0], v_idx))
    edge_set.add((v_idx, edge[1]))


def addV2V(vlist, edge_set, sv_idx, v_idx):
    """
    Adds a new edge between source vertex and new vertex
    """
    # vlist[sv_idx].adj.add(v_idx)
    # vlist[v_idx].adj.add(sv_idx)
    edge_set.add((sv_idx, v_idx))
    


def get_normal_pt(edge, pt):
    """Given an edge and a point, calculates the point on the edge which is closest to the target

    Args:
        edge (_type_): pair of points
        pt (_type_): single point

    Returns:
        _type_: single point
    """
    return VerticalCellDecomposition.get_normal_pt(edge[0],edge[1], pt)
    a, b, c = (
        cart2complex(pt, edge[0]),
        cart2complex(pt, edge[1]),
        cart2complex(edge[1], edge[0]),
    )
    if abs(c) == 0:
        return pt

    h = mag(a)
    norm = lambda cv: cv / abs(cv)
    theta = abs(np.angle(a / c))
    d = h * np.cos(theta)
    npt = complex2cart(norm(c) * d, edge[0])
    return npt


def get_nearest_feature(vtx_list, edge_set, tpt):
    """
    Given a target point, computes the nearest feature in the RDT
    """
    min_edist = float("Inf")
    min_eidx = -1
    min_vdist = float("Inf")
    min_vidx = -1
    edge_list = list(edge_set)

    # find the nearest edge
    for i, e in enumerate(edge_list):
        p1, p2 = vtx_list[e[0]].pt, vtx_list[e[1]].pt
        n = get_normal_pt((p1, p2), tpt)
        pdist = dist(p1, p2)
        if dist(n, p1) < pdist and dist(n, p2) < pdist:
            d = dist(n, tpt)
            if d < min_edist:
                min_edist = d
                min_eidx = i
    # find the nearest vertex
    
    sortkey = lambda x: x[0]
    dlist = sorted([(dist(vtx_list[i].pt,tpt),i) for i in range(len(vtx_list))], key = sortkey)
    min_vidx = dlist[0][1]
    min_vdist = dlist[min_vidx][0]

    # return the nearest feature
    if min_vdist < min_edist:
        return [min_vidx]
    else:
        return edge_list[min_eidx]


def check_path(vlist, obs_edge_set, sv_idx, tpt, edge_set, ovl):
    """
    Given a source point and a target point, computes the closest point between them on the boundary of an obstacle
    if it exists, otherwise creates the goal point.
    """
    sv = vlist[sv_idx].pt
    min_st_dist = float("Inf")
    theta, d = mfn.car2pol(sv, tpt)

    # check each obstacle edge for intersections
    for i,e in enumerate(obs_edge_set):
        p1, p2 = ovl[e[0]].pt, ovl[e[1]].pt
        if test_for_intersection(p1, p2, sv, theta):
            # I = VerticalCellDecomposition.get_intersection_pt(p1, p2, sv, theta)
            d = dist(
                VerticalCellDecomposition.get_intersection_pt(p1, p2, sv, theta), sv
            )
            min_st_dist = min(min_st_dist, d)

    theta, d = mfn.car2pol(sv, tpt)

    flag = False
    if min_st_dist >= d:
        min_st_dist = d
        flag = True

    # create the new vertex
    # npt = mfn.pol2car(sv, min_st_dist-1, theta)
    np_idx = len(vlist)
    # npv = V(npt)
    vlist.append(V(mfn.pol2car(sv, min_st_dist - 1, theta)))
    addV2V(vlist, edge_set, sv_idx, np_idx)
    return flag


def test_for_intersection(A, B, C, theta):
    """
    Test function for determining whether vector at origin C with angle theta
    intersects with the segment AB
    Returns True/False
    """
    I = VerticalCellDecomposition.get_intersection_pt(A, B, C, theta)
    T = mfn.pol2car(C, 0.2, theta)
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


def get_rand_sequence(k=32, ub=1000):
    """
    Generates a random sequence of floats between 0,1000
    returns a sequence of points
    """
    rng = np.random.default_rng(random.randint(10000,20000))
    rand_val = lambda: (rng.uniform()) * 700 + 130
    pl = []
    for i in range(k):
        x = rand_val() - 10
        y = rand_val() - 10
        pl.append((x, y))
    return pl

def check_for_free_path(obs_edge_list, obs_vtx_list, origin_pt, target_pt):
    """
    Determines whether vector with origin, angle, of length distance is free of obstacles
    Returns True/False
    """
    distkey = lambda x: x[0]
    intersections = []
    theta, d = mfn.car2pol(origin_pt,target_pt)
    # print(d)
    for i,e in enumerate(obs_edge_list):
        # print(e)
        p1, p2, = obs_vtx_list[e[0]].pt, obs_vtx_list[e[1]].pt
        if test_for_intersection(p1, p2, origin_pt, theta) or test_for_intersection(p2, p1, origin_pt, theta):
            npt = get_normal_pt((p1,p2), origin_pt)
            if dist(npt, origin_pt) < d:
                return False
                # continue
    return True
