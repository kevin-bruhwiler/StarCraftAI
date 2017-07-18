import cybw
import UnitManager
import GameState
import Macro
import BuildingManager
from GA import BOGASS

import os

UPDATE_INTERVAL = 5


class StarCraftAI:
    def __init__(self):
        self.unit_manager = None
        self.game_state = None
        self.replay_game_states = []
        self.macro_agent = Macro.Macro()
        self.building_Manager = None

    def run(self):
        if not cybw.Broodwar.isReplay():
            self.unit_manager.manage()
            self.building_Manager.assign_workers_to_unassigned_buildings()

        if cybw.Broodwar.isReplay():
            for state in self.replay_game_states:
                state.update()
                print(state.basic_game_state(state.player))

        else:
            self.game_state.update()
            if self.game_state.history_added:
                self.macro_agent.prepare_input(self.game_state.history)
                self.macro_agent.run()
                # build_order_finder = BOGASS.BOGASS(start=self.game_state.basic_game_state(), goal=self.macro_agent.get_output())
                # build_order_finder.find_optimal_build_order()


    def initialize(self):
        cybw.Broodwar.setCommandOptimizationLevel(2)
        if cybw.Broodwar.isReplay():
            for player in cybw.Broodwar.getPlayers():
                self.replay_game_states.append(GameState.GameState(player))
            for player in self.replay_game_states:
                player.initialize()
        else:
            self.game_state = GameState.GameState(cybw.Broodwar.self())
            self.unit_manager = UnitManager.UnitManager()
            self.building_Manager = BuildingManager.BuildingManager()

            self.unit_manager.initialize()
            self.game_state.initialize()
            # self.build_order_parser()


    @staticmethod
    def build_order_parser(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        # Add pathing to each race's buildorders depending on their race
        absolute_path = os.path.join(working_dir, "buildOrders", "Terran", "testOrder.txt")
        build_order = [build_order.rstrip('\n') for build_order in open(absolute_path)]
        return build_order
