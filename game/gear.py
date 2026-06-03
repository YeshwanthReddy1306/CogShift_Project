from panda3d.core import LVecBase4f
from direct.interval.IntervalGlobal import LerpHprInterval, Sequence

GEAR_NORMAL = "normal"
GEAR_LOCKED = "locked"
GEAR_SOURCE = "source"
GEAR_TARGET = "target"

CW  =  1
CCW = -1

COLORS = {
    GEAR_NORMAL: LVecBase4f(0.55, 0.60, 0.65, 1),
    GEAR_LOCKED: LVecBase4f(0.70, 0.30, 0.25, 1),
    GEAR_SOURCE: LVecBase4f(0.25, 0.75, 0.40, 1),
    GEAR_TARGET: LVecBase4f(0.95, 0.75, 0.10, 1),
}

class Gear:
    def __init__(self, base, grid_pos, gear_type=GEAR_NORMAL, locked=False):
        self.base      = base
        self.grid_pos  = grid_pos
        self.gear_type = gear_type
        self.locked    = locked or gear_type in (GEAR_LOCKED, GEAR_SOURCE)
        self.powered   = gear_type == GEAR_SOURCE
        self.direction = CW if gear_type == GEAR_SOURCE else None
        self._spin_seq = None

        try:
            self.node = base.loader.loadModel("models/gear")
            self.node.setScale(0.45)
        except Exception:
            self.node = base.loader.loadModel("models/misc/sphere")
            self.node.setScale(0.45)

        self.node.setColor(COLORS[gear_type])
        wx, wy = self._to_world(grid_pos)
        self.node.setPos(wx, 0, wy)
        self.node.reparentTo(base.render)
        self.node.setTag("gear_col", str(grid_pos[0]))
        self.node.setTag("gear_row", str(grid_pos[1]))

        if self.powered:
            self._start_spin()

    @staticmethod
    def _to_world(grid_pos, spacing=2.0):
        col, row = grid_pos
        return col * spacing, row * spacing

    def set_powered(self, powered, direction):
        self.powered   = powered
        self.direction = direction
        base_col = COLORS[self.gear_type]
        if powered:
            self.node.setColor(
                min(base_col[0] + 0.20, 1.0),
                min(base_col[1] + 0.20, 1.0),
                min(base_col[2] + 0.20, 1.0), 1)
            self._start_spin()
        else:
            self.node.setColor(base_col)
            self._stop_spin()

    def _start_spin(self):
        if self._spin_seq:
            self._spin_seq.finish()
        end_h = 360 if self.direction == CW else -360
        spin  = LerpHprInterval(self.node, 2.0, (end_h, 0, 0), (0, 0, 0))
        self._spin_seq = Sequence(spin)
        self._spin_seq.loop()

    def _stop_spin(self):
        if self._spin_seq:
            self._spin_seq.finish()
            self._spin_seq = None

    def toggle_direction(self):
        if self.locked:
            return False
        self.direction = CCW if self.direction == CW else CW
        return True

    def cleanup(self):
        self._stop_spin()
        self.node.removeNode()
