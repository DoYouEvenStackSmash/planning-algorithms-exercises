#!/usr/bin/python3


class Vertex:
    """
    Vertex:
      A point on the boundary of a region.

    """

    def __init__(self, point_coordinate=None, _half_edge=None):
        self.point_coordinate = point_coordinate
        self._half_edge = _half_edge
        self._id = None
        self.rank = -1

    def get_point_coordinate(self):
        """
        Accessor for the point coordinate
        Returns an (x,y) point
        """
        if not self.point_coordinate:
            print(f"WARN: vertex does not have point coordinate!")
        return self.point_coordinate

    def set_point_coordinate(self, point_coordinate):
        """
        helper for adjusting point coordinate
        """
        self.point_coordinate = point_coordinate


class Face:
    """
    Face:
      A "flat" polygon embedded in R3.  Useful as a boundary representation.
    """

    def __init__(self, _half_edge=None, obs_space=1):
        self._half_edge = _half_edge
        self.norm_direction = obs_space
        self._id = None

    def get_half_edge(self):
        """
        Accessor for boundary half edge list head
        Returns a Half Edge
        """
        if self._half_edge == None:
            print(f"no half edge!")
        return self._half_edge

    def get_vertices(self):
        """
        Walks around the Face, collecting vertex objects
        Returns a list of Vertex objects
        """
        if self._half_edge == None:
            return []
        vtx = []
        h = self._half_edge
        vtx.append(h.source_vertex)
        h = h._next
        while h != self._half_edge:
            vtx.append(h.source_vertex)
            h = h._next
        return vtx

    def get_half_edges(self):
        """
        Walks around the face, collecting half edge objects
        Returns a list of Half Edge objects
        """
        if self._half_edge == None:
            return []
        edge_list = []
        h = self._half_edge
        edge_list.append(h)
        h = h._next
        while h != self._half_edge:
            edge_list.append(h)
            h = h._next
        return edge_list


class HalfEdge:
    """
    Half Edge
      A "directed" component of a doubly linked list around a face. Can access
      neighboring twin edge(if present), vertex object.

      source_vertex:  vertex shared with self._prev.
      _bounded_face:  reference to higher level Face object.
              _prev:  pointer to previous half edge in linked list.
              _next:  pointer to next half edge in linked list.
              _twin:  pointer to sibling half edge which encloses the neighboring face
    """

    def __init__(
        self, source_vertex=None, _bounded_face=None, _prev=None, _next=None, _twin=None
    ):
        self.source_vertex = source_vertex
        self._bounded_face = _bounded_face
        self._next = _next
        self._prev = _prev
        self._twin = _twin
        self._id = None

    def get_next_vertex_segment(self):
        """
        Accessor for pair of vertices, curr->next
        """
        return (self.source_vertex, self._next.source_vertex)

    def get_prev_vertex_segment(self):
        """
        Accessor for pair of vertices, prev->curr
        """
        return (self._prev.source_vertex, self.source_vertex)


