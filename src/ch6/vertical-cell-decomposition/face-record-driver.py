#!/usr/bin/python3
import pygame
import sys

sys.path.append("./support")
sys.path.append("./DCEL")
from env_init import *

# from BoundaryVertex import BoundaryVertex
# from DCEL import *

from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
from graph_processing import *
# from cell_decomp_support import VerticalCellDecomposition as vcd
import numpy as np
import time
from V import V


def cut_face(screen, dcel):
    f_id = 0
    fr = dcel.face_records[f_id]

    ipl = fr.get_interior_component_chains()
    ipl.append(fr.get_boundary_chain())

    colors = []
    for i in pafn.colors:
        if i == "black":
            continue
        colors.append(pafn.colors[i])

    for i, el in enumerate(ipl):
        draw_component(screen, el, colors[i])
    pygame.display.update()
    angle = np.pi / 2
    vert_line = lambda pt: (
        mfn.pol2car(pt, 500, angle),
        mfn.pol2car(pt, 500, adjust_angle(np.pi + angle)),
    )

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pt = pygame.mouse.get_pos()
                for il in ipl:
                    intersections = vcd.calc_face_split(il, pt)
                    for ipt in intersections:
                        pafn.frame_draw_cross(screen, ipt, pafn.colors["red"])
                vl = vert_line(pt)
                pafn.frame_draw_line(screen, vl, pafn.colors["lightslategray"])
                pygame.display.update()


def event_active_edge_traversal(screen, dcel):
    colors = []
    for i in pafn.colors:
        if i == "black":
            continue
        colors.append(pafn.colors[i])
    boundary_events = vcd.get_boundary_vertices(dcel)
    fr = dcel.face_records[0]
    ipl = fr.get_interior_component_chains()
    ipl.append(fr.get_boundary_chain())
    global_edge_list = []
    for il in ipl:
        for e in range(len(il)):
            global_edge_list.append(il[e])

    get_seg = lambda edge: (
        edge.source_vertex.get_point_coordinate(),
        edge._next.source_vertex.get_point_coordinate(),
    )
    sortkey = lambda bv: bv.vertex.rank

    boundary_events = sorted(boundary_events, key=sortkey)
    for i, el in enumerate(ipl):
        draw_component(screen, el, colors[i])
    # for bv in boundary_events:
    #     segs = bv.get_vertical_vectors()
    #     for seg in segs:
    #         pafn.frame_draw_line(screen, seg, pafn.colors["white"])
    pygame.display.update()
    time.sleep(2)
        # pafn.frame_

    last_layer = []
    curr_layer = []
    rank = sortkey(boundary_events[0])
    valid_edges = vcd.get_active_edges(global_edge_list, rank)
    fps = vcd.calculate_free_points(valid_edges, boundary_events[0])
    pairs = []
    for pt in fps:
        last_layer.append(pt)
    last_active_edges = valid_edges

    for i in range(1, len(boundary_events)):
        bv = boundary_events[i]
        pafn.clear_frame(screen)
        pafn.frame_draw_cross(
            screen, bv.vertex.get_point_coordinate(), pafn.colors["magenta"]
        )
        for i, el in enumerate(ipl):
            draw_component(screen, el, colors[i])

        rank = sortkey(bv)

        valid_edges = vcd.get_active_edges(global_edge_list, rank)
        last_active_edges = vcd.get_past_edges(global_edge_list, rank)

        fps = vcd.calculate_free_points(valid_edges, bv)
        intermediate_pts = []
        for fp in fps:
            intermediate_pts.append(
                mfn.pol2car(fp, 5, np.pi)
            )
        # print(intermediate_pts)

        for j in range(len(intermediate_pts)):
            pt = intermediate_pts[j]
            pafn.frame_draw_cross(screen, pt, pafn.colors["red"])
            for k in range(len(last_layer)):
                lpt = last_layer[k]
                if lpt == None:
                    continue
                theta, radius = mfn.car2pol(pt, lpt)
                if vcd.check_for_free_path(
                    last_active_edges, pt, theta, radius
                ):  # and check_for_free_path(last_active_edges, pt, theta, radius):
                    pairs.append([last_layer[k], pt])
                    last_layer[k] = None
        
        # pygame.display.update()
        # time.sleep(0.3)
        for pt in intermediate_pts:
            last_layer.append(pt)
        
        for j in range(len(fps)):
            pt = fps[j]
            if pt == None:
                continue
            pafn.frame_draw_cross(screen, pt, pafn.colors["cyan"])

            for k in range(len(last_layer)):
                lpt = last_layer[k]
                if lpt == None:
                    continue
                pafn.frame_draw_dot(screen, lpt, pafn.colors["red"])
                # pygame.display.update()

                theta, radius = mfn.car2pol(pt, lpt)
                if vcd.check_for_free_path(
                    last_active_edges, pt, theta, radius
                ):  # and check_for_free_path(last_active_edges, pt, theta, radius):
                    pairs.append([last_layer[k], pt])
                    # last_layer[k] = None

        for pt in fps:
            if pt != None:
                curr_layer.append(pt)

        for lpt in last_layer:
            if lpt == None:
                continue
            else:
                curr_layer.append(lpt)
        for pair in pairs:
            pafn.frame_draw_line(screen, (pair[0], pair[1]), pafn.colors["tangerine"])

        last_layer = curr_layer
        curr_layer = []

        pygame.display.update()
        time.sleep(0.2)

    pygame.display.update()

    pafn.clear_frame(screen)
    for i, el in enumerate(ipl):
        draw_component(screen, el, colors[i])
    pygame.display.update()
    pairs = clean_graph(pairs)
    pairs = clean_graph(pairs)
    return pairs
    # sys.exit()


