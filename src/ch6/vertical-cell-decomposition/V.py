class V:
    """
    Abstraction for constructing an undirected graph
    Rarely used
    """

    def __init__(self, coordinate, neighbor_dict=None):
        self.pt = coordinate
        self.neighbor_dict = neighbor_dict if neighbor_dict != None else {}
        self.neighbor_counter = 0

    def get_coord(self):
        return self.pt
