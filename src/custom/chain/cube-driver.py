#!/usr/bin/python3
import pygame
import time
from render_support import PygameArtFxns as pafn
from render_support import GeometryFxns as gfn
from render_support import MathFxns
from render_support import TransformFxns as tfn
import sys
LALT = 256
LSHIFT = 1
LCTRL = 64
SPACE = 32

def lerp_list(p1, p2, n = 100):
  pts = []
  step = 1 / n
  for i in range(n):
    pts.append(gfn.lerp(p1, p2, step * i))
  pts.append(p2)
  return pts

def lerp_calculate(pts, n = 100):
  l1 = lerp_list(pts[0],pts[1])
  l2 = lerp_list(pts[1],pts[2])
  l3 = lerp_list(pts[2],pts[3])
  m1 = []
  m2 = []
  step = 1 / n
  for i in range(n):
    m1.append(gfn.lerp(l1[i],l2[i],i * step))
    m2.append(gfn.lerp(l2[i],l3[i],i * step))
  m1.append(gfn.lerp(l1[-1],l2[-1],1))
  m2.append(gfn.lerp(l2[-1],l3[-1],1))
  m3 = []
  for i in range(n):
    m3.append(gfn.lerp(m1[i],m2[i],i * step))
  m3.append(gfn.lerp(m1[-1],m2[-1],1))
  return l1,l2,l3,m1,m2,m3

  
  
def pygame_cube_lerp_main(screen):
  k = 100
  segment = 8
  origin = (k,k)
  pts = []
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
        pts.append(p)
        pafn.frame_draw_dot(screen, p,pafn.colors["green"])
        if len(pts) == 4:
          pafn.clear_frame(screen)
          pafn.frame_draw_polygon(screen, pts, pafn.colors["red"])
          l1,l2,l3,m1,m2,mpts = lerp_calculate(pts)
          for i in range(len(mpts)):
            pafn.clear_frame(screen)
            for j in range(i):
              pafn.frame_draw_dot(screen, mpts[j], pafn.colors["cyan"])
            pafn.frame_draw_line(screen, (pts[0],pts[1]), pafn.colors['red'])
            pafn.frame_draw_line(screen, (pts[1],pts[2]), pafn.colors['red'])
            pafn.frame_draw_line(screen, (pts[2],pts[3]), pafn.colors['red'])
            pafn.frame_draw_line(screen, (l1[i],l2[i]),pafn.colors["tangerine"])
            pafn.frame_draw_line(screen, (l2[i],l3[i]),pafn.colors["tangerine"])
            pafn.frame_draw_bold_line(screen, (m1[i],m2[i]),pafn.colors['green'])
            # pafn.frame_draw_polygon(screen, pts, pafn.colors["red"])
            pygame.display.update()
            time.sleep(0.02)
          pts = []
        pygame.display.update()
        
def main():
  pygame.init()
  screen = pafn.create_display(800,800)
  pygame_cube_lerp_main(screen)

if __name__ == '__main__':
  main()