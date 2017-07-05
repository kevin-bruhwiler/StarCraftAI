import cybw
import time
from copy import copy

MAX_DEPTH = 5
build_orders = []


def goal_reached(position, goal):
    return False


def build_time(build_order):
    return 5


class Tree:
    def __init__(self, data=None, parent=None, race=None, goal=None):
        self.data = data
        self.children = []
        self.new_addition = None
        self.parent = parent
        self.depth = 0
        self.race = race
        self.goal = goal
        self.build_orders = []

    # returns a list of all possible children that we could move to from node.
    def make_children(self):
        all_valid_units = [unit for unit in cybw.UnitTypes.allUnitTypes()
                           if unit.getRace() == self.race
                           and unit.isBuilding()
                           and not unit.isSpecialBuilding()
                           or unit.isWorker()]

        children = []
        for unit in all_valid_units:
            # ignore other race's workers
            if unit.getRace() != self.race:
                continue

            child = Tree(data=copy(self.data), parent=self, race=self.race, goal=self.goal)
            child.depth = self.depth + 1
            child.build_orders = self.build_orders

            if unit not in child.data:
                child.data[unit] = 1
            else:
                child.data[unit] += 1
            child.new_addition = unit
            if goal_reached(child.get_build_order(), child.goal):
                self.build_orders.append(child.get_build_order())
            else:
                children.append(child)
        return children

    def get_build_order(self):
        order = []
        node = self
        while node.parent is not None:
            order.insert(0, node.new_addition)
            node = node.parent
        return order

    # adds node to self.children
    def add_child(self, node):
        assert isinstance(node, Tree)
        if node.depth < MAX_DEPTH:
            self.children.append(node)

    # adds nodes to list.children
    def add_children(self, nodes):
        for node in nodes:
            if node.depth < MAX_DEPTH:
                self.add_child(node)

    def construct_and_search_tree(self):
        children = self.make_children()
        if len(children) > 0:
            self.add_children(children)
            for child in self.children:
                if child.depth < MAX_DEPTH:
                    child.construct_and_search_tree()


# Build Order Tree Search Simulator
class BOTSS:
    def __init__(self, start=None, goal=None):
        self.tree = Tree(data=start, goal=goal, race=list(start.keys())[0].getRace())
        self.start = start
        self.goal = goal
        self.optimal_build_order = None

    def find_optimal_build_order(self):
        time_start = time.time()

        # construct a search tree with a depth of MAXDEPTH
        self.tree.construct_and_search_tree()

        # all possible build orders are in self.tree.build_orders
        # determine the best build order
        best_time = 9999
        for build_order in self.tree.build_orders:
            tmp_time = build_time(build_order)
            if tmp_time < best_time:
                best_time = tmp_time
                self.optimal_build_order = build_order

        time_end = time.time()
        print("Total Execution time: " + (str(time_end - time_start)))


# test code
tree_search = BOTSS(start={cybw.UnitTypes.Protoss_Probe: 5, cybw.UnitTypes.Protoss_Nexus: 1},
                    goal={cybw.UnitTypes.Protoss_Nexus: 2,
                          cybw.UnitTypes.Protoss_Gateway: 2,
                          cybw.UnitTypes.Protoss_Stargate: 1})

tree_search.find_optimal_build_order()
