import cybw


class WorkerManager:
    def __init__(self):
        self.workers = []

    def update(self):
        self.update_worker_status()
        self.handle_gas_workers()
        self.handle_idle_workers()
        self.handle_move_workers()
        self.handle_combat_workers()

        self.draw_resource_debug_info()
        self.draw_worker_information(450, 20)

        self.worker_data.draw_depot_debug_info()

    def finished_with_worker(self, worker):
        pass