#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import numpy as np
import time
import random

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
    # p2 = (,)
    split_dim = 0 if xmax - xmin > ymax - ymin else 1
    # print(split_dim)
    sortkey = lambda p: p[1]
    if split_dim == 0:
        sortkey = lambda p: p[0]
    comparexy = np.array(sorted(pairs, key=sortkey))
    # comparexy = np.sort(pairs[:],axis=split_dim)
    print(comparexy)
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

    # print(comparexy.shape)
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
        cut_ang = np.pi if root.cut_dim == 0 else np.pi / 2
        if len(root.box_pts):
            pafn.frame_draw_polygon(
                screen, boxpts(root.box_pts[0], root.box_pts[1]), pafn.colors["yellow"]
            )
        # pafn.frame_draw_line(screen, (root.pt, mfn.pol2car(root.pt, 1000, cut_ang)), pafn.colors["white"])
        # pafn.frame_draw_line(screen, (root.pt, mfn.pol2car(root.pt, 1000, np.pi + cut_ang)), pafn.colors["white"])
        # pygame.display.update()
        # if root.left != None:
        #   pafn.frame_draw_ray(screen, root.pt, root.left.pt, pafn.colors["green"])
        # if root.right != None:
        #   pafn.frame_draw_ray(screen, root.pt, root.right.pt, pafn.colors["green"])
        
        # time.sleep(0.1)
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


# def search_kd_tree


def box_distance(p1, corners):
    c1, c2 = corners
    if c1[0] < p1[0] < c1[0]:
        return min(abs(p1[1] - c1[1]), abs(p1[1] - c2[1]))
    if c1[1] < p1[1] < c1[1]:
        return min(abs(p1[0] - c1[0]), abs(p1[0] - c2[0]))
    else:
        d1 = mfn.euclidean_dist(p1, c1)
        d2 = mfn.euclidean_dist(p1, c2)
        d3 = mfn.euclidean_dist(p1, (c1[0], c2[1]))
        d4 = mfn.euclidean_dist(p1, (c2[0], c1[1]))
        return min(min(d1, d2), min(d3, d4))


def search_leaf(node, dbox, dbest, q, p):
    dist = mfn.euclidean_dist(q, node.pt)
    if dist < dbest[0]:
        p[0] = node.pt
        dbest[0] = dist


def search_tree(node, dbox, dbest, q, p):
    
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
            search_tree(node.left, dbox, dbest, q, p)
            search_tree(node.right, dbox - d2 + d1, dbest, q, p)

    


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
            print(init_d)
            p = [None]
            dbest = [float("inf")]
            search_tree(tr, init_d, dbest, goal, p)
            # print(dbest)
            pafn.frame_draw_cross(screen, goal, pafn.colors["red"])
            pafn.frame_draw_cross(screen, p[0], pafn.colors["green"])
            traverse(screen, tr)
            pygame.display.update()

    # s
    # p1 = (pairs[xmin][0],pairs[ymin][1])
    # p2 = (pairs[xmax][0],pairs[ymax][1])

    # comparexy = np.argsort(pairs[:,0],axis=0)
    # compareyx = np.argsort(pairs[:,1], axis=0)
    pygame.display.update()
    time.sleep(1)
    # for c,i in enumerate(pairs):
    #   # print(c)
    #   pafn.frame_draw_dot(screen, pairs[c], pafn.colors["cyan"])
    #   if not c%10:
    #     pygame.display.update()
    #     time.sleep(0.01)
    # for c,i in enumerate(pairs):
    #   # print(c)
    #   pafn.frame_draw_dot(screen, pairs[c], pafn.colors["cyan"])
    #   if not c%10:
    #     pygame.display.update()
    #     time.sleep(0.01)

    pygame.display.update()
    time.sleep(3)


if __name__ == "__main__":
    main()


# # k points
# if k == 1:
#   create single external node containing this point

# else:
#   compute minimum enclosing rectangle R for the points by
