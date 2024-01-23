#!/usr/bin/python3


class Face:
    """
    Face:
      A "flat" polygon embedded in R3.  Useful as a boundary representation.
    """

    def __init__(self, boundary_edge=None, interior_components=None):
        self.boundary_edge = boundary_edge
        self.interior_components = (
            interior_components if interior_components != None else []
        )
        self._id = None

    def get_boundary_chain(self):
        """
        Walks around the face, collecting half edge objects
        Returns a list of Half Edge objects
        """
        if self.boundary_edge == None:
            return []
        edge_list = []
        h = self.boundary_edge
        edge_list.append(h)
        h = h._next
        while h != self.boundary_edge:
            edge_list.append(h)
            h = h._next
        return edge_list

    def get_interior_component_chain(self, component_id=0):
        """
        Walks around the chain representing some interior component by component_id
        Returns a list of Half Edge Objects
        """

        edge_list = []
        if component_id > len(self.interior_components) - 1:
            print("component_id does not exist!")
            return edge_list

        h = self.interior_components[component_id]
        edge_list.append(h)
        h = h._next
        while h != self.interior_components[component_id]:
            edge_list.append(h)
            h = h._next
        return edge_list

    def get_interior_component_chains(self):
        """
        Accessor for all interior components
        Returns a list of lists of half edges
        """
        components_list = []
        for i in range(len(self.interior_components)):
            components_list.append(self.get_interior_component_chain(i))
        return components_list
