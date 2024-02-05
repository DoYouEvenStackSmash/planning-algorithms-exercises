#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import numpy as np
import time
import random
import sys
nodecount = 0


class TNode:
    def __init__(self, pt, cut_dim=0):
        global nodecount
        self.pt = pt
        self.cut_dim = cut_dim
        self.left = None
        self.right = None
        self.id = nodecount
        nodecount += 1
        self.box_pts = [pt, pt]


nodelist = []


def build_func(pairs):
    global nodelist
    k = len(pairs)
    print(k)
    if k == 1:
        M = TNode(pairs[0])
        nodelist.append(M)
        return M
    xmax = np.argmax(pairs[:, 0], axis=0)
    ymax = np.argmax(pairs[:, 1], axis=0)
    xmin, ymin = np.argmin(pairs[:, 0], axis=0), np.argmin(pairs[:, 1], axis=0)
    xmin = pairs[xmin][0]
    ymin = pairs[ymin][1]
    xmax = pairs[xmax][0]
    ymax = pairs[ymax][1]
    
    split_dim = 0 if xmax - xmin > ymax - ymin else 1
    sortkey = lambda p: p[1]
    if split_dim == 0:
        sortkey = lambda p: p[0]
    comparexy = np.array(sorted(pairs, key=sortkey))
    
    if k == 2:
        M1 = TNode(comparexy[1])
        M1.box_pts = [(xmin, ymin), (xmax, ymax)]
        M1.cut_dim = split_dim
        M2 = TNode(comparexy[0])
        M2.cut_dim = -1 + split_dim * -1
        M1.left = M2
        nodelist.append(M1)
        nodelist.append(M2)
        return M1
    if k == 3:
        M1 = TNode(comparexy[0])
        M2 = TNode(comparexy[1])
        M3 = TNode(comparexy[2])
        M2.left = M1
        M2.right = M3
        M2.cut_dim = split_dim
        M2.box_pts = [(xmin, ymin), (xmax, ymax)]
        nodelist.append(M1)
        nodelist.append(M2)
        nodelist.append(M3)
        return M2

    m = int(np.ceil(k / 2))

    M = TNode(comparexy[m])
    M.box_pts = [(xmin, ymin), (xmax, ymax)]
    M.cut_dim = split_dim
    nodelist.append(M)
    l1 = comparexy[:m]
    l2 = comparexy[m + 1 :]
    if len(l1):
        M.left = build_func(l1)
    if len(l2):
        M.right = build_func(l2)
    return M


boxpts = lambda a, b: [(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])]


def traverse(screen, root):
    if root != None:
        pafn.frame_draw_dot(screen, root.pt, pafn.colors["red"])
        if root.left == None or root.right == None:
            pafn.frame_draw_cross(screen, root.pt, pafn.colors["tangerine"])
        
        cut_ang = np.pi if root.cut_dim == 0 else np.pi / 2
        if len(root.box_pts):
            pafn.frame_draw_polygon(
                screen, boxpts(root.box_pts[0], root.box_pts[1]), pafn.colors["yellow"]
            )

        traverse(screen, root.left)
        traverse(screen, root.right)


from graphviz import Digraph


def convert_to_graphviz(nodelist):
    graph = Digraph(
        format="png"
    )  # You can choose the output format (e.g., 'png', 'pdf', 'svg', etc.)

    for n in nodelist:
        node_label = f"{n.pt} : c{n.cut_dim}"
        graph.node(str(n.id), label=node_label)

        if n.left:
            graph.edge(str(n.id), str(n.left.id))

        if n.right:
            graph.edge(str(n.id), str(n.right.id))

    graph.render(
        filename="kd", cleanup=True, view=True
    )  # Saves the output as 'kd.format' and opens it


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

# Import the NumPy library and define a constant for PI
PI = np.pi

# Define lambda functions for exponential, angle, and distance calculations using NumPy
exp = lambda x: np.exp(x)
ang = lambda x: np.angle(x)
dist = lambda p1, p2: np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

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
    if abs(c) == 0:
        return pt

    h = mag(a)
    norm = lambda cv: cv / abs(cv)
    theta = abs(np.angle(a / c))
    d = h * np.cos(theta)
    npt = complex2cart(norm(c) * d, edge[0])
    return npt

def box_distance(p1, corners):
    c1, c2 = corners
    c3,c4 = (c1[0],c2[1]),(c2[0],c1[1])
    xmin = min(c2[0],c1[0])
    xmax = max(c2[0],c1[0])
    ymin = min(c2[1],c1[1])
    ymax = max(c2[1],c1[1])
    edges = []
    if xmin < p1[0] < xmax:
        edges.extend([(c1,c4),(c2,c3)])
    if ymin < p1[1] < ymax:
        edges.extend([(c1,c3),(c2,c4)])
        
    npts = [get_normal_pt(edge, p1) for edge in edges]
    npts.extend([c1,c2,c3,c4])
    
    npmin = np.min([dist(npt, p1) for npt in npts])
    return npmin
    
search_count = 0
    
    
def search_leaf(node, dbox, dbest, q, p):
    global search_count
    search_count +=1
    dist = mfn.euclidean_dist(q, node.pt)
    if dist < dbest[0]:
        p[0] = node.pt
        dbest[0] = dist


def search_tree(node, dbox, dbest, q, p):
    global search_count
    if node != None:
        search_count +=1
    if node != None and (node.right == None or node.left == None):
        if node.right != None:
            search_leaf(node.right, dbox, dbest, q, p)
        if node.left != None:
            search_leaf(node.left, dbox, dbest, q, p)
        search_leaf(node, dbox, dbest, q, p)
    
    
    if node.left != None and node.right != None and dbox < dbest[0]:
        d1 = float("Inf")
        d2 = float("Inf")
        if node.left != None:
            d1 = box_distance(q, node.left.box_pts)
        if node.right != None:
            d2 = box_distance(q, node.right.box_pts)

        if d1 < d2:
            search_tree(node.left, dbox, dbest, q, p)
            search_tree(node.right, dbox - d1 + d2, dbest, q, p)
        else:
            search_tree(node.right, dbox, dbest, q, p)
            search_tree(node.left, dbox - d2 + d1, dbest, q, p)
    


    


def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    T = 30
    pairs = np.array(
        [(random.randint(1, 1000), random.randint(1, 1000)) for _ in range(T)]
    )
    # pairs = np.array([(a, b) for a in A_range for b in B_range])
    tr = build_func(pairs)
    # print(nodecount)
    # print(len(nodelist))
    traverse(screen, tr)
    # convert_to_graphviz(nodelist)
    last = None
    global search_count
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
            goal = pygame.mouse.get_pos()
            if goal == last:
                continue
            last = goal
            pafn.clear_frame(screen)
            init_d = box_distance(goal, tr.box_pts)
            # print(init_d)
            p = [None]
            dbest = [float("inf")]
            search_tree(tr, init_d, dbest, goal, p)
            print(search_count)
            search_count = 0
            pafn.frame_draw_ray(screen, goal, p[0], pafn.colors["green"],True)
            pafn.frame_draw_cross(screen, goal, pafn.colors["red"])
            traverse(screen, tr)
            pygame.display.update()

    pygame.display.update()
    time.sleep(1)

    pygame.display.update()
    time.sleep(3)


if __name__ == "__main__":
    main()
