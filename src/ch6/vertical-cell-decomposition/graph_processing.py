#!/usr/bin/python3
from env_init import *
import heapq


class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight


def kruskal(edges):
    cost = 0

    tree_id = {}
    for e in edges:
        if e.u not in tree_id:
            tree_id[e.u] = len(tree_id)
        if e.v not in tree_id:
            tree_id[e.v] = len(tree_id)

    result = []

    edges.sort()

    for e in edges:
        if tree_id[e.u] != tree_id[e.v]:
            cost += e.weight
            result.append(e)

            old_id, new_id = tree_id[e.u], tree_id[e.v]
            for i in list(tree_id):
                if tree_id[i] == old_id:
                    tree_id[i] = new_id
    return result


class Vtx:
    def __init__(self):
        self.color = 0
        self.adj = []


from collections import deque


def build_inverted_tree(pair_list, start):
    """Given an edge list of pairs, constructs a spanning tree rooted at start

    Args:
        pair_list (_type_): list of points
        start (_type_): single point

    Returns:
        _type_: spanning tree as a list of edges
    """
    vlist = []
    queue = deque()
    vmap = {}
    for p in pair_list:
        a, b = p[0], p[1]
        if a not in vmap:
            vmap[a] = len(vmap)
            vlist.append(Vtx())
        if b not in vmap:
            vmap[b] = len(vmap)
            vlist.append(Vtx())
        vlist[vmap[a]].adj.append(vmap[b])
        vlist[vmap[b]].adj.append(vmap[a])
    queue.append(vmap[start])
    el = []
    vl = list(vmap)
    while queue:
        idx = queue[0]
        queue.popleft()
        v = vlist[idx]
        v.color = 1
        for n in v.adj:
            if vlist[n].color > 0:
                continue
            queue.append(n)
            el.append([vl[n], vl[idx]])
    return el


def get_path(el, start, end):
    """Given a rooted tree, solves for the shortest path (fewest number of edges
        between start and end

    Args:
        el (_type_): edge list as pairs of points
        start (_type_): single point
        end (_type_): single point

    Returns:
        _type_: path, edge list as pairs of points
    """
    el.reverse()
    c = 0
    while el[c][0] != end:
        c += 1
    marker = c + 1
    hold = c
    path = []
    while 1:
        e = [el[hold][1], el[hold][0]]
        path.append(e)
        if el[hold][1] == start:
            e = [el[hold][1], el[hold][0]]
            path.append(e)
            break
        while el[marker][0] != el[hold][1]:
            marker += 1
        hold = marker
        marker = marker + 1
    path.reverse()
    return path
