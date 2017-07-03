import cybw
import UnitManager
import GameState


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
        if cybw.Broodwar.isReplay():
            for player in cybw.Broodwar.getPlayers():
                self.replay_game_states.append(GameState.GameState(player))
            for player in self.replay_game_states:
                player.initialize()
        else:
            self.game_state = GameState.GameState(cybw.Broodwar.self())
            self.unit_manager = UnitManager.UnitManager()

            self.unit_manager.initialize()
            self.game_states.initialize()
