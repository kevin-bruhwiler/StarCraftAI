import cybw

client = cybw.BWAPIClient
Broodwar = cybw.Broodwar


class GameState:
    def __init__(self, player):
        self.unit_features = {}
        self.building_features = {}

        self.history = None
        self.player = player

    def update_unit(self, unit):
        """
       :type unit: cybw.Unit
       """
        if not unit.exists():
            return

        if unit.getType().isMineralField() or unit.getType().getID() == 188:  # 188 is vespene geyser
            return

        if not unit.isVisible(self.player):
            return

        if unit.getType().isBuilding():
            self.building_features[unit.getID()] = {'team': unit.getPlayer(),
                                                    'type': unit.getType(),
                                                    'hp': unit.getHitPoints(),
                                                    'pos_x': unit.getPosition().x,
                                                    'pos_y': unit.getPosition().y,
                                                    'build_time_remaining': unit.getRemainingBuildTime(),
                                                    'is_built': unit.isCompleted()}
            if unit.getType().getRace().getID() != cybw.Races.Zerg.getID():
                self.building_features[unit.getID()]['shields'] = unit.getShields()

            if unit.getID() in self.building_features:
                print(str(self.player) + ": Updated Building " + str(unit.getID()))
            else:
                print(str(self.player) + ": Added building" + str(unit.getID()))
        else:
            self.unit_features[unit.getID()] = {'team': unit.getPlayer(),
                                                'type': unit.getType(),
                                                'hp': unit.getHitPoints(),
                                                'pos_x': unit.getPosition().x,
                                                'pos_y': unit.getPosition().y}

            if unit.getType().getRace().getID() != cybw.Races.Zerg.getID():
                self.unit_features[unit.getID()]['shields'] = unit.getShields()

            if unit.getID() in self.unit_features:
                print(str(self.player) + ": Updated unit " + str(unit.getID()))
            else:
                print(str(self.player) + ": Added new unit " + str(unit.getID()))

    def remove_unit(self, unit):
        """
       :type unit: cybw.Unit
       """
        if unit.getType().isBuilding():
            if unit.getID().isBuilding():
                if unit.getID() in self.building_features:
                    del self.building_features[unit.getID()]
                    print(str(self.player) + ": Removed building " + str(unit.getID()))
        else:
            if unit.getID() in self.building_features:
                del self.unit_features[unit.getID()]
                print(str(self.player) + ": Removed unit " + str(unit.getID()))

        print(str(self.player) + ": removed unit " + str(unit.getID()))

    def initialize(self):
        pass

    def update(self):
        for unit in Broodwar.getAllUnits():
            if unit.isVisible(self.player):
                self.update_unit(unit)
