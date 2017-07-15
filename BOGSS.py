import cybw
import time

MAX_DEPTH = 5
build_orders = []

# 1. Construct a graph of every possible build order for the given race.
# 2. Pickle graph
# 3. Before the game loads, load in the pickled graph
# 4. With the loaded graph, search for optimal build orders
#  ---> still might not be able to run in real time.

# Build Order Graph Search Simulator
class BOGSS:
    def __init__(self, start=None, goal=None):
        # graph = { "a" : ["c"],
        # "b" : ["c", "e"],
        #  "c" : ["a", "b", "d", "e"],
        #  "d" : ["c"],
        #  "e" : ["c", "b"],
        #  "f" : []
        # }
        self.graph = {}
        self.start = start
        self.goal = goal
        self.optimal_build_order = None

    def construct_graph(self):
        pass

    def find_optimal_build_order(self):
        time_start = time.time()

        time_end = time.time()
        print("Total Execution time: " + (str(time_end - time_start)))


# test code
graph_search = BOGSS(start={cybw.UnitTypes.Protoss_Probe: 5, cybw.UnitTypes.Protoss_Nexus: 1},
                     goal={cybw.UnitTypes.Protoss_Nexus: 2,
                          cybw.UnitTypes.Protoss_Gateway: 2,
                          cybw.UnitTypes.Protoss_Stargate: 1})
