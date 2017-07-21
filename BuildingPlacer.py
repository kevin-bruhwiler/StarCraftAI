import cybw
import MapTools

import gc

class BuildingPlacer(object):
    def __init__(self):
        self.reserve_map = {}
        self.map_tools = None

        for obj in gc.get_objects():
            if isinstance(obj, MapTools.MapTools):
                self.map_tools = obj
    def can_build_here(self, position, building):
        """
        A final check to see if a building can be built in a certain location
        :type position: cybw.TilePosition.Position
        :type building: BuildingData.Building
        """
        if not cybw.Broodwar.canBuildHere(position, building.type(), building.builder_unit):
            return False

        for pos_x in range(position.x, position.x + building.type().tileWidth()):
            for pos_y in range(position.y, position.y + building.type().tileHeight()):
                if pos_x in self.reserve_map:
                    if pos_y in self.reserve_map[pos_x]:
                        if self.reserve_map[pos_x][pos_y]:
                            return False

        if self.tile_over_laps_base_locations(position, building.type):
            return False

        return True

    @staticmethod
    def tile_blocks_add_on(position):
        """
        check to see if the building at position can have an add on
        :type position: cybw.TilePosition.Position
        """
        for i in range(2):
            for unit in cybw.Broodwar.getUnitsOnTile(position.x - i, position.y):
                if unit.canBuildAddon():
                    return True
        return False

    def can_build_here_with_space(self, position, building, build_dist, horizontal_only):
        """
        Returns true if we can build this type of unit here with the specified amount of space
        :type position: cybw.TilePosition.Position
        :type building: BuildingData.Building
        :type build_dist: int
        :type horizontal_only: bool
        """
        if not self.can_build_here(position, building):
            return False

        width = building.type().tileWidth()
        height = building.type().tileHeight()

        if building.type.canBuildAddon():
            width += 2

        start_x = position.x - build_dist
        start_y = position.y - build_dist
        end_x = position.x + width + build_dist
        end_y = position.y + height + build_dist

        if building.type().isAddon():
            main_building = building.type().whatBuilds()[0]


            start_x = position.x - main_building.tileWidth().x - build_dist
            start_y = position.y + 2 - main_building.tileHeight() - build_dist
            end_x = position.x + width + build_dist
            end_y = position.y + height + build_dist

        if horizontal_only:
            start_y += build_dist
            end_y -= build_dist

        # check to make sure that this rectangle fits inside the map
        if start_x < 0 or start_y < 0 or end_x > cybw.Broodwar.mapWidth() or end_x < position.x + width or end_y > cybw.Broodwar.mapHeight():
            return False

        for pos_x in range(start_x, end_x):
            for pos_y in range(start_y, end_y):
                if not building.type().isRefinery():
                    if not self.buildable(building, pos_x, pos_y):
                        return False
                    if pos_x in self.reserve_map:
                        if pos_y in self.reserve_map[pos_x]:
                            if self.reserve_map[pos_x][pos_y]:
                                return False

        return True

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