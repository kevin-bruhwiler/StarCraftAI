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
            if unit.getType().isWorker():
                self.worker_manager.add_worker(unit)

    def add_unit(self, unit):
        if unit.getType().isWorker():
            self.worker_manager.add_worker(unit)

    def manage(self):
        if len(self.worker_manager.workers) == 0:
            print("got here")
            self.add_units()
        self.worker_manager.work()
