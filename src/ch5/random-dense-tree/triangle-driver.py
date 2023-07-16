#!/usr/bin/python3
import pygame
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
import time
import sys
import numpy as np

WHITE = 0
GRAY = 1
BLACK = 2


class Vertex:
    def __init__(self, coordinate):
        self.pt = coordinate
        self.neighbor_set = set()
        self.visited = WHITE
        self.neighbor_counter = 0

    def get_coord(self):
        return self.pt

    # def add_neighbor(self, target_pt):
    #   self.neighbor_list.append(target_pt)


class Edge:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2

    def get_triangle_theta(self, new_pt):
        delta1 = abs(get_delta_theta(self.pt2, self.pt1, new_pt))
        delta2 = abs(get_delta_theta(self.pt1, self.pt2, new_pt))
        return delta1 + delta2

    def get_out_of_normal(self, new_pt):
        delta2 = abs(get_delta_theta(self.pt1, self.pt2, new_pt))
        delta1 = abs(get_delta_theta(self.pt2, self.pt1, new_pt))
        return delta1 > np.pi / 2 or delta2 > np.pi / 2

    def get_triangle_perimeter(self, new_pt):
        r1 = mfn.euclidean_dist(self.pt1, new_pt)
        r2 = mfn.euclidean_dist(self.pt2, new_pt)

    def get_normal_dist(self, new_pt):
        h = mfn.euclidean_dist(self.pt1, new_pt)
        theta = abs(get_delta_theta(self.pt2, self.pt1, new_pt))
        return np.sin(theta) * h

    def get_normal_pt(self, new_pt):
        h = mfn.euclidean_dist(self.pt1, new_pt)
        theta = abs(get_delta_theta(self.pt2, self.pt1, new_pt))
        direction, r = mfn.car2pol(self.pt1, self.pt2)
        d = h * np.cos(theta)
        normal_pt = mfn.pol2car(self.pt1, d, direction)
        return normal_pt

    def break_edge(self, new_pt):
        d1 = mfn.euclidean_dist(self.pt1, new_pt)
        d2 = mfn.euclidean_dist(self.pt2, new_pt)
        new_edge = None
        if d1 < d2:
            new_edge = Edge(self.pt1, new_pt)
            self.pt1 = new_pt
        else:
            new_edge = Edge(new_pt, self.pt2)
            self.pt2 = new_pt
        # self.pt2 = new_pt
        return new_edge

    def get_pts(self):
        return (self.pt1, self.pt2)


def gen_van_der_corput(k_bits=4):
    """
    Generates van der corput sequence with k_bits
    Returns a list of floats between [0,1]
    """

    max_val = np.square(k_bits)
    seq = []
    for i in range(max_val):
        k = bin(i)[2:][::-1]
        print(k)
        if len(k) < k_bits:
            k = k + f"{(k_bits - len(k)) * '0'}"
        n = 0
        for j in range(len(k)):
            n += int(k[-1 - j]) * np.power(2, j)
        seq.append(np.divide(n, max_val))
    return seq


def adjust_angle(theta):
    """
    adjusts some theta to arctan2 interval [0,pi] and [-pi, 0]
    """
    if theta > np.pi:
        theta = theta + -2 * np.pi
    elif theta < -np.pi:
        theta = theta + 2 * np.pi

    return theta


def get_delta_theta(endpoint_1, vertex, endpoint_2):
    theta1, rad1 = mfn.car2pol(vertex, endpoint_1)
    theta2, rad2 = mfn.car2pol(vertex, endpoint_2)

    delta_theta = adjust_angle(theta2 - theta1)
    return delta_theta


