import cybw

class BuildingPlacer(object):
    def __init__(self):
        self.reserve_map = []

    def can_build_here(self, position, building):
        """
        A final check to see if a building can be built in a certain location
        :type position: cybw.TilePosition.Position
        :type building: BuildingData.Building
        """
        if not cybw.Broodwar.canBuildHere(position, building.type(), building.builder_unit):
            return False

    def tile_blocks_add_on(self, position):
        """
        check to see if the building at position can have an add on
        :type position: cybw.TilePosition.Position
        """
        pass

    def can_build_here_with_space(self, position, building, build_dist, horizontal_only):
        """
        Returns true if we can build this type of unit here with the specified amount of space
        :type position: cybw.TilePosition.Position
        :type building: BuildingData.Building
        :type build_dist: int
        :type horizontal_only: bool
        """
        pass

    def get_build_location(self, building, padding):
        """
        find the building location for building + padding
        :type building: BuildingData.Building
        :type padding: int
        """
        pass

    def get_build_location_near(self, building, horizontal_only=False):
        """
        find the best build location near the building.desired_position
        :type building: BuildingData.Building
        :type horizontal_only: bool
        """
        pass

    def tile_over_laps_base_locations(self, tile, unit_type):
        """
        :param tile: cybw.TilePosition.Position
        :param unit_type: cybw.UnitType
        """
        pass

    def buildable(self, building, x, y):
        """
        reserve the tiles where building will be built
        :type building: BuildingData.Building
        :type x: int
        :type y: int
        """
        pass

    def reserve_tiles(self, building, width, height):
        """
        reserve the tiles where building will be built
        :type building: BuildingData.Building
        :type width: int
        :type height: int
        """
        pass

    def free_tiles(self, position, width, height):
        """
        free the tiles at (position.x, position.y) => (position.x + width, position.y + height)
        :param position: cybw.TilePosition.Position
        :type width: int
        :type height: int
        """
        pass

    def get_refinery_position(self):
        """
        Gets the nearest refinery position
        """
        pass

    def is_reserved(self, x, y):
        """
        check to see if tile (x,y) is reserved
        :type x: int
        :type y: int
        """
        pass