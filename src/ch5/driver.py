#!/usr/bin/python3
from polygon import *
from render_support import *
from point_file_loader import *
import sys
import time

def main():
  if len(sys.argv) < 2:
    print("provide a file")
    sys.exit()
  p = load_json_file(sys.argv[1])
  if not len(p):
    print(f"json file did not load.")
    sys.exit()
  P = Polygon(p)

  pygame.init()
  w, h = 500,500
  screen = create_display(w, h)
  pts = [i.get_component_vec() for i in P.dump_points()]
  frame_draw_polygon(screen, pts, colors["magenta"])
  pygame.display.update()

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

main()