import cybw
import UnitManager
import GameState


class StarCraftAI:
    def __init__(self):
        self.unit_manager = UnitManager.UnitManager()
        self.game_state = GameState.GameState()

    def run(self):
        self.unit_manager.manage()

    def initialize(self):
        self.unit_manager.initialize()
        self.game_state.initialize()
