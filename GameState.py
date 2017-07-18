import cybw
import math

client = cybw.BWAPIClient
broodwar = cybw.Broodwar
HISTORY_THRESHOLD = 100


def euclidian_distance(x1, y1, x2, y2):
    """
    computes the  euclidean distance between (x1, y1) and (x2, y2). Right now, the metrics are arbitary.
    :type x1: cybw.Position.x
    :type y2: cybw.Position.y
    :type x2: cybw.Position.x
    :type y2: cybw.Position.y
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def distance(game_state1, game_state2):
    """
    computes the distance between gamestate 1 and gamestate 2. Right now, the metrics are arbitary.
    :type game_state1: GameState.GameState
    :type game_state2: GameState.GameState
    """
    final_distance = 0
    for unit_id, features in game_state1['building_features'].items():
        # this building has been destroyed
        if unit_id not in game_state2['building_features']:
            final_distance += HISTORY_THRESHOLD
        else:
            # the building is now complete
            if not game_state1['building_features'][unit_id]['is_built'] and game_state2['building_features'][unit_id]['is_built']:
                final_distance += HISTORY_THRESHOLD / 2
            if broodwar.getUnit(unit_id).getType().getRace() == cybw.Races.Terran:
                final_distance += euclidian_distance(game_state1['building_features'][unit_id]['pos_x'],
                                                     game_state1['building_features'][unit_id]['pos_y'],
                                                     game_state2['building_features'][unit_id]['pos_x'],
                                                     game_state2['building_features'][unit_id]['pos_y'])
            old_health = game_state1['building_features'][unit_id]['hp'] + game_state1['building_features'][unit_id]['shields']
            new_health = game_state2['building_features'][unit_id]['hp'] + game_state2['building_features'][unit_id]['shields']
            final_distance += abs(old_health - new_health) ** .5
    for unit_id, features in game_state2['building_features'].items():
        # this building is new to the game
        if unit_id not in game_state1['building_features']:
            final_distance += HISTORY_THRESHOLD
        else:
            # the building is now complete
            if not game_state1['building_features'][unit_id]['is_built'] and game_state2['building_features'][unit_id]['is_built']:
                final_distance += HISTORY_THRESHOLD / 2
            if broodwar.getUnit(unit_id).getType().getRace() == cybw.Races.Terran:
                final_distance += euclidian_distance(game_state1['building_features'][unit_id]['pos_x'],
                                                     game_state1['building_features'][unit_id]['pos_y'],
                                                     game_state2['building_features'][unit_id]['pos_x'],
                                                     game_state2['building_features'][unit_id]['pos_y'])

            old_health = game_state1['building_features'][unit_id]['hp'] + game_state1['building_features'][unit_id]['shields']
            new_health = game_state2['building_features'][unit_id]['hp'] + game_state2['building_features'][unit_id]['shields']
            final_distance += abs(old_health - new_health) ** .5

    for unit_id, features in game_state1['unit_features'].items():
        # this unit is new to the game
        if unit_id not in game_state2['unit_features']:
            final_distance += HISTORY_THRESHOLD / 4
        else:
            old_health = game_state1['unit_features'][unit_id]['hp'] + game_state1['unit_features'][unit_id]['shields']
            new_health = game_state2['unit_features'][unit_id]['hp'] + game_state2['unit_features'][unit_id]['shields']
            final_distance += abs(old_health - new_health) ** .5

            final_distance += euclidian_distance(game_state1['unit_features'][unit_id]['pos_x'],
                                                 game_state1['unit_features'][unit_id]['pos_y'],
                                                 game_state2['unit_features'][unit_id]['pos_x'],
                                                 game_state2['unit_features'][unit_id]['pos_y']) ** .5

    for unit_id, features in game_state2['unit_features'].items():
        # this unit has been destroyed
        if unit_id not in game_state1['unit_features']:
            final_distance += HISTORY_THRESHOLD / 4
        else:
            old_health = game_state1['unit_features'][unit_id]['hp'] + game_state1['unit_features'][unit_id]['shields']
            new_health = game_state2['unit_features'][unit_id]['hp'] + game_state2['unit_features'][unit_id]['shields']
            final_distance += abs(old_health - new_health) ** .5

            final_distance += euclidian_distance(game_state1['unit_features'][unit_id]['pos_x'],
                                                 game_state1['unit_features'][unit_id]['pos_y'],
                                                 game_state2['unit_features'][unit_id]['pos_x'],
                                                 game_state2['unit_features'][unit_id]['pos_y']) ** .5
    return final_distance


class GameState:
    """
    Organizes the information we receive throughout the game.
    Unit_Features: team, type, hp, (last known) position, shields (if applicable)
    Building_Features: team, type, hp, (last known) position, build time remaining, if it is completed, shields (if applicable)
    History: A list of previous game states, a new gamestate gets added to history if the distance between the last saved
        gamestate and the current gamestate is significantly different.
    """
    def __init__(self, player):
        self.features = {'unit_features': {}, 'building_features': {}}

        self.history = []
        self.player = player
        self.history_added = False

    def update_unit(self, unit):
        """
        Update the unit's information in gamestate
        :type unit: cybw.Unit
        """
        if not unit.exists():
            return

        if unit.getType().isMineralField() or unit.getType().getID() == 188:  # 188 is vespene geyser
            return

        if not unit.isVisible(self.player):
            current_game_time = broodwar.elapsedTime()
            if unit.getType().isBuilding() and 'time' in self.features.keys() and unit.getID() in self.features['building_features'].keys():
                old_time_remaining = unit.getRemainingBuildTime()
                actual_time_remaining = old_time_remaining - current_game_time - self.features['time']

                if actual_time_remaining > 0:
                    self.features['building_features'][unit.getID()]['build_time_remaining'] = actual_time_remaining
                else:
                    self.features['building_features'][unit.getID()]['build_time_remaining'] = 0
                    self.features['building_features'][unit.getID()]['is_built'] = True

        if unit.getType().isBuilding():
            self.features['building_features'][unit.getID()] = {'team': unit.getPlayer(),
                                                                'type': unit.getType(),
                                                                'hp': unit.getHitPoints(),
                                                                'pos_x': unit.getPosition().x,
                                                                'pos_y': unit.getPosition().y,
                                                                'build_time_remaining': unit.getRemainingBuildTime(),
                                                                'is_built': unit.isCompleted(),
                                                                'shields': 0}
            if unit.getType().getRace().getID() != cybw.Races.Zerg.getID():
                self.features['building_features'][unit.getID()]['shields'] = unit.getShields()

        else:
            self.features['unit_features'][unit.getID()] = {'team': unit.getPlayer(),
                                                            'type': unit.getType(),
                                                            'hp': unit.getHitPoints(),
                                                            'pos_x': unit.getPosition().x,
                                                            'pos_y': unit.getPosition().y,
                                                            'shields': 0}
            if unit.getType().getRace().getID() != cybw.Races.Zerg.getID():
                self.features['unit_features'][unit.getID()]['shields'] = unit.getShields()

    def remove_unit(self, unit):
        """
        Removes a unit from gamestate
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
        """
        For every unit cybw.broodwar gives us, update the information about it.
        """
        for unit in broodwar.getAllUnits():
            self.update_unit(unit)

        # used for building timings. If we last saw a building and it wasn't built, we can determine when it will be complete
        # with the time stamp on the game state in which it is saved.
        self.features['time'] = broodwar.elapsedTime()

        # Add current gamestate to history if either history is empty (game just began) or it is significantly different that
        # the previous game state
        if len(self.history) == 0:
            self.history.append(self.features)
        else:
            dist = distance(self.history[-1], self.features)
            if dist >= HISTORY_THRESHOLD:
                self.history.append(self.features)
                self.history_added = True
            else:
                self.history_added = False

    def basic_game_state(self, player):
        """
        returns only the amounts of every unit in features that belongs to player.
        Used for build order search.
        """
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
