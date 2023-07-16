#!/usr/bin/python3
from env_init import *
import pygame


def cut_face(screen, dcel):
    """
    Mouse driven line intersection visualizations
    """
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
        mfn.pol2car(pt, 500, mfn.adjust_angle(np.pi + angle)),
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


def main():
    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)

    dcel = gen_dcel_2()
    cut_face(screen, dcel)


if __name__ == "__main__":
    main()
