import cybw


MAX_DEPTH = 100


class Tree:
    def __init__(self, data=None):
        self.data = data
        self.children = []
        self.depth = 0

    # returns a list of all possible children that we could move to from node.
    def make_children(self, node):
        return []

    # adds node to self.children
    def add_child(self, node):
        assert isinstance(node, Tree)
        node.depth = self.depth + 1
        if node.depth < MAX_DEPTH:
            self.children.append(node)

    # adds nodes to list.children
    def add_children(self, nodes):
        for node in nodes:
            node.depth = self.depth + 1
            if node.depth < MAX_DEPTH:
                self.add_child(node)


# Build Order Tree Search Simulator
class BOTSS:
    def __init__(self, start=None, goal=None):
        self.tree = Tree(start)
        self.goal = goal
        self.optimal_build = []

    def find_optimal_build_order(self, start, goal):
        # construct a tree with a depth of self.maxdepth

        # search this tree to find the optimal build order from start to goal

        # save off the best build order
        self.optimal_build = []

