#!/usr/bin/python3

class Vertex:
  def __init__(self, point_coordinate = None,_half_edge = None):
    self.point_coordinate = point_coordinate
    self._half_edge = _half_edge
    self._id = None
  
  def get_point_coordinate(self):
    if not self.point_coordinate:
      print(f"WARN: vertex does not have point coordinate!")
    return self.point_coordinate
  
class Face:
  def __init__(self, _half_edge = None):
    self._half_edge = _half_edge
    self._id = None
  
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

  
class HalfEdge:
  def __init__(self, source_vertex = None, _bounded_face = None, _prev = None,_next = None, _twin = None):
    self.source_vertex = source_vertex
    self._bounded_face_ = _bounded_face
    self._next = _next
    self._prev = _prev
    self._twin = _twin
    self._id = None

  # def create_half_edge

class DoublyConnectedEdgeList:
  def __init__(self):
    self.half_edge_records = []
    self.vertex_records = []
    self.face_records = []
    
  def get_face_points(self, face_id = None):
    if face_id == None:
      print(f"WARN: no face id specified")
      return []
    elif face_id >= len(self.face_records):
      print(f"WARN: face id not present in records!")
      return []
    return [pt.get_point_coordinate() for pt in self.face_records[face_id].get_vertices()]
  
  def get_face_vertices(self, face_id = None):
    if face_id == None:
      print(f"WARN: no face id specified")
      return []
    elif face_id >= len(self.face_records):
      print(f"WARN: face id not present in records!")
      return []
    
    return self.face_records[face_id].get_vertices()

  
  def create_new_face(self, point_list = []):
    if not len(point_list):
      print(f"ERR: cannot create empty face!")
      return -1
    # f = Face()
    f_id = len(self.face_records)
    self.face_records.append(Face())
    
    self.vertex_records.append(Vertex(point_list[0]))
    
    h_id = len(self.half_edge_records)
    self.half_edge_records.append(HalfEdge(self.vertex_records[-1], self.face_records[-1]))
    
    self.vertex_records[-1]._half_edge = self.half_edge_records[-1]
    
    self.face_records[-1]._half_edge = self.half_edge_records[-1]
    
    # head = self.half_edge_records[-1]
    # f = self.face_records[-1]
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


      
    