def generically_display_face(screen, dcel):
    f_id = 0
    fr = dcel.face_records[f_id]
    el = fr.get_boundary_chain()
    pl = [e.get_source_vertex().get_point_coordinate() for e in el]
    for i in range(1, len(pl)):
        pafn.frame_draw_ray(screen, pl[i - 1], pl[i], pafn.colors["white"])
    pafn.frame_draw_ray(screen, pl[-1], pl[0], pafn.colors["white"])

    int_comp_list = fr.get_interior_component_chains()
    iptl = []
    for el in int_comp_list:
        iptl.append([e.get_source_vertex().get_point_coordinate() for e in el])
    colors = []
    for i in pafn.colors:
        if i == "black":
            continue
        colors.append(pafn.colors[i])
    for x in range(len(iptl)):
        interior_component = iptl[x]
        color = colors[x]
        for i in range(1, len(interior_component)):
            pafn.frame_draw_ray(
                screen, interior_component[i - 1], interior_component[i], color
            )
        pafn.frame_draw_ray(
            screen, interior_component[-1], interior_component[0], color
        )

    pygame.display.update()
    time.sleep(3)


def gen_textbook_dcel():
    dcel = DCEL()
    bc = [(226, 280), (778, 284), (670, 711), (136, 706)]
    obs_1 = [(285, 579), (430, 622), (345, 515), (485, 333), (260, 393)]
    obs_2 = [(419, 482), (528, 541), (505, 591), (622, 576), (561, 386)]
    dcel.create_face(bc, [obs_1, obs_2])
    return dcel

def gen_spiral_dcel():
    dcel = DCEL()
    bc = [(137, 86), (965, 56), (920, 944), (75, 930)]
    obs_1 = [(879, 116), (782, 160), (668, 154), (535, 174), (424, 221), (301, 361), (245, 515), (286, 648), (403, 727), (560, 757), (694, 734), (788, 616), (814, 491), (783, 361), (712, 278), (599, 267), (474, 349), (411, 474), (434, 546), (549, 560), (589, 528), (579, 462), (541, 392), (580, 314), (658, 319), (718, 361), (750, 474), (729, 576), (686, 633), (599, 668), (500, 671), (360, 604), (341, 495), (358, 406), (444, 317), (568, 237), (686, 195), (833, 236), (913, 440), (879, 656), (733, 838), (504, 873), (224, 772), (142, 565), (198, 308), (422, 151), (759, 106)]
    obs_1.reverse()
    dcel.create_face(bc, [obs_1])
    return dcel