class DoublyConnectedEdgeList:
    """
    Data structure for representing polyhedra

    Made up of faces, which are surrounded by half edges,
    every pair of which share a vertex.
    """

    def __init__(self, half_edge_records=None, vertex_records=None, face_records=None):
        self.half_edge_records = half_edge_records if half_edge_records != None else []
        self.vertex_records = vertex_records if vertex_records != None else []
        self.face_records = face_records if face_records != None else []

    def get_face_vertices_walk(self):
        """
        Accessor for walking all faces and accumulating vertices
        """
        pts = []
        for f in self.face_records:
            pts.append(f.get_vertices())
        return pts

    def get_face_edges_walk(self):
        """
        Accessor for walking all faces and accumulating edges
        """
        edges = []
        for f in self.face_records:
            edges.append(f.get_half_edges())
        return edges

    def get_faces(self, face_id=None):
        """
        Accessor for a specific face
        """
        if face_id == None:
            print("NO face id specified")
            return []
        return [self.face_records[face_id]]

    def get_other_faces(self, origin_face_id=None):
        """
        Retrieves faces other than the one specified
        """
        if origin_face_id == None:
            print(f"WARN: no face id specified")
            return []
        else:
            face_list = []
            for f in self.face_records:
                if f._id == origin_face_id:
                    print("skipping")
                    continue
                else:
                    face_list.append(f)
            return face_list

    def get_other_faces_edges(self, origin_face_id=None):
        """
        Accessor for half edges in faces other than the one specified
        """
        if origin_face_id == None:
            print(f"WARN: no face id specified")
            return []
        else:
            fl = self.get_other_faces(origin_face_id)
            half_edge_list = []
            for face in fl:
                half_edge_list.append(face.get_half_edges())
            return half_edge_list

    def get_face_half_edge(self, face_id=None):
        """
        Accessor for the lead half edge of a given face_id
        Returns a single half edge
        """
        if face_id == None:
            print(f"WARN: no face id specified")
            return []
        elif face_id >= len(self.face_records):
            print(f"WARN: face id not present in records!")
            return []
        return self.face_records[face_id].get_half_edge()

    def get_face_points(self, face_id=None):
        """
        Accessor for points on the perimeter of a face
        Returns a list of (x,y) points
        """
        if face_id == None:
            print(f"WARN: no face id specified")
            return []
        elif face_id >= len(self.face_records):
            print(f"WARN: face id not present in records!")
            return []
        return [
            pt.get_point_coordinate()
            for pt in self.face_records[face_id].get_vertices()
        ]

    def get_face_vertices(self, face_id=None):
        """
        Accessor for vertices on the boundary of a face
        Returns a list of Vertex objects
        """
        if face_id == None:
            print(f"WARN: no face id specified")
            return []
        elif face_id >= len(self.face_records):
            print(f"WARN: face id not present in records!")
            return []

        return self.face_records[face_id].get_vertices()

    def get_face_edges(self, face_id=None):
        """
        Accessor for half edges which enclose a face
        Returns a list of Half Edges
        """
        if face_id == None:
            print(f"WARN: no face id specified")
            return []
        elif face_id >= len(self.face_records):
            print(f"WARN: face id not present in records!")
            return []

        return self.face_records[face_id].get_half_edges()

    def create_new_face(self, point_list=[], obs_space=1):
        """
        Constructs a new face from a list of (x,y) points.
        Returns integer id of created face
        """
        if not len(point_list):
            print(f"ERR: cannot create empty face!")
            return -1

        # initialize face
        f_id = len(self.face_records)
        self.face_records.append(Face(obs_space=obs_space))

        # initialize first vertex
        self.vertex_records.append(Vertex(point_list[0]))

        # initialize first half edge, with origin at newest Vertex, belonging to newest Face
        h_id = len(self.half_edge_records)
        self.half_edge_records.append(
            HalfEdge(self.vertex_records[-1], self.face_records[-1])
        )

        # Add pointer from newest Vertex to newest Half Edge
        self.vertex_records[-1]._half_edge = self.half_edge_records[-1]

        # Add pointer from newest Face to newest Half Edge
        self.face_records[-1]._half_edge = self.half_edge_records[-1]

        for i in range(1, len(point_list)):
            # create new Vertex
            self.vertex_records.append(Vertex(point_list[i]))

            # create new Half Edge, origin at newest Vertex, belonging to newest Face
            h = HalfEdge(
                self.vertex_records[-1],
                self.face_records[-1],
                self.half_edge_records[-1],
            )
            self.half_edge_records[-1]._next = h
            self.half_edge_records.append(h)

            # Add pointer from newest Vertex to newest Half Edge
            self.vertex_records[-1]._half_edge = self.half_edge_records[-1]

        # add newest half edge to doubly linked list of Face
        self.half_edge_records[-1]._next = self.half_edge_records[h_id]
        self.half_edge_records[h_id]._prev = self.half_edge_records[-1]

        # Add pointer from Face to newest Half Edge
        self.face_records[f_id]._half_edge = self.half_edge_records[h_id]

        # add face_id
        self.face_records[f_id]._id = f_id

        return f_id

    # def split_face(self, face_id=None):
    #     if face_id == None:
    #         print("WARN: No face id specified, cannot split face!")
