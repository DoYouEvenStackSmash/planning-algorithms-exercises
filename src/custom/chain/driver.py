#!/usr/bin/python3
import pygame
import time
from render_support import PygameArtFxns as pafn
from render_support import GeometryFxns as gfn
from render_support import MathFxns
import sys
SAMPLE_RATE = 400
LALT = 256
LSHIFT = 1
LCTRL = 64
SPACE = 32


def pygame_lerp_main(screen):
  k = 100
  segment = 8
  origin = (k,k)
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        # LCTRL for exit hotkey
        if pygame.key.get_mods() == LCTRL:
          sys.exit()
        if pygame.key.get_mods() == LALT:
          pafn.clear_frame(screen)
          continue
        while pygame.MOUSEBUTTONUP not in [event.type for event in pygame.event.get()]:
          continue
        p = pygame.mouse.get_pos()

        if segment > 2:
          spts = []
          pts = []
          ev = []
          l1_pts = []
          l2_pts = []

          seg_step = 1 / segment

          for i in range(segment):
            spts.append(gfn.lerp(origin, p, i * seg_step))
          spts.append(p)
          sign = 1
          for i in range(len(spts) - 1):
            ev.append(gfn.get_equilateral_vertex(spts[i], spts[i+1], sign))
            sign = sign * -1

          n = 100
          step = 1 / n
          for sp in range(len(spts) - 1):
            for i in range(n):
              l1 = gfn.lerp(spts[sp], ev[sp],step * i)
              l2 = gfn.lerp(ev[sp], spts[sp + 1], step * i)
              m1 = gfn.lerp(l1, l2, step * i)

              l1_pts.append(l1)
              l2_pts.append(l2)
              pts.append(m1)
          for sp in range(len(spts) - 1):
            li = n * sp
            ri = n * (sp + 1)
            interval = n * (sp + 1)
            
            for i in range(li,ri):
              pafn.clear_frame(screen)
              for j in range(i):
                pafn.frame_draw_dot(screen,pts[j],pafn.colors["cyan"])
              
              pafn.frame_draw_line(screen, (l1_pts[i], l2_pts[i]),pafn.colors["green"])
              # pafn.frame_draw_line(screen, (origin, p),pafn.colors["tangerine"])
              pafn.frame_draw_line(screen, (spts[sp],ev[sp]),pafn.colors["tangerine"])
              pafn.frame_draw_line(screen, (ev[sp],spts[sp+1]),pafn.colors["tangerine"])
              pygame.display.update()
              time.sleep(0.005)

          continue

        ev = gfn.get_equilateral_vertex(origin, p)
        mp = gfn.get_midpoint(origin, p)
        evs = []
        evs.append(gfn.get_equilateral_vertex(origin, mp))
        evs.append(gfn.get_equilateral_vertex(mp, p, -1))
        if segment == 2:
          n = 100
          step = 1 / n
          pts = []
          l1_pts = []
          l2_pts = []

          for i in range(n):
            l1 = gfn.lerp(origin, evs[0], step * i)
            l2 = gfn.lerp(evs[0], mp, step * i)
            m1 = gfn.lerp(l1, l2,step * i)
            pts.append(m1)
            l1_pts.append(l1)
            l2_pts.append(l2)

          for i in range(n):
            l1 = gfn.lerp(mp, evs[1], step * i)
            l2 = gfn.lerp(evs[1], p, step * i)
            m1 = gfn.lerp(l1, l2,step * i)
            pts.append(m1)
            l1_pts.append(l1)
            l2_pts.append(l2)
          
          for i in range(int(len(pts)/2)):
            pafn.clear_frame(screen)
            for j in range(i):
              pafn.frame_draw_dot(screen,pts[j],pafn.colors["cyan"])
            pafn.frame_draw_line(screen, (l1_pts[i], l2_pts[i]),pafn.colors["green"])
            # pafn.frame_draw_line(screen, (origin, p),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (origin,evs[0]),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (mp,evs[0]),pafn.colors["tangerine"])
            pygame.display.update()
            time.sleep(0.01)
          for i in range(int(len(pts)/2),len(pts)):
            pafn.clear_frame(screen)
            for j in range(i):
              pafn.frame_draw_dot(screen,pts[j],pafn.colors["cyan"])
            pafn.frame_draw_line(screen, (l1_pts[i], l2_pts[i]),pafn.colors["green"])
            # pafn.frame_draw_line(screen, (origin, p),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (mp,evs[1]),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (p,evs[1]),pafn.colors["tangerine"])
            pygame.display.update()
            time.sleep(0.01)
        
        elif segment == 1:
          n = 100
          step = 1 / n
          pts = []
          l1_pts = []
          l2_pts = []
          
          for i in range(n):

            l1 = gfn.lerp(origin, ev, step * i)
            l2 = gfn.lerp(ev, p, step * i)
            m1 = gfn.lerp(l1, l2,step * i)
            pts.append(m1)
            l1_pts.append(l1)
            l2_pts.append(l2)

          for i in range(n):
            pafn.clear_frame(screen)
            for j in range(i):
              pafn.frame_draw_dot(screen,pts[j],pafn.colors["cyan"])
            pafn.frame_draw_line(screen, (l1_pts[i], l2_pts[i]),pafn.colors["green"])
            # pafn.frame_draw_line(screen, (origin, p),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (origin,ev),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (p,ev),pafn.colors["tangerine"])
            pygame.display.update()
            time.sleep(0.01)
        continue
        l1 = gfn.get_midpoint(p,ev)
        l2 = gfn.get_midpoint(origin, ev)
        pafn.frame_draw_line(screen, (l1, l2),pafn.colors["tangerine"])
        print(ev)
        pafn.frame_draw_line(screen,(p,ev),pafn.colors["indigo"])
        pafn.frame_draw_line(screen,(ev,origin),pafn.colors["indigo"])
        pafn.frame_draw_dot(screen,ev,pafn.colors["cyan"])
        pafn.frame_draw_line(screen,(origin,p),pafn.colors["indigo"])
        pafn.frame_draw_dot(screen,p,pafn.colors["yellow"])
        pafn.frame_draw_dot(screen,origin,pafn.colors["green"])

        pygame.display.update()

    


      
def pygame_path_main(screen):
  '''
  Driver function interactions between two polygons A and static O
  Mouse driven path following
  '''
  
  while 1:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        # LCTRL for exit hotkey
        if pygame.key.get_mods() == LCTRL:
          sys.exit()
        if pygame.key.get_mods() == LALT:
          pafn.clear_frame(screen)
          continue
        
        ptlist = []
        counter = 0
        # construct the path
        while pygame.MOUSEBUTTONUP not in [event.type for event in pygame.event.get()]:
          if not counter % SAMPLE_RATE:
            ptlist.append(pygame.mouse.get_pos())
            pafn.frame_draw_dot(screen, ptlist[-1], colors["yellow"])
            pygame.display.update()
          counter+=1
        
        # observe the line
        # time.sleep(0.5)
        #clear_frame(screen)
        
        # execute the path following

def main():
  pygame.init()
  screen = pafn.create_display(800,800)
  pygame_lerp_main(screen)

if __name__ == '__main__':
  main()