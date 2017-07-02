import cybw

client = cybw.BWAPIClient
broodwar = cybw.Broodwar
HISTORY_THRESHOLD = 100


def distance(game_state1, game_state2):
    return 5


class GameState:
    def __init__(self, player):
        self.features = {'unit_features': {}, 'building_features': {}}

        self.history = []
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
            # TODO: if unit is a building, update getReaminingBuildTime if the building wasn't completed when it was
            # last seen
            print('got here')
            return

        if unit.getType().isBuilding():
            self.features['building_features'][unit.getID()] = {'team': unit.getPlayer(),
                                                                'type': unit.getType(),
                                                                'hp': unit.getHitPoints(),
                                                                'pos_x': unit.getPosition().x,
                                                                'pos_y': unit.getPosition().y,
                                                                'build_time_remaining': unit.getRemainingBuildTime(),
                                                                'is_built': unit.isCompleted()}
            if unit.getType().getRace().getID() != cybw.Races.Zerg.getID():
                self.features['building_features'][unit.getID()]['shields'] = unit.getShields()

        else:
            self.features['unit_features'][unit.getID()] = {'team': unit.getPlayer(),
                                                            'type': unit.getType(),
                                                            'hp': unit.getHitPoints(),
                                                            'pos_x': unit.getPosition().x,
                                                            'pos_y': unit.getPosition().y}

            if unit.getType().getRace().getID() != cybw.Races.Zerg.getID():
                self.features['unit_features'][unit.getID()]['shields'] = unit.getShields()

    def remove_unit(self, unit):
        """
       :type unit: cybw.Unit
       """
        if unit.getType().isBuilding():
            if unit.getID() in self.features['building_features']:
                del self.features['building_features'][unit.getID()]
        else:
            if unit.getID() in self.features['unit_features']:
                del self.features['unit_features'][unit.getID()]

    def initialize(self):
        self.update()

    def update(self):
        for unit in broodwar.getAllUnits():
            if unit.isVisible(self.player):
                self.update_unit(unit)

        self.features['time'] = broodwar.elapsedTime()

        if len(self.history) == 0:
            self.history.append(self.features)
        else:
            dist = distance(self.history[-1], self.features)
            if dist >= HISTORY_THRESHOLD:
                self.history.append(self.features)

    # returns only the amounts of every unit in features that belongs to player
    def basic_game_state(self, player):
        basic = {}
        for key, value in self.features.items():
            if isinstance(value, dict):
                for unit_id, features in value.items():
                    if features['team'] == player:
                        if features['type'] in basic:
                            basic[features['type']] += 1
                        else:
                            basic[features['type']] = 1
        return basic