def gen_dcel_2():
    bc = [
        (159, 629),
        (332, 196),
        (427, 260),
        (581, 82),
        (765, 148),
        (628, 329),
        (534, 269),
        (460, 391),
        (608, 638),
        (427, 832),
    ]
    dcel = DCEL()
    a = [(436, 754), (401, 674), (501, 667)]
    b = [(437, 326), (422, 380), (396, 334), (430, 291), (487, 286)]
    c = [(590, 242), (556, 163), (680, 198)]
    x = [(397, 605), (319, 661), (368, 549), (290, 570), (395, 458)]
    x.reverse()
    print(a)
    a.reverse()
    print(a)
    # sys.exit()
    b.reverse()
    c.reverse()
    dcel.create_face(bc, [[(308, 609), (257, 591), (323, 424), (199, 619)], x, a, b, c])
    return dcel

def test_triangle_theta(A,B,C):
    theta_1 = vcd.test_get_delta_theta(A,B,C)
    theta_2 = vcd.test_get_delta_theta(B,A,C)
    return theta_1 > np.pi / 2 or theta_2 > np.pi / 2

def query_roadmap(screen, dcel, pairlist):
    sortkey = lambda pt: pt[0]
    adj_dict = {}
    pt_set = set()
    vertex_list = []
    for pair in pairlist:
        pair = sorted(pair, key=sortkey)
        pt1, pt2 = pair
        pt_set.add(pt1)
        pt_set.add(pt2)
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
    edge_list = dcel.construct_global_edge_list()
    pt_list = list(pt_set)
    get_seg = lambda edge: (
        edge.source_vertex.get_point_coordinate(),
        edge._next.source_vertex.get_point_coordinate(),
    )
    pt_index = []
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pt = pygame.mouse.get_pos()
                
                vlist = []
                seg_dict = {}
                for pair in pairlist:
                    seg = pair
                    if not test_triangle_theta(seg[0],seg[1], pt):
                        npt = vcd.get_normal_pt(seg[0],seg[1], pt)
                        theta, radius = mfn.car2pol(pt, npt)
                        if vcd.check_for_free_path(edge_list, pt, theta, radius):
                            vlist.append((mfn.euclidean_dist(npt, pt), npt))
                            seg_dict[npt] = seg

                for v in pt_list:
                    theta, radius = mfn.car2pol(pt, v)
                    if vcd.check_for_free_path(edge_list, pt, theta, radius):
                        vlist.append((mfn.euclidean_dist(v, pt),v))
                vlist = sorted(vlist, key=sortkey)
                nearest_neighbor = vlist[0][1]
                new_pairs = []
                if nearest_neighbor not in pt_set:
                    seg = seg_dict[nearest_neighbor]

                    pairlist.append((seg[0], nearest_neighbor))
                    new_pairs.append(pairlist[-1])
                    pairlist.append((seg[1], nearest_neighbor))
                    new_pairs.append(pairlist[-1])
                    
                    pt_set.add(nearest_neighbor)
                    pt_list.append(nearest_neighbor)
                    if nearest_neighbor not in adj_dict:
                        adj_dict[nearest_neighbor] = len(vertex_list)
                        vertex_list.append(V(nearest_neighbor))
                    vprime = vertex_list[adj_dict[seg[0]]]
                    vdprime = vertex_list[adj_dict[seg[1]]]
                    vprime.neighbor_dict[adj_dict[nearest_neighbor]] = False
                    vdprime.neighbor_dict[adj_dict[nearest_neighbor]] = False
                    vn = vertex_list[adj_dict[nearest_neighbor]]
                    vn.neighbor_dict[adj_dict[seg[0]]] = False
                    vn.neighbor_dict[adj_dict[seg[1]]] = False
                    # v1 = vertex_list[adj_dict[nearest_neighbor]]
                pt_set.add(pt)
                pairlist.append((nearest_neighbor, pt))
                new_pairs.append(pairlist[-1])

                if pt not in adj_dict:
                    adj_dict[pt] = len(vertex_list)
                    vertex_list.append(V(pt))
                v1 = vertex_list[adj_dict[nearest_neighbor]]
                v2 = vertex_list[adj_dict[pt]]

                v1.neighbor_dict[adj_dict[pt]] = False
                v2.neighbor_dict[adj_dict[nearest_neighbor]] = False
                # # for v in vlist:
                pc = [pafn.colors["green"],pafn.colors["red"]]
                pafn.frame_draw_cross(screen, pt, pc[len(pt_index)])
                # pafn.frame_draw_line(screen, (pt,nearest_neighbor), pafn.colors["green"])
                pygame.display.update()
                # for pair in new_pairs:
                #     pafn.frame_draw_bold_line(screen, (pair[0],pair[1]),pafn.colors["red"])
                pt_index.append(pt)
            if len(pt_index) == 2:
                time.sleep(0.5)
                start = pt_index[0]
                end = pt_index[1]
                stack = find_path(adj_dict, vertex_list, start, end)
                for v in range(1, len(stack)):
                    # pafn.frame_draw_cross(screen, stack[v - 1].get_coord(), pafn.colors["yellow"])
                    pafn.frame_draw_bold_line(
                        screen,
                        (stack[v - 1].get_coord(), stack[v].get_coord()),
                        pafn.colors["green"],
                    )
                    pygame.display.update()
                    time.sleep(0.1)
                for v in vertex_list:
                    v.neighbor_counter = 0
                    v.visited = 0
                pt_index = []
                pygame.display.update()
            
