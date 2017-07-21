import cybw
import WorkerManager


class AutoObserver(object):
    def __init__(self):
        self.unit_follow_frames = 0
        self.camera_last_move = 0
        self.observer_following_unit = None
        self.worker_manager = None

        for obj in gc.get_objects():
            if isinstance(obj, WorkerManager.WorkerManager):
                self.worker_manager = obj

    def observe(self):
        if cybw.Broodwar.isReplay():
            return

        pick_unit_to_follow = None

        if self.observer_following_unit is not None:
            if not self.observer_following_unit.exists() or cybw.Broodwar.getFrameCount() - self.camera_last_move > self.unit_follow_frames:
                pick_unit_to_follow = True
        else:
            pick_unit_to_follow = True

        if pick_unit_to_follow:
            for unit in cybw.Broodwar.getAllUnits():
                if unit.isUnderAttack() or unit.isAttacking():
                    self.camera_last_move = cybw.Broodwar. getFrameCount()
                    self.unit_follow_frames = 6
                    self.observer_following_unit = unit
                    pick_unit_to_follow = False
                    break

        if pick_unit_to_follow:
            for unit in cybw.Broodwar.getAllUnits():
                if unit.isBeingConstructed and unit.getRemainingBuildTime() < 12:
                    self.camera_last_move = cybw.Broodwar.getFrameCount()
                    self.unit_follow_frames = 6
                    self.observer_following_unit = unit
                    pick_unit_to_follow = False
                    break

        if pick_unit_to_follow:
            for unit in cybw.Broodwar.getAllUnits():
                if self.is_worker_scout(unit):
                    self.camera_last_move = cybw.Broodwar.getFrameCount()
                    self.unit_follow_frames = 6
                    self.observer_following_unit = unit
                    break

        if self.observer_following_unit is not None:
            if self.observer_following_unit.exists():
                cybw.Broodwar.setScreenPosition(self.observer_following_unit.getPosition() - cybw.Position(320, 180))
