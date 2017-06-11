import cybw


client = cybw.BWAPIClient
Broodwar = cybw.Broodwar

class GameState:
    def __init__(self):
        pass

    def add_unit(self, unit):
        """
       :type unit: cybw.Unit
       """
        pass

    def remove_unit(self, unit):
        """
       :type unit: cybw.Unit
       """
        pass

    def update_unit(self, unit):
        """
       :type unit: cybw.Unit
       """
        if not unit.exists():
            return

    def update(self):
        for unit in Broodwar.self().getUnits():
            self.update_unit(unit)

