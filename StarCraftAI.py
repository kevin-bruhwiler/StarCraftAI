
import cybw
import UnitManager
import GameState
import os

UPDATE_INTERVAL = 5


class StarCraftAI:

    def __init__(self):
        self.unit_manager = None
        self.game_state = None
        self.replay_game_states = []

    def run(self):
        if not cybw.Broodwar.isReplay():
            self.unit_manager.manage()

        if cybw.Broodwar.isReplay():
            for state in self.replay_game_states:
                state.update()
                print(state.basic_game_state(state.player))

        else:
            self.game_state.update()
            print(self.game_state.basic_game_state(self.game_state.player))

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

            self.unit_manager.initialize()
            self.game_state.initialize()
            self.build_order_parse()

    def build_order_parse(self):
        working_dir = os.path.dirname(os.path.abspath(__file__))
        # Add pathing to each race's buildorders depending on their race
        absolute_path = os.path.join(working_dir, "buildOrders", "Terran", "testOrder.txt")
        build_order = [build_order.rstrip('\n') for build_order in open(absolute_path)]
        return build_order
