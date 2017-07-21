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
        """
        Gets called every frame, calls every sub-controller to run
        """
        for event in cybw.Broodwar.getEvents():
            if event.getType() == cybw.EventType.UnitDestroy:
                if cybw.Broodwar.isReplay():
                    for player_state in self.replay_game_states:
                        player_state.remove_unit(event.getUnit())
                else:
                    self.game_state.remove_unit(event.getUnit())
            elif event.getType() == cybw.EventType.UnitMorph:
                if cybw.Broodwar.isReplay():
                    for player_state in self.replay_game_states:
                        player_state.update_unit(event.getUnit())
                else:
                    self.game_state.update_unit(event.getUnit())
            elif event.getType() == cybw.EventType.UnitShow:
                if cybw.Broodwar.isReplay():
                    for player_state in self.replay_game_states:
                        player_state.update_unit(event.getUnit())
                else:
                    self.game_state.update_unit(event.getUnit())
            elif event.getType() == cybw.EventType.UnitHide:
                    pass

        if not cybw.Broodwar.isReplay():
            self.unit_manager.manage()

        if cybw.Broodwar.isReplay():
            for state in self.replay_game_states:
                state.update()

        else:
            self.game_state.update()
            if self.game_state.history_added:
                self.macro_agent.prepare_input(self.game_state.history)
                self.macro_agent.run()

    def initialize(self):
        """
        Intialize every sub-controller
        """
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
    def build_order_parser():
        """
        Load in a predefined build order from file
        """
        working_dir = os.path.dirname(os.path.abspath(__file__))
        # Add pathing to each race's buildorders depending on their race
        absolute_path = os.path.join(working_dir, "buildOrders", "Terran", "testOrder.txt")
        build_order = [build_order.rstrip('\n') for build_order in open(absolute_path)]
        return build_order
