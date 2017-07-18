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
        pass

    def run(self):
        pass

    def get_output(self):
        return {cybw.UnitTypes.Terran_Command_Center: 2,
            cybw.UnitTypes.Terran_Starport: 1}
