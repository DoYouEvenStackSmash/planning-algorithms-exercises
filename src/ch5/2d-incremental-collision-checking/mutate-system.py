#!/usr/bin/python3
'''
  FPT is a lambda function describing some modification to the system
  FPTargs are the arguments to FPT
  OPList is the list of observing polygons which need to be considered
'''

# FPT = rotate_polygon
def get_step_rotation_matrix(P, t):
  rad_theta = compute_rotation(P.get_front_edge(), t)
  deg = abs(rad_theta * 180 / np.pi)
  step_rad = rad_theta / deg
  r_mat = get_cc_rotation_matrix(step_rad)
  return (deg,r_mat)

def gradually_rotate_system(OPList, P_index, t, screen = None):
  steps, r_mat = get_step_rotation_matrix(OPList[P_index], t)
  for step in range(steps):
    rotate_polygon(OPList[P_index], r_mat)
    for i in range(len(OPList)):
      sanity_check_polygon(screen, OPList[i])

    


