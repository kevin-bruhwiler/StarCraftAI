import cybw
import WorkerData
import InformationManager
import gc

class WorkerManager:
    def __init__(self):
        self.worker_data = WorkerData.WorkerData()
        self.information_manager = None

        for obj in gc.get_objects():
            if isinstance(obj, InformationManager.InformationManager):
                self.information_manager = obj

    def update(self):
        self.update_worker_status()
        self.handle_gas_workers()
        self.handle_idle_workers()
        self.handle_move_workers()
        self.handle_combat_workers()

        self.draw_resource_debug_info()
        self.draw_worker_information(450, 20)


    def update_worker_status(self):
        for worker in self.worker_data.workers:
            if not worker.isCompleted():
                continue
            # if the worker is idle
            if worker.isIdle() and \
            self.worker_data.get_worker_job(worker) != WorkerData.WorkerJob.build and \
            self.worker_data.get_worker_job(worker) != WorkerData.WorkerJob.move and \
            self.worker_data.get_worker_job(worker) != WorkerData.WorkerJob.scout:
                self.worker_data.set_worker_job(worker, WorkerData.WorkerJob.idle, None)

            if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.gas:
                refinery = self.worker_data.get_worker_resource(worker)

                # if the refinery does not exist anymore
                if not refinery or not refinery.exists() or refinery.getHitPoints() <= 0:
                    self.set_mineral_worker(worker)

    def set_repair_worker(self, worker, unit_to_repair):
        self.worker_data.set_worker_job(worker, WorkerData.WorkerJob.repair, unit_to_repair)

    def stop_repairing(self, worker):
        self.worker_data.set_worker_job(worker, WorkerData.WorkerJob.idle, None)

    def handle_gas_workers(self):
        # for each unit we have
        for unit in cybw.Broodwar.self().getUnits():
            # check if refinery
            if unit.getType().isRefinery() and unit.isComplete() and not self.is_gas_steal_refinery(unit):
                num_assigned = self.worker_data.get_num_assigned_workers(unit)

                while num_assigned < 3:
                    gas_worker = self.get_gas_worker(unit)
                    if gas_worker:
                        self.worker_data.set_worker_job(gas_worker, WorkerData.WorkerJob.gas, unit)

    def is_gas_steal_refinery(self, unit):
        enemy_base_location = self.information_manager.get_main_base_location(cybw.Broodwar.enemy())
        if not enemy_base_location:
            return False
        if enemy_base_location.getGeysers().empty():
            return False
        for geyser in enemy_base_location.getGeysers():
            if unit.getTilePosition() == geyser.getTilePosition():
                return True
        return False

    def handle_idle_workers(self):
        for worker in self.worker_data.workers:
            if worker is not None:
                if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.idle:
                    self.set_mineral_worker(worker)

    def handle_repair_workers(self):
        if cybw.Broodwar.self().race != cybw.Races.Terran:
            return None

        for unit in cybw.Broodwar.self().getUnits():
            if unit.getType().isBuilding and unit.getHitPoints() < unit.getType().maxHitPoints():
                repair_worker = self.get_closest_mineral_worker(unit)
                self.set_repair_worker(repair_worker, unit)
                break

    def handle_combat_workers(self):
        for worker in self.worker_data.workers:
            if worker is not None:
                if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.combat:
                    target = sorted(cybw.Broodwar.enemy().getUnits(), key=lambda unit: unit.getDistnace(worker))
                    if target is not None:
                        worker.right_click(target[0])

    def finished_with_combat_workers(self):
        for worker in self.worker_data.workers:
            if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.combat:
                self.set_mineral_worker(worker)

    def get_closest_mineral_worker(self, unit):
        closest_dist = 10000
        closest_mineral_worker = None
        for worker in self.worker_data.workers:
            if not worker:
                continue
            if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.minerals:
                tmp_dist = worker.get_distance(unit)

                if not closest_mineral_worker or tmp_dist < closest_dist:
                    closest_mineral_worker = worker
                    closest_dist = tmp_dist
        return closest_mineral_worker

    def get_worker_scout(self):
        for worker in self.worker_data.workers:
            if worker is None:
                continue
            if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.scout:
                return worker
        return None

    def handle_move_workers(self):
        for worker in self.worker_data.workers:
            if worker is None:
                continue
            if self.worker_data.get_worker_job(worker) == WorkerData.WorkerJob.move:
                move_data = self.worker_data.get_worker_move_data(worker)
                worker.right_click(move_data.posiiton)

    def set_mineral_worker(self, unit):
        depot = self.get_closest_depot(unit)
        if depot:
            self.worker_data.set_worker_job(unit, WorkerData.WorkerJob.minerals, depot)

    def get_closest_depot(self, worker):
        closest_depot = None
        closest_distance = 10000
        for unit in cybw.Broodwar.self().getUnits():
            if unit.getType().isResourceDepot and unit.isComplete():
                if self.worker_data.depot_is_full(unit):
                    tmp_distance = unit.getDistance(worker)
                    if not closest_depot or tmp_distance < closest_distance:
                        closest_depot = unit
                        closest_distance = tmp_distance
        return closest_depot

    def finished_with_worker(self, unit):
        if self.worker_data.get_worker_job(unit) == WorkerData.WorkerJob.scout:
            self.worker_data.set_worker_job(unit, WorkerData.WorkerJob.idle, None)

    def get_gas_worker(self, refinery):
        pass
            