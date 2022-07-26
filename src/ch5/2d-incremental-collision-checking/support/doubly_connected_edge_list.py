#!/usr/bin/python3

'''
  Vertex:
    A point on the boundary of a region. 
'''
class Vertex:
  def __init__(self, point_coordinate = None,_half_edge = None):
    self.point_coordinate = point_coordinate
    self._half_edge = _half_edge
    self._id = None
  
  '''
    Accessor for the point coordinate
  '''
  def get_point_coordinate(self):
    if not self.point_coordinate:
      print(f"WARN: vertex does not have point coordinate!")
    return self.point_coordinate
  
  '''
    helper for adjusting point coordinate
  '''
  def set_point_coordinate(self, point_coordinate):
    self.point_coordinate = point_coordinate
  
'''
  Face:
    A "flat" polygon embedded in R3.  Useful as a boundary representation.
'''
class Face:
  def __init__(self, _half_edge = None):
    self._half_edge = _half_edge
    self._id = None
  
  '''
    Accessor for boundary half edge list head
  '''
  def get_half_edge(self):
    if self._half_edge == None:
      print(f"no half edge!")
    return self._half_edge
  '''
    Walks around the Face, collecting vertex objects
  '''
  def get_vertices(self):
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
  
  '''
    Walks around the face, collecting half edge objects
  '''
  def get_half_edges(self):
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

'''
  Half Edge
    A "directed" component of a doubly linked list around a face. Can access
    neighboring twin edge(if present), vertex object.
    
    source_vertex:  vertex shared with self._prev.
    _bounded_face:  reference to higher level Face object.
            _prev:  pointer to previous half edge in linked list.
            _next:  pointer to next half edge in linked list.
            _twin:  pointer to sibling half edge which encloses the neighboring face
'''  
class HalfEdge:
  def __init__(self, source_vertex = None, _bounded_face = None, _prev = None,_next = None, _twin = None):
    self.source_vertex = source_vertex
    self._bounded_face = _bounded_face
    self._next = _next
    self._prev = _prev
    self._twin = _twin
    self._id = None

'''
  Data structure for representing polyhedron
'''
class DoublyConnectedEdgeList:
  def __init__(self):
    self.half_edge_records = []
    self.vertex_records = []
    self.face_records = []
  
  def get_face_half_edge(self, face_id = None):
    if face_id == None:
      print(f"WARN: no face id specified")
      return []
    elif face_id >= len(self.face_records):
      print(f"WARN: face id not present in records!")
      return []
    return self.face_records[face_id].get_half_edge()
  '''
    get the vector components of the vertices surrounding the face
  '''
  def get_face_points(self, face_id = None):
    if face_id == None:
      print(f"WARN: no face id specified")
      return []
    elif face_id >= len(self.face_records):
      print(f"WARN: face id not present in records!")
      return []
    return [pt.get_point_coordinate() for pt in self.face_records[face_id].get_vertices()]
  
  '''
    get vertices on the boundary of the face
  '''
  def get_face_vertices(self, face_id = None):
    if face_id == None:
      print(f"WARN: no face id specified")
      return []
    elif face_id >= len(self.face_records):
      print(f"WARN: face id not present in records!")
      return []
    
    return self.face_records[face_id].get_vertices()

  '''
    get half edges enclosing the face
  '''
  def get_face_edges(self, face_id = None):
    if face_id == None:
      print(f"WARN: no face id specified")
      return []
    elif face_id >= len(self.face_records):
      print(f"WARN: face id not present in records!")
      return []
    
    return self.face_records[face_id].get_half_edges()
  
  '''
    constructs a new face from a point list.  
  '''
  def create_new_face(self, point_list = []):
    if not len(point_list):
      print(f"ERR: cannot create empty face!")
      return -1
    
    f_id = len(self.face_records)
    self.face_records.append(Face())
    
    self.vertex_records.append(Vertex(point_list[0]))
    
    h_id = len(self.half_edge_records)
    self.half_edge_records.append(HalfEdge(self.vertex_records[-1], self.face_records[-1]))
    
    self.vertex_records[-1]._half_edge = self.half_edge_records[-1]
    
    self.face_records[-1]._half_edge = self.half_edge_records[-1]
    
    for i in range(1, len(point_list)):
      self.vertex_records.append(Vertex(point_list[i]))
      
      h = HalfEdge(self.vertex_records[-1], self.face_records[-1], self.half_edge_records[-1])
      self.half_edge_records[-1]._next = h
      self.half_edge_records.append(h)

      self.vertex_records[-1]._half_edge = self.half_edge_records[-1]
    
    self.half_edge_records[-1]._next = self.half_edge_records[h_id]
    self.half_edge_records[h_id]._prev = self.half_edge_records[-1]

    self.face_records[f_id]._half_edge = self.half_edge_records[h_id]
    
    return f_id


      
    
