import cybw
import BuildingData
import gc
import WorkerManager

class BuildingManager(object):
    def __init__(self):
        self.reservedGas = 0
        self.reservedMinerals = 0
        self.buildings = []

    def update(self):
        self.validate_workers_and_buildings()
        self.assign_workers_to_unassigned_buildings()
        self.construct_assigned_buildings()
        self.check_for_started_construction()
        self.check_for_dead_builder()
        self.check_for_completed_buildings()

    def is_building_position_explored(self):
        pass

    def remove_buildings(self, building):
        pass

    def validate_workers_and_buildings(self):
        buildings_to_remove = []
        for building in self.buildings:
            if building.status != BuildingData.BuildingStatus.under_construction:
                continue

            if building.building_unit is None or not building.building_unit.getType().isBuilding() or building.building_unit.getHitPoints() <= 0:
                buildings_to_remove.append(building)

        self.remove_buildings(buildings_to_remove)

    def assign_workers_to_unassigned_buildings(self):
        worker_manager = None
        for obj in gc.get_objects():
            if isinstance(obj, WorkerManager.WorkerManager):
                worker_manager = obj

        for building in self.buildings:
            if building.status == BuildingData.BuildingStatus.unassigned:
                continue

            worker_to_assign = worker_manager.getBuilder(building)


    def construct_assigned_buildings(self):
        pass

    def check_for_started_construction(self):
        pass

    def check_for_dead_builder(self):
        pass

    def check_for_completed_buildings(self):
        pass

    def get_building_worker_code(self):
        pass

    def is_being_built(self, type):
        for building in self.buildings:
            if building.type() == type:
                return True
        return False
