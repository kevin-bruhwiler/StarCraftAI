import cybw
import UnitManager
import GameState


class StarCraftAI:
    def __init__(self):
        self.unit_manager = None
        self.game_state = []

    def run(self):
        if not cybw.Broodwar.isReplay():
            self.unit_manager.manage()

    def initialize(self):
        if cybw.Broodwar.isReplay():
            print(len(cybw.Broodwar.getPlayers()))
            for player in cybw.Broodwar.getPlayers():
                self.game_state.append(GameState.GameState(player))
            for player in self.game_state:
                player.initialize()
        else:
            self.game_state = GameState.GameState(cybw.Broodwar.self())
            self.unit_manager = UnitManager.UnitManager()

            self.unit_manager.initialize()
            self.game_state.initialize()
