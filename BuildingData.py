import cybw
from enum  import Enum

class BuildingStatus(Enum):
    unassigned = 0
    assigned = 1
    under_construction = 2
    size = 3

class Building(object):
    def __int__(self, unit_type=None, desired_position=None):
        self.type = unit_type
        self.position = cybw.Position(0,0)
        self.final_position = cybw.Position(0,0)
        self.last_order_frame = 0
        self.status = BuildingStatus.unassigned
        self.build_command_given = False
        self.under_construction = False
        self.is_gas_steal = False

class BuildingData(object):
    def __init__(self):
        self.buildings = []

    def is_being_built(self, type):
        for building in self.buildings:
            if building.type() == type:
                return True
        return False

    def remove_buildings(self, buildings):
        for building in buildings:
            self.remove_building(building)

    def remove_building(self, building):
        self.buildings.remove(building)
