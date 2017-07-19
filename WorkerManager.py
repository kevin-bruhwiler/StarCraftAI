import cybw


class WorkerManager:
    def __init__(self):
        self.workers = []

    def add_worker(self, unit):
        """
        add a worker to self.workers
        :type unit: cybw.Unit
        """
        if unit.getType().isWorker() and unit not in self.workers:
            self.workers.append(unit)

    def work(self):
        """
        the command that gets called every frame
        Makes every worker gather resources
        """
        for worker in self.workers:
            if worker.isIdle():
                if worker.isCarryingGas() or worker.isCarryingMinerals():
                    worker.returnCargo()
                else:
                    minerals = cybw.Broodwar.getMinerals()
                    closest_mineral = None
                    for mineral in minerals:
                        if closest_mineral is None or worker.getDistance(mineral) < worker.getDistance(closest_mineral):
                            closest_mineral = mineral
                    if closest_mineral:
                        worker.gather(closest_mineral)

    def get_builder(self, building):
        """
        Routine for BuildingManager, gets the closest worker to the building
        :type building: BuildingData.Building
        """
        pass

    def finished_with_worker(self, worker):
        return True