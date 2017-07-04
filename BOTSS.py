import cybw
import time

MAX_DEPTH = 100


class Tree:
    def __init__(self, data=None, parent=None, race=None):
        self.data = data
        self.children = []
        self.parent = parent
        self.depth = 0
        self.race = race

    # returns a list of all possible children that we could move to from node.
    def make_children(self):
        base_data = self.data
        all_valid_units = [unit for unit in cybw.UnitTypes.allUnitTypes()
                           if unit.getRace() == self.race
                           and unit.isBuilding()
                           and not unit.isSpecialBuilding()
                           or (unit.isWorker() and unit.getRace() == self.race)]
        children = []
        for unit in all_valid_units:
            child = Tree(data=base_data, parent=self, race=self.race)
            child.depth = self.depth + 1
            if unit not in child.data:
                child.data[unit] = 1
            else:
                child.data[unit] += 1
                print(child.data)
            children.append(child)
        return children

    # adds node to self.children
    def add_child(self, node):
        assert isinstance(node, Tree)
        if node.depth < MAX_DEPTH:
            self.children.append(node)
            return True;
        return False;
        print("Node Depth: " + (str)(node.depth))

    # adds nodes to list.children
    def add_children(self, nodes):
        for node in nodes:
            if node.depth < MAX_DEPTH:
                self.add_child(node)
                return True;
            return False;

    def construct_tree(self):
        children = self.make_children()
        if len(children) > 0:
            if self.add_children(children) :
                for child in self.children:
                    if child.depth < MAX_DEPTH:
                        child.construct_tree()
                        print("Child Depth: " + (str)(child.depth))


# Build Order Tree Search Simulator
class BOTSS:
    def __init__(self, start=None, goal=None):
        self.tree = Tree(start)
        self.goal = goal
        self.optimal_build = []

    def find_optimal_build_order(self, start, goal):
        # construct a tree with a depth of MAXDEPTH

        # search this tree to find the optimal build order from start to goal

        # save off the best build order
        self.optimal_build = []


# test code
tree_search = BOTSS()
tree_search.tree.data = {cybw.UnitTypes.Protoss_Probe: 5, cybw.UnitTypes.Protoss_Nexus: 1}
tree_search.tree.race = list(tree_search.tree.data.keys())[0].getRace()
time_start = time.time()
tree_search.tree.construct_tree()
time_end = time.time()
print("Total Execution time: " + (str)(time_end - time_start))