def add_new_edge(edge_list, point_set, target_pt):
    nearest_el = []
    sortkey = lambda et: et[0]
    # get distance to all valid edges
    for i in range(len(edge_list)):
        if not edge_list[i].get_out_of_normal(target_pt):
            nearest_el.append((edge_list[i].get_normal_dist(target_pt), i))

    # get distance to all points
    nearest_pts = []
    for pt in point_set:
        nearest_pts.append((mfn.euclidean_dist(pt, target_pt), pt))
    # nearest_pts.append((1e9, (-1, -1)))
    nearest_pts = sorted(nearest_pts, key=sortkey)
    # print(nearest_pts)
    nearest_el = sorted(nearest_el, key=sortkey)
    edge_dist = 1e9  # set edge dist to some big constant
    pt_dist = 1e9
    if not len(nearest_pts) and not len(nearest_el):
        point_set.add(target_pt)
        return

    if len(nearest_el):
        edge_dist = nearest_el[0][0]

    pt_dist = nearest_pts[0][0]
    new_edge = None
    if pt_dist < edge_dist:
        new_edge = Edge(nearest_pts[0][1], target_pt)
    else:
        norm_pt = edge_list[nearest_el[0][1]].get_normal_pt(target_pt)
        print(norm_pt)
        intermediate_edge = edge_list[nearest_el[0][1]].break_edge(norm_pt)
        edge_list.append(intermediate_edge)
        point_set.add(norm_pt)
        new_edge = Edge(norm_pt, target_pt)

    point_set.add(target_pt)
    edge_list.append(new_edge)


def get_nearest_pt(edge_list, point_set, target_pt):
    nearest_el = []
    sortkey = lambda et: et[0]
    # get distance to all valid edges
    for i in range(len(edge_list)):
        if not edge_list[i].get_out_of_normal(target_pt):
            nearest_el.append((edge_list[i].get_normal_dist(target_pt), i))

    # get distance to all points
    nearest_pts = []
    for pt in point_set:
        nearest_pts.append((mfn.euclidean_dist(pt, target_pt), pt))

    nearest_pts = sorted(nearest_pts, key=sortkey)

    nearest_el = sorted(nearest_el, key=sortkey)
    edge_dist = 1e9  # set edge dist to some big constant
    pt_dist = 1e9

    if len(nearest_el):
        edge_dist = nearest_el[0][0]

    pt_dist = nearest_pts[0][0]
    new_edge = None
    nearest_pt = None
    if pt_dist < edge_dist:
        nearest_pt = nearest_pts[0][1]
    else:
        nearest_pt = edge_list[nearest_el[0][1]].get_normal_pt(target_pt)

    return nearest_pt


def interactive_triangle_test(screen):
    endpt_1 = (500, 500)
    endpt_2 = (600, 600)
    point_set = {endpt_1, endpt_2}
    edge_list = [Edge(endpt_1, endpt_2)]
    for e in edge_list:
        pt1, pt2 = e.get_pts()
        pafn.frame_draw_dot(screen, pt1, pafn.colors["white"])
        pafn.frame_draw_dot(screen, pt2, pafn.colors["white"])
        pafn.frame_draw_line(screen, (pt1, pt2), pafn.colors["indigo"])
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                pafn.clear_frame(screen)

                add_new_edge(edge_list, point_set, p)
                for e in edge_list:
                    pt1, pt2 = e.get_pts()
                    pafn.frame_draw_dot(screen, pt1, pafn.colors["white"])
                    pafn.frame_draw_dot(screen, pt2, pafn.colors["white"])
                    pafn.frame_draw_line(screen, (pt1, pt2), pafn.colors["indigo"])
                pygame.display.update()


def generate_points(origin=(500, 500), dim=500, input_sequence=[]):
    """
    Generates a sequence of points
    returns a list of (x,y)
    """
    pl = []
    x, y = origin
    for i in input_sequence:
        val = i - 0.5
        x = dim * val + dim
        y = dim * 2 - x
        pl.append((x, x))
    return pl


def get_rand_sequence(k=32):
    """
    Generates a random sequence of floats between 0,1000
    returns a sequence of points
    """
    rng = np.random.default_rng(12345)
    rand_val = lambda: (rng.uniform()) * 1000
    pl = []
    for i in range(k):
        x = rand_val()
        y = rand_val()
        pl.append((x, y))
    return pl


def sequence_test(screen, input_points):
    edge_list = []
    point_set = set()
    for p in input_points:
        # pafn.frame_draw_dot(i)
        pafn.clear_frame(screen)

        add_new_edge(edge_list, point_set, p)
        for e in edge_list:
            pt1, pt2 = e.get_pts()
            pafn.frame_draw_dot(screen, pt1, pafn.colors["white"])
            pafn.frame_draw_dot(screen, pt2, pafn.colors["white"])
            pafn.frame_draw_line(screen, (pt1, pt2), pafn.colors["indigo"])
        pygame.display.update()
        time.sleep(0.01)