def find_path(adj_dict, vertex_list, start_pt, target_pt):
    WHITE = 0
    GRAY = 1
    BLACK = 2
    for v in vertex_list:
        v.neighbor_dict = list(set(v.neighbor_dict))
    vertex_dict = vertex_list
    print(len(vertex_list))
    curr_vertex = vertex_list[adj_dict[start_pt]]
    target_vtx = vertex_list[adj_dict[target_pt]]
    stack = []
    curr_vertex.visited = GRAY
    stack.append(curr_vertex)
    while stack[-1].get_coord() != target_pt:
        print(stack[-1].neighbor_dict)
        if stack[-1].visited == BLACK:
            stack.pop()
            continue
        stack[-1].visited = GRAY
        if stack[-1].neighbor_counter < len(stack[-1].neighbor_dict):
            stack[-1].neighbor_counter += 1
            if (
                vertex_dict[
                    stack[-1].neighbor_dict[stack[-1].neighbor_counter -1]
                ].visited
                == WHITE
            ):
                stack.append(
                    vertex_dict[stack[-1].neighbor_dict[stack[-1].neighbor_counter - 1]]
                )
                stack[-1].visited = GRAY
                # break

        # if stack[-1].neighbor_counter >=len(stack[-1].neighbor_dict):
        #     stack[-1].visited = BLACK
        #     stack.pop()
        #     continue
        else:
            stack[-1].visited = BLACK
            stack.pop()
    return stack
    
                
def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    # dcel = gen_dcel_2()
    dcel = gen_spiral_dcel()
    # dcel = gen_textbook_dcel()
    # cut_face(screen, dcel)
    # generically_display_face(screen, dcel)
    # time.sleep(4)
    # sys.exit()
    # active_edge_traversal(screen, dcel)
    pl = event_active_edge_traversal(screen, dcel)
    # pl = vcd.build_roadmap(dcel)
    # print(len(pl))
    # pl = clean_graph(pl)
    fr = dcel.face_records[0]
    ipl = fr.get_interior_component_chains()
    ipl.append(fr.get_boundary_chain())
    # colors = [pafn.colors["cyan"], pafn.colors["magenta"], pafn.colors["white"]]
    colors = []
    for i in pafn.colors:
        if i == "black":
            continue
        colors.append(pafn.colors[i])

    for i, el in enumerate(ipl):
        draw_component(screen, el, colors[i])
    pygame.display.update()
    # time.sleep(3)
    for pair in pl:
        pafn.frame_draw_line(screen, pair, pafn.colors["tangerine"])
    print("Foo")
    pygame.display.update()
    query_roadmap(screen, dcel, pl)
    # time.sleep(4)
    # cut_face(screen, dcel)
    # calculated_face_cut(screen, dcel)
    sys.exit()


if __name__ == "__main__":
    main()
