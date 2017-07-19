import cybw
import BuildingData
import gc
import WorkerManager
import BuildingPlacer
import MapTools


class BuildingManager(object):
    def __init__(self):
        self.reservedGas = 0
        self.reservedMinerals = 0
        self.buildings = []

    def update(self):
        """
        Update all aspects of the BuildingManager
        """
        self.validate_workers_and_buildings()
        self.assign_workers_to_unassigned_buildings()
        self.construct_assigned_buildings()
        self.check_for_started_construction()
        self.check_for_dead_builder()
        self.check_for_completed_buildings()

    def is_building_position_explored(self, building):
        """
        Check to seeif where we want to build the building has been explored
        """
        tile = building.final_position

        for x in  range(building.type.tileWidth()):
           for y in range(building.type.tileHeight()):
               if not cybw.Broodwar.isExplored(tile.x + x, tile.y + y):
                   return False
        return True


    def remove_buildings(self, buildings):
        """
        Update all aspects of the BuildingManager
        :type buildings: list(BuildingData.Building)
        """
        for building in buildings:
            self.buildings.remove(building)

    def validate_workers_and_buildings(self):
        """
        Check to see if assigned workers have died en route or while constructing
        """
        buildings_to_remove = []
        for building in self.buildings:
            if building.status != BuildingData.BuildingStatus.under_construction:
                continue

            if building.building_unit is None or not building.building_unit.getType().isBuilding() or building.building_unit.getHitPoints() <= 0:
                buildings_to_remove.append(building)

        self.remove_buildings(buildings_to_remove)

    def assign_workers_to_unassigned_buildings(self):
        """
        Assign workers to the unassigned buildings and label them 'planned'
        """
        worker_manager = None
        building_placer = None
        for obj in gc.get_objects():
            if isinstance(obj, WorkerManager.WorkerManager):
                worker_manager = obj
            if isinstance(obj, BuildingPlacer.BuildingPlacer):
                building_placer = obj

        for building in self.buildings:
            if building.status == BuildingData.BuildingStatus.unassigned:
                continue

            worker_to_assign = worker_manager.get_builder(building)

            if worker_to_assign is not None:
                building.building_unit = worker_to_assign

                test_location = self.building_location(building)

                if not test_location.isValid():
                    continue

                building.final_position = test_location

                building_placer.reserve_tiles(building.final_position, b.type.tileWidth(), b.type.tileHeight())

    @staticmethod
    def building_location(building):
        """
        Update all aspects of the BuildingManager
        :type building: BuildingData.Building
        """
        building_placer = None
        map_tools = None
        for obj in gc.get_objects():
            if isinstance(obj, BuildingPlacer.BuildingPlacer):
                building_placer = obj
                if isinstance(obj, MapTools.MapTools):
                    map_tools = obj

        if building.type().isRefinery():
            return building_placer.get_refinery_position()

        if building.type().isResourceDepot():
            return map_tools.get_next_expansion()

        return building_placer.get_build_location_near(building, False)


    def construct_assigned_buildings(self):
        """
        For each planned building, if the worker isn't constructing, send the command
        """
        worker_manager = None
        building_placer = None
        for obj in gc.get_objects():
            if isinstance(obj, WorkerManager.WorkerManager):
                worker_manager = obj
            if isinstance(obj, BuildingPlacer.BuildingPlacer):
                building_placer = obj

        for building in self.buildings:
            if building.status != BuildingData.BuildingStatus.assigned:
                continue

            # check to see if the worker is not currently constructing
            if building.building_unit.isConstructing():
                if not self.is_building_position_explored(building):
                    pass

                # If this is not the first time this worker has been sent to build this, there must be something in the way of building
                elif building.build_command_given:

                    # tell worker manager the unit we had is not needed now, since we might not be able to get a location location soon enough
                    worker_manager.finished_with_worker(building.building_unit)

                    # free the previous location in reserved
                    building_placer.free_tiles(building.final_position, building.type().tileWidth(), building.type().tileHeight())

                    # reset the building's variables
                    building.building_unit = None
                    building.build_command_given = False
                    building.status = BuildingData.BuildingStatus.unassigned

                else:
                    # send the command to build
                    building.building_unit.build(building.type, building.final_position)

                    # set the flag to true
                    building.build_command_given = True


    def check_for_started_construction(self):
        """
        Check to see if any buildings have started construction and update data structures accordingly
        """
        pass

    def check_for_dead_builder(self):
        """
        If we are Terran (we are) and building is under construction without a worker, assign a new one
        """
        pass

    def check_for_completed_buildings(self):
        """
        Check to see if any buildings have completed and update data structures accordingly
        """
        pass

    def get_building_worker_code(self):
        pass

    def is_being_built(self, type):
        """
        Check to see if type is being built
        :type type: cybw.Unit
        """
        for building in self.buildings:
            if building.type() == type:
                return True
        return False
