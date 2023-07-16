#!/usr/bin/python3
from env_init import *


def clean_graph(pairlist):
    """
    Somewhat thrown together graph minimization
    Returns a list of pairs of (x,y) points
    """
    sortkey = lambda pt: pt[0]
    adj_dict = {}
    vertex_list = []
    for pair in pairlist:
        pair = sorted(pair, key=sortkey)
        pt1, pt2 = pair
        if pt1 not in adj_dict:
            adj_dict[pt1] = len(vertex_list)
            vertex_list.append(V(pt1))
        v1 = vertex_list[adj_dict[pt1]]

        if pt2 not in adj_dict:
            adj_dict[pt2] = len(vertex_list)
            vertex_list.append(V(pt2))
        v2 = vertex_list[adj_dict[pt2]]
        v1.neighbor_dict[adj_dict[pt2]] = False
        v2.neighbor_dict[adj_dict[pt1]] = False

    edge_list = []

    for k, v_idx in adj_dict.items():
        v = vertex_list[v_idx]
        vlist = []
        for i in v.neighbor_dict:
            if not v.neighbor_dict[i]:
                vlist.append((mfn.euclidean_dist(vertex_list[i].pt, v.pt), i))
            vlist = sorted(vlist, key=sortkey)
            if len(vlist):
                neighbor_idx = vlist[0][1]
                neighbor = vertex_list[neighbor_idx]
                neighbor.neighbor_dict[v_idx] = True
                v.neighbor_dict[neighbor_idx] = True
                edge_list.append((v.pt, neighbor.pt))

    return edge_list
