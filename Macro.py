# import tensorflow as tf
import cybw

class Macro(object):
    """
    The Macro agent is a TensorFlow (TF) model receives the history of the game (see Gamestate.py), as input, and outputs
    the target gamestate. To get from current -> target, a genetic algorithm is used (see GA/)
    """
    def __init__(self):
        pass

    def prepare_input(self, game_states):
        """
        Converts game_states to be a TF input
        :type game_states: list(GameState.GameState)
        """
        pass

    def run(self):
        """
        Runs the TF model one time
        """
        pass

    def get_output(self):
        """
        Collects the output of the TF model, and converts it to a basic_game_state
        """
        return {cybw.UnitTypes.Terran_Command_Center: 2,
            cybw.UnitTypes.Terran_Starport: 1}
