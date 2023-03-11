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

# render 
def lerp_render(screen, n, spts, ev, l1_pts, l2_pts, pts):

  # render lerp points
  for sp in range(len(spts) - 1):
    li = n * sp
    ri = n * (sp + 1)
    
    for i in range(li,ri):
      pafn.clear_frame(screen)
      # render preexisting points, plus new point
      for j in range(i):
        pafn.frame_draw_dot(screen,pts[j],pafn.colors["cyan"])
      
      pafn.frame_draw_line(screen, (l1_pts[i], l2_pts[i]),pafn.colors["green"])
      # pafn.frame_draw_line(screen, (origin, p),pafn.colors["tangerine"])
      pafn.frame_draw_line(screen, (spts[sp],ev[sp]),pafn.colors["tangerine"])
      pafn.frame_draw_line(screen, (ev[sp],spts[sp+1]),pafn.colors["tangerine"])
      pygame.display.update()
      time.sleep(0.005)

def pygame_lerp_main(screen):
  k = 100
  segment = 1
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

        if segment > 0:
          spts = []
          pts = []
          ev = []
          l1_pts = []
          l2_pts = []

          seg_step = 1 / segment
          # break origin-target segment into regions
          for i in range(segment):
            spts.append(gfn.lerp(origin, p, i * seg_step))
          spts.append(p)
          
          # get equilateral vertex of each segment
          sign = 1
          for i in range(len(spts) - 1):
            ev.append(gfn.get_equilateral_vertex(spts[i], spts[i+1], sign))
            sign = sign * -1
          
          # calculate lerp points
          n = 100
          step = 1 / n
          for sp in range(len(spts) - 1):
            for i in range(n):
              # lerp between origin and equilateral vertex
              l1 = gfn.lerp(spts[sp], ev[sp],step * i)
              # lerp between equilateral vertex and target
              l2 = gfn.lerp(ev[sp], spts[sp + 1], step * i)
              # lerp between lerps
              m1 = gfn.lerp(l1, l2, step * i)

              l1_pts.append(l1)
              l2_pts.append(l2)
              pts.append(m1)

          lerp_render(screen, n, spts, ev, l1_pts, l2_pts, pts)


          continue

    


      
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