import cybw


class ScoutManager:
    def __init__(self):
        self.scouts = []
        self.scouting_path = []

        # self.start_locations.remove(cybw.Player.getStartLocation())
        self.scouting_complete = False
        self.desired_number_of_scouts = 1

    def initialize(self):
        start_locations = cybw.Broodwar.getStartLocations()
        start_locations.remove(cybw.Broodwar.self().getStartLocation())
        self.make_path(start_locations)

    def make_path(self, start_locations):
        scout = self.scouts[0]
        while len(start_locations) > 0:
            smallest_distance = 99999
            closest_location = None
            for location in start_locations:
                distance_to_location = scout.getPosition().getDistance(cybw.Position(location))
                if distance_to_location < smallest_distance:
                    closest_location = location
                    smallest_distance = distance_to_location
            if closest_location is not None:
                self.scouting_path.append(closest_location)
                start_locations.remove(closest_location)

        print(len(self.scouting_path))

    def add_scout(self, scout):
        if scout.getType().isWorker() and scout not in self.scouts:
            self.scouts.append(scout)

    def scout(self):
        # since we only have one scout (for now, make it cleaner to access)
        scout = self.scouts[0]

        if scout.getPosition().getDistance(cybw.Position(self.scouting_path[0])) < scout.getType().sightRange():
            print(len(self.scouting_path))
            self.scouting_path.pop(0)
            print(len(self.scouting_path))

        if len(self.scouting_path) > 0:
            scout.move(cybw.Position(self.scouting_path[0]))
        # return home
        else:
            print("got here")
            if scout.getPosition().getDistance(cybw.Position(cybw.Broodwar.self().getStartLocation())) > 3:
                scout.move(cybw.Position(cybw.Broodwar.self().getStartLocation()))
            else:
                self.scouting_complete = True
