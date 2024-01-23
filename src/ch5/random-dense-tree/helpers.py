import numpy as np
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn

class V:
    def __init__(self, pt=None):
        self.pt = pt
        self.adj = set()


THRES = 1e-8
xval = lambda m, p: 0 if abs(m) < THRES else m * np.cos(p)
yval = lambda m, p: 0 if abs(m) < THRES else m * np.sin(p)
mag = lambda complex_val: np.sqrt(complex_val.real**2 + complex_val.imag**2)


def phase(complex_val):
    checkfxn = lambda x: [0 if abs(x) < THRES else x]

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
    return x[0], y[0]


# Define a lambda function to normalize a complex number
norm = lambda cv: cv / abs(cv)

# Import the NumPy library and define a constant for PI
PI = np.pi

# Define lambda functions for exponential, angle, and distance calculations using NumPy
exp = lambda x: np.exp(x)
ang = lambda x: np.angle(x)
dist = lambda p1, p2: np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))


# Define a function to calculate the distance between intersecting points A, B, C, and T
def get_intersect_dist(A, B, C, T):
    # Convert points B, C, A, and T to complex numbers
    eCB = cart2complex(B, C)
    eCA = cart2complex(A, C)
    eCT = cart2complex(T, C)
    
    eAT = cart2complex(T,A)
    eAC = cart2complex(C, A)
    eAB = cart2complex(B, A)
    
    eBT = cart2complex(T,B)
    eBC = cart2complex(C,B)
    eBA = cart2complex(A,B)
    
    if ang(eAT / eAB) * ang(eAT / eAC) < 0 or ang(eBT / eBA) * ang(eBT / eBC) < 0:
      return -1


    # Calculate angles and distances for further calculations

    theta = abs(ang(eAB / eAC))
    ndist = np.cos(theta) * dist(A, C)
    
    # Calculate the point N and the distance to the intersecting line
    N = complex2cart(norm(eAB) * ndist, A)
    if dist(A,N) > dist(A,B) or dist(B,N) > dist(A,B):
      return -1

    eCN = cart2complex(N, C)
    alpha = abs(ang(eCN / eCT))
    mdist = ndist / np.cos(alpha)

    # Calculate the point M and return the intersecting distance
    M = complex2cart(norm(eCT) * mdist, C)
    return mdist


def addV2E(vlist, edge_set, edge, v_idx):
    edge_set.remove(edge)
    v1, v2 = edge
    vlist[v1].adj.add(v_idx)
    vlist[v2].adj.add(v_idx)
    vlist[v1].adj.remove(v2)
    vlist[v2].adj.remove(v1)
    vlist[v_idx].adj.add(v1)
    vlist[v_idx].adj.add(v2)
    edge_set.add((v1, v_idx))
    edge_set.add((v_idx, v2))


def addV2V(vlist, edge_set, sv_idx, v_idx):
    edge_set.add((sv_idx, v_idx))
    vlist[sv_idx].adj.add(v_idx)
    vlist[v_idx].adj.add(sv_idx)


def edge_region_test(edge, pt):
    """tests if a point is in an edge region, defined as in voronoi

    Args:
        edge (_type_): pair of points
        pt (_type_): single point

    Returns:
        _type_: true/false
    """
    a, b, c = (
        cart2complex(pt, edge[0]),
        cart2complex(pt, edge[1]),
        cart2complex(edge[1], edge[0]),
    )
    if (
        abs(np.angle(a / c)) < np.pi / 2
        and abs(np.angle(b / (c * np.exp(1j * np.pi)))) < np.pi / 2
    ):
        return True
    return False


def get_normal_pt(edge, pt):
    """Given an edge and a point, calculates the point on the edge which is closest to the target

    Args:
        edge (_type_): pair of points
        pt (_type_): single point

    Returns:
        _type_: single point
    """
    a, b, c = (
        cart2complex(pt, edge[0]),
        cart2complex(pt, edge[1]),
        cart2complex(edge[1], edge[0]),
    )
    h = mag(a)
    norm = lambda cv: cv / abs(cv)
    theta = abs(np.angle(a / c))
    d = h * np.cos(theta)
    npt = complex2cart(norm(c) * d, edge[0])
    return npt


def get_nearest_feature(vtx_list, edge_set, tpt):
    min_edist = float("Inf")
    min_eidx = -1
    min_vdist = float("Inf")
    min_vidx = -1
    el = list(edge_set)
    for i, e in enumerate(el):
        p1, p2 = vtx_list[e[0]].pt, vtx_list[e[1]].pt
        if edge_region_test((p2, p1), tpt) or edge_region_test((p1, p2), tpt):
            d = dist(get_normal_pt((p1, p2), tpt), tpt)
            if d < min_edist:
                min_edist = d
                min_eidx = i
    for i, v in enumerate(vtx_list):
        d = dist(v.pt, tpt)
        if d < min_vdist:
            min_vdist = d
            min_vidx = i
    if min_vdist < min_edist:
        return [min_vidx]
    else:
        return el[min_eidx]


def check_path(vlist, obs_edge_set, sv_idx, tpt,edge_set):
    sv = vlist[sv_idx].pt
    min_st_dist = float("Inf")
    for e in obs_edge_set:
        p1, p2 = e
        d = get_intersect_dist(p1, p2, sv, tpt)
        # d2 = get_intersect_dist(p2, p1, sv, tpt)
        d2 = d
        if d < 0 and d2 < 0:
            continue
        if d < 0:
          d = d2
        if d2 < 0:
          d2 = d
        
        min_st_dist = min(min_st_dist, min(d2, d))
    
    theta, d = mfn.car2pol(sv, tpt)
    flag = False
    if min_st_dist > d:
      min_st_dist = d
      flag = True
    npt = mfn.pol2car(sv, min_st_dist, theta)
    np_idx = len(vlist)
    npv = V(npt)
    vlist.append(npv)
    addV2V(vlist, edge_set, sv_idx, np_idx)
    return flag
    

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