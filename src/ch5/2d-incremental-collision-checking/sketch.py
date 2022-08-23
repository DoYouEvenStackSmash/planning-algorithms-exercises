

from turtle import width


def find_contact(star_list, screen):
  
  I1 = 0
  I2 = 0
  NO_MATCH = True
  while star_list[I2][1]._bounded_face == star_list[I1][1]._bounded_face and I2 < len(star_list):
    I2+=1
  # assume that we have found the first edge in other polygon
  T_OOB_HYPOTENUSE = -3
  T_OOB_NORM = -1
  T_OOB_EDGE = -2
  T_IN_VOR_EDGE = 1
  END = False

  
  
  while I1 < len(star_list) and I2 < len(star_list):
    
    val = t_in_vor_edge(star_list[I1][1], star_list[I2][1].source_vertex.get_point_coordinate())

    if val == T_OOB_HYPOTENUSE:
      neighbor_edge = star_list[I1][1]._next
      neighbor_val = t_in_vor_edge(neighbor_edge, star_list[I2][1].source_vertex.get_point_coordinate())
      if neighbor_val == T_OOB_NORM:
        print("VV found!")
        VV_found(neighbor_edge.source_vertex, star_list[I2][1].source_vertex, screen)
        NO_MATCH = False
        break
      elif neighbor_val == T_IN_VOR_EDGE:
        print("neigbor happens to have EV!")
        EV_found(neighbor_edge, star_list[I2][1].source_vertex, screen)
        NO_MATCH = False
        break
        # return
      elif neighbor_val == T_OOB_EDGE:
        print("nothing interesting found.")
      else:
        print("somehow val isn't what it should be?")
    elif val == T_IN_VOR_EDGE:
      print("EV found!")
      EV_found(star_list[I1][1], star_list[I2][1].source_vertex, screen)
      NO_MATCH = False
      break
      # return
    elif val == T_OOB_EDGE: # val = T_OOB_EDGE, which means it could be anywhere and we therefore don't care.
      print("nothing interesting found")
    else:
      print("somehow val isn't what it should be?")
    
    mark_edge_clear(star_list[I1][1], screen)
    # mark_vertex_clear()
    e_hold = star_list[I1][1]._next
    while I1 < len(star_list) and star_list[I1][1] != e_hold:
      I1+=1
    
    # if I1 is at star list oob, we must wrap to 0 for the last edge
    if I1 == len(star_list):
      break
    # make sure I1 is always trailing
    #swap(I1, I2)
    if not END and I1 > I2:
      temp = I1
      I1 = I2
      I2 = temp
    elif I1 == I2:
      print("not sure how this one happened.")
      
    # we can assume the next I1 has been found
    #goto next 
  if NO_MATCH:
    print("must be wrapped to beginning of unit circle")

def mark_vertex_clear(v, screen):
  frame_draw_dot(screen, v.get_point_coordinates(), colors["tangerine"], 1)
  pygame.display.update()



def mark_edge_clear(edge, screen):
  e_p1 = edge.source_vertex.get_point_coordinate()
  e_p2 = edge._next.source_vertex.get_point_coordinate()
  frame_draw_line(screen, [e_p1, e_p2], colors["tangerine"])
  pygame.display.update()

def VV_found(v1,v2, screen):
  p1 = v1.get_point_coordinate()
  p2 = v2.get_point_coordinate()
  frame_draw_bold_line(screen,[p1,p2], colors["magenta"])
  pygame.display.update()

def EV_found(edge, v1, screen):
    e_p1 = edge.source_vertex.get_point_coordinate()
    e_p2 = edge._next.source_vertex.get_point_coordinate()
    l = get_unit_norm(e_p1,e_p2)
    e_mid = l.get_origin()
    v_p = v1.get_point_coordinate()
    frame_draw_bold_line(screen, [e_mid, v_p], colors["cyan"])
    pygame.display.update()
    

