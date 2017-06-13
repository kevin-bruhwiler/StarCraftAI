import cybw
import ScoutManager
import WorkerManager


class UnitManager:
    def __init__(self):
        self.scout_manager = ScoutManager.ScoutManager()
        self.worker_manager = WorkerManager.WorkerManager()

    def add_units(self):
        units = cybw.Broodwar.self().getUnits()
        for unit in units:
            self.add_unit(unit)

    def add_unit(self, unit):
        if unit.getType().isWorker():
            if len(self.scout_manager.scouts) < self.scout_manager.desired_number_of_scouts:
                self.scout_manager.add_scout(unit)
            else:
                self.worker_manager.add_worker(unit)

    def initialize(self):
        self.add_units()
        self.scout_manager.initialize()

    def manage(self):
        if not self.scout_manager.scouting_complete:
            self.scout_manager.scout()

        elif len(self.scout_manager.scouts) > 0:
            for scout in self.scout_manager.scouts:
                self.worker_manager.workers.append(scout)
                self.scout_manager.scouts.remove(scout)

        self.worker_manager.work()
