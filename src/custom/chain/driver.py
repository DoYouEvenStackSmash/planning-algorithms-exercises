#!/usr/bin/python3
import pygame

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
  origin = (400,400)
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
        pafn.frame_draw_line(screen,(origin,p),pafn.colors["yellow"])
        pafn.frame_draw_dot(screen,p,pafn.colors["yellow"])
        pafn.frame_draw_dot(screen,origin,pafn.colors["green"])
        ev = gfn.get_equilateral_vertex(origin, p)
        print(ev)
        pafn.frame_draw_line(screen,(p,ev),pafn.colors["yellow"])
        pafn.frame_draw_line(screen,(ev,origin),pafn.colors["yellow"])
        pafn.frame_draw_dot(screen,ev,pafn.colors["cyan"])
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