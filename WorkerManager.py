import cybw


class WorkerManager:
    def __init__(self):
        self.workers = []

    def add_worker(self, unit):
        if unit.getType().isWorker() and unit not in self.workers:
            self.workers.append(unit)

    def work(self):
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

    def getBuilder(self, building):
        pass