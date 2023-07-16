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
                pygame.display.update()

                theta, radius = mfn.car2pol(pt, lpt)
                if vcd.check_for_free_path(
                    last_active_edges, pt, theta, radius
                ):  # and check_for_free_path(last_active_edges, pt, theta, radius):
                    pairs.append([last_layer[k], pt])
                    last_layer[k] = None

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
        time.sleep(0.4)

    pygame.display.update()

    pafn.clear_frame(screen)
    for i, el in enumerate(ipl):
        draw_component(screen, el, colors[i])
    pygame.display.update()

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


def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    # dcel = gen_dcel_2()
    dcel = gen_textbook_dcel()
    # cut_face(screen, dcel)
    # generically_display_face(screen, dcel)
    # time.sleep(4)
    # sys.exit()
    # active_edge_traversal(screen, dcel)
    pl = event_active_edge_traversal(screen, dcel)
    # pl = vcd.build_roadmap(dcel)
    print(len(pl))
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
    time.sleep(4)
    # cut_face(screen, dcel)
    # calculated_face_cut(screen, dcel)
    sys.exit()


if __name__ == "__main__":
    main()
