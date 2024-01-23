#!/usr/bin/python3
from Vertex import Vertex
from HalfEdge import HalfEdge
from Face import Face


class DCEL:
    """
    Data structure for representing polyhedra

    Made up of faces, which are surrounded by half edges,
    every pair of which share a vertex.
    """

    def __init__(self, half_edge_records=None, vertex_records=None, face_records=None):
        self.half_edge_records = half_edge_records if half_edge_records != None else []
        self.vertex_records = vertex_records if vertex_records != None else []
        self.face_records = face_records if face_records != None else []

    def construct_global_edge_list(self):
        """
        Accessor for all chains, of all faces, stored in data structure
        """
        gel = []
        for face in self.face_records:
            interior_chains = face.get_interior_component_chains()
            interior_chains.append(face.get_boundary_chain())
            for edge_list in interior_chains:
                for edge in edge_list:
                    gel.append(edge)
        return gel

    def create_chain(self, point_list, face_ref=None):
        """
        Initializes a chain of half edges using an ORDERED list of points.
        The convention is that a vector normal to a directed half edge points into the obstacle free region

        returns a pointer to a single member of the chain
        """
        if len(point_list) < 2:
            print("Cannot create a chain with fewer than two points!")
            return None
        # face_ref = self.get_face(face_id)

        # initialize anchors
        anchor_vertex = self.add_vertex(Vertex(point_list[0]))
        anchor_edge = self.add_half_edge(
            HalfEdge(anchor_vertex, _bounded_face=face_ref)
        )
        anchor_vertex._half_edge = anchor_edge
        anchor_edge.source_vertex = anchor_vertex

        h = anchor_edge
        for i in range(1, len(point_list)):
            v = self.add_vertex(Vertex(point_list[i]))
            he = self.add_half_edge(HalfEdge(v, _bounded_face=face_ref))
            self.set_ev_pointers(he, v)
            h._next = he
            h._next._prev = h
            h = h._next
        h._next = anchor_edge
        h._next._prev = h
        return anchor_edge

    def create_face(self, boundary_points=None, interior_components=None):
        """
        Initializes a new face
        Returns the id of that face
        """

        bpts = boundary_points if boundary_points != None else []
        interior_pt_lists = interior_components if interior_components != None else []

        f = self.add_face(Face())
        f.boundary_edge = self.create_chain(bpts, f)
        for i in range(len(interior_pt_lists)):
            ic = self.create_chain(interior_pt_lists[i], f)
            if ic != None:
                f.interior_components.append(ic)
        return f._id

    def get_face(self, face_id=None):
        """
        Accessor for reference to a face object
        """
        if face_id == None or face_id > len(self.face_records) - 1:
            return None
        return self.face_records[face_id]

    def add_vertex(self, vertex):
        """
        Adds a vertex to the records
        returns the index of the vertex in the records
        """
        vertex._id = len(self.vertex_records)
        self.vertex_records.append(vertex)
        return self.vertex_records[-1]

    def add_half_edge(self, half_edge):
        """
        Adds a half edge to the records
        returns the index of the half edge in the records
        """
        half_edge._id = len(self.half_edge_records)
        self.half_edge_records.append(half_edge)
        return self.half_edge_records[-1]

    def add_face(self, face):
        """
        Add a face to the records
        returns the reference of the face in the records
        """
        face._id = len(self.face_records)
        self.face_records.append(face)
        return self.face_records[-1]

    def set_ev_pointers(self, edge, vertex):
        """
        Convencience function for setting reference
        """
        edge.source_vertex = vertex
        vertex._half_edge = edge
