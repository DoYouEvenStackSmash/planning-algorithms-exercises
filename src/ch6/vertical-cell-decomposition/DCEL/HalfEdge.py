#!/usr/bin/python3


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

    def get_next_half_edge(self):
        """
        Accessor for next half edge by _next ptr
        Returns a half edge
        """
        return self._next

    def get_prev_half_edge(self):
        """
        Accessor for prev half edge by _prev ptr
        Returns a half edge
        """
        return self._prev

    def get_twin_half_edge(self):
        """
        Accessor for twin half edge by _twin ptr
        Returns a half edge
        """
        return self._twin

    def get_source_vertex(self):
        """
        Accessor for source vertex of half edge
        Returns a vertex
        """
        return self.source_vertex
