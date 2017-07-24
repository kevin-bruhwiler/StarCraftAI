import cybw
from enum  import Enum

class WorkerJob (Enum):
    minerals = 0
    gas = 1
    build = 2
    combat = 3
    idle = 4
    repair = 5
    move = 6
    scout = 7
    default = 8

class WorkerMoveData(object):
    def __init__(self, minerals_needed=0, gas_needed=0, position=None):
        self.minerals_needed = minerals_needed
        self.gas_needed = gas_needed
        self.position = position

class WorkerData(object):
    def __init__(self):
        self.workers = []
        self.resource_depots = []
        self.worker_job = {}
        self.worker_mineral = {}
        self.worker_depot = {}
        self.worker_refinery = {}
        self.worker_repair = {}
        self.worker_move = {}
        self.worker_building_type = {}

        self.depot_worker_count = {}
        self.refinery_worker_count = {}

        self.workers_on_mineral_patch = {}
        self.worker_mineral_assignemnet = {}

        self.initialize()

    def initialize(self):
        for unit in cybw.Broodwar.getAllUnits():
            if unit.getType() == cybw.UnitTypes.Resource_Mineral_Field:
                self.workers_on_mineral_patch[unit] = 0

    def worker_destroyed(self, unit):
        if not unit:
            return

        self.clear_previous_job(unit)
        self.workers.remove(unit)

    def add_worker(self, unit, job, job_unit):
        if not unit or not job_unit:
            return

        if unit not in self.workers:
            self.workers.append(unit)
            self.set_worker_job(unit, job, job_unit)

    def add_depot(self, unit):
        if not unit:
            return

        if unit not in self.resource_depots:
            self.resource_depots.append(unit)
            self.depot_worker_count[unit] = 0

    def remove_depot(self, unit):
        if not unit:
            return

        self.resource_depots.remove(unit)
        self.depot_worker_count.pop(unit, None)

        for worker in self.workers:
            if self.worker_depot[worker] == unit:
                self.set_worker_job(worker, WorkerJob.idle, None)

    def add_to_mineral_patch(self, unit, num):
        if unit not in self.workers_on_mineral_patch.keys():
            self.workers_on_mineral_patch[unit] = num
        else:
            self.workers_on_mineral_patch[unit] = self.workers_on_mineral_patch[unit] + num

    def set_worker_job(self, unit, job, job_unit):
        if not unit:
            return

        self.clear_previous_job(unit)
        self.worker_job[unit] = job

        if job == WorkerJob.minerals:
            # increase the amount of workers assigned to this resource depot
            self.depot_worker_count[job_unit] += 1

            # set the mineral the worker is working on
            self.worker_depot[unit] = job_unit

            mineral_to_mine = self.get_mineral_to_mine(unit)
            self.worker_mineral_assignemnet[unit] = mineral_to_mine
            self.add_to_mineral_patch(mineral_to_mine, 1)

            # right click on the mineral to start mining
            unit.rightClick(mineral_to_mine)

        elif job == WorkerJob.gas:
            # increase the count of workers assigned to this refinery
            self.refinery_worker_count[job_unit] += 1

            # set the refinery the worker is working on
            self.worker_refinery[unit] = job_unit

            # right click on teh mineral to start harvesting
            unit.rightClick(job_unit)

        elif job == WorkerJob.repair:
            # only SCVs can repair
            if unit.getType() == cybw.UnitTypes.Terran_SCV:

                # set the building the unit is to reapir
                self.worker_repair[unit] = job_unit

                # start repairing
                if not unit.isRepairing():
                    unit.rightClick(job_unit)

        elif job == WorkerJob.scout:
            pass

        elif job == WorkerJob.build:
            self.worker_building_type[unit] = job_unit.type()

    def clear_previous_job(self, unit):
        if not unit:
            return
        previous_job = self.get_worker_job(unit)

        if previous_job == WorkerJob.minerals:
            self.depot_worker_count[self.worker_depot[unit]] -= 1
            self.worker_depot.pop(unit, None)

            # remove the worker from this unit's assigned mineral patch
            self.add_to_mineral_patch(self.worker_mineral_assignemnet[unit], -1)

            # remove from mineral workers dictionary
            self.worker_mineral_assignemnet.pop(unit, None)

        elif previous_job == WorkerJob.gas:
            self.refinery_worker_count[self.worker_refinery[unit]] -= 1
            self.worker_refinery.pop(unit, None)

        elif previous_job == WorkerJob.build:
            self.worker_building_type.pop(unit, None)

        elif previous_job == WorkerJob.repair:
            self.worker_repair.pop(unit, None)

        elif previous_job == WorkerJob.move:
            self.worker_move.pop(unit, None)

        self.worker_job.pop(unit, None)

    def get_number_of_workers(self):
        return len(self.workers)

    def get_number_of_mineral_workers(self):
        num = 0
        for worker in self.workers:
            if self.worker_job[worker] == WorkerJob.minerals:
                num += 1
        return num

    def get_number_of_gas_workers(self):
        num = 0
        for worker in self.workers:
            if self.worker_job[worker] == WorkerJob.gas:
                num += 1
        return num

    def get_number_of_idle_workers(self):
        num = 0
        for worker in self.workers:
            if self.worker_job[worker] == WorkerJob.idle:
                num += 1
        return num

    def get_worker_job(self, unit):
        if not unit:
            return WorkerJob.default

        if unit in self.worker_job.keys():
            return self.worker_job[unit]
        else:
            return WorkerJob.default

    def depot_is_full(self, depot):
        if not depot:
            return False

        num_assigned_workers = self.get_num_assigned_workers(depot)
        minerals_near_depot = self.get_mineral_near_depot(depot)

        if num_assigned_workers >= minerals_near_depot*3:
            return True
        else:
            return False

    @staticmethod
    def get_mineral_near_depot(depot):
        if not depot:
            return 0

        minerals_near_depot = 0

        for unit in cybw.Broodwar.getAllUnits():
            if unit.getType() == cybw.UnitTypes.Resource_Mineral_Field and unit.getDistance(depot) < 200:
                minerals_near_depot += 1

        return minerals_near_depot

    def get_worker_resource(self, unit):
        if not unit:
            return None

        if self.worker_job[unit] == WorkerJob.minerals:
            return self.worker_mineral[unit]

        if self.worker_job[unit] == WorkerJob.gas:
            return self.worker_refinery[unit]

        return None

    def get_mineral_to_mine(self, unit):
        if not unit:
            return None

        depot = self.get_worker_depot(unit)
        mineral = None
        closest_dist = 10000

        if depot:
            for unit in cybw.Broodwar.getAllUnits():
                if unit.getType() == cybw.UnitTypes.Resource_Mineral_Field and unit.getResources() > 0:
                    tmp_dist = unit.getDistance(depot)
                    if not mineral and tmp_dist < closest_dist:
                        mineral = unit
                        closest_dist = tmp_dist

        return mineral

    def get_worker_repair_unit(self, unit):
        if not unit:
            return None

        if unit in self.worker_repair.keys():
            return self.worker_repair[unit]

        return None

    def get_worker_depot(self, unit):
        if not unit:
            return None

        if unit in self.worker_depot.keys():
            return self.worker_depot[unit]

        return None

    def get_worker_building_type(self, unit):
        if not unit:
            return None

        if unit in self.worker_building_type.keys():
            return self.worker_building_type[unit]

        return None

    def get_worker_move_data(self, unit):
        if unit in self.worker_move.keys():
            return self.worker_move[unit]

        return None

    def get_num_assigned_workers(self, unit):
        if not unit:
            return 0

        if unit.getType().isResourceDepot():
            if unit in self.depot_worker_count.keys():
                return self.depot_worker_count[unit]
        elif unit.getType().isRefinery():
            if unit in self.refinery_worker_count.keys():
                return self.refinery_worker_count[unit]
            else:
                self.refinery_worker_count[unit] = 0
        return 0

