#!/usr/bin/python3
from env_init import *


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