def get_farthest_pt(obstacle_list, point_list, distance_thres=30):
    last_pt = None
    for i in range(len(point_list)):
        p = point_list[i]
        for o in obstacle_list:
            d = mfn.euclidean_dist(p, o)
            if d < distance_thres:
                print("breaking")
                return last_pt
        last_pt = p
    return last_pt


def sequence_with_goal_test(screen, input_points, goal_pt=(900, 100)):
    """
    Demonstrates RDT implementation
    """
    obs_list = get_rand_sequence(40)

    obs_rad = 20

    edge_list = []
    initial_point = (100, 900)
    point_set = {initial_point}
    step_size = obs_rad / 4
    rng = np.random.default_rng(32345)
    rand_val = lambda: (int(rng.uniform(0, 100)))
    for i in range(len(input_points)):
        p = input_points[i]
        if rand_val() == 1:
            p = goal_pt
        nearest_pt = get_nearest_pt(edge_list, point_set, p)
        step_count = (
            100  # max(int(mfn.euclidean_dist(nearest_pt, p) / step_size), 10) * 2
        )
        point_list = gfn.lerp_list(nearest_pt, p, step_count)

        # print(point_list)

        target_pt = get_farthest_pt(obs_list, point_list, 70)
        if target_pt != None:
            add_new_edge(edge_list, point_set, target_pt)
        for e in edge_list:
            pt1, pt2 = e.get_pts()
            pafn.frame_draw_dot(screen, pt1, pafn.colors["white"])
            pafn.frame_draw_dot(screen, pt2, pafn.colors["white"])
            pafn.frame_draw_line(screen, (pt1, pt2), pafn.colors["indigo"])
        for o_center in obs_list:
            pafn.frame_draw_dot(screen, o_center, pafn.colors["red"], obs_rad, obs_rad)

        pygame.display.update()
        time.sleep(0.05)
        if target_pt == goal_pt:
            print("path found!")
            break

    vertex_dict = {}
    for pt in point_set:
        vertex_dict[pt] = Vertex(pt)

    for edge in edge_list:
        p1, p2 = edge.get_pts()
        vertex_dict[p1].neighbor_set.add(p2)
        vertex_dict[p2].neighbor_set.add(p1)

    for vertex in vertex_dict:
        vertex_dict[vertex].neighbor_set = list(vertex_dict[vertex].neighbor_set)
    # queue = []
    stack = []  # stack.append(), stack.pop()
    curr_vertex = vertex_dict[initial_point]
    curr_vertex.visited = GRAY
    stack.append(curr_vertex)

    while stack[-1].get_coord() != target_pt:
        if stack[-1].neighbor_counter < len(stack[-1].neighbor_set):
            stack[-1].neighbor_counter += 1
            if (
                vertex_dict[
                    stack[-1].neighbor_set[stack[-1].neighbor_counter - 1]
                ].visited
                == WHITE
            ):
                stack.append(
                    vertex_dict[stack[-1].neighbor_set[stack[-1].neighbor_counter - 1]]
                )
                stack[-1].visited = GRAY
        else:
            stack[-1].visited = BLACK
            stack.pop()

    for v in range(1, len(stack)):
        pafn.frame_draw_cross(screen, stack[v - 1].get_coord(), pafn.colors["yellow"])
        pafn.frame_draw_bold_line(
            screen,
            (stack[v - 1].get_coord(), stack[v].get_coord()),
            pafn.colors["green"],
        )
        pygame.display.update()
        time.sleep(0.1)

    pafn.frame_draw_cross(screen, initial_point, pafn.colors["yellow"])
    pafn.frame_draw_cross(screen, goal_pt, pafn.colors["yellow"])
    pygame.display.update()

    time.sleep(5)
    sys.exit()


def main():
    pl = get_rand_sequence(600)

    pygame.init()
    screen = pafn.create_display(1000, 1000)
    pafn.clear_frame(screen)
    pygame.display.update()
    time.sleep(3)

    sequence_with_goal_test(screen, pl)


if __name__ == "__main__":
    main()
