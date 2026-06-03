import json, os
from game.gear import Gear, GEAR_SOURCE, GEAR_TARGET, GEAR_LOCKED, GEAR_NORMAL, CW
from game.rotation_bridge import propagate_directions as cpp_propagate

LEVELS_PATH = os.path.join(os.path.dirname(__file__), "..", "levels", "levels.json")

def _load_levels():
    with open(LEVELS_PATH) as f:
        raw = json.load(f)
    type_map = {"source": GEAR_SOURCE, "target": GEAR_TARGET,
                "locked": GEAR_LOCKED,  "normal": GEAR_NORMAL}
    levels = []
    for entry in raw:
        gears = [(g["col"], g["row"], type_map[g["type"]], g["locked"])
                 for g in entry["gears"]]
        levels.append({"name": entry["name"], "gears": gears, "edges": entry["edges"]})
    return levels

class LevelManager:
    def __init__(self, base):
        self.base        = base
        self.current_idx = 0
        self.gears       = []
        self.edges       = []
        self._levels     = _load_levels()

    def level_name(self):  return self._levels[self.current_idx]["name"]
    def level_count(self): return len(self._levels)

    def load_level(self, idx):
        self.clear()
        self.current_idx = idx
        data = self._levels[idx]
        for col, row, gtype, locked in data["gears"]:
            self.gears.append(Gear(self.base, (col, row), gtype, locked))
        for a_idx, b_idx in data["edges"]:
            self.edges.append((self.gears[a_idx], self.gears[b_idx]))
        self.propagate_power()
        self.base.ui.update_level_label(idx + 1, self.level_count(), self.level_name())

    def clear(self):
        for g in self.gears: g.cleanup()
        self.gears.clear()
        self.edges.clear()

    def next_level(self):
        nxt = self.current_idx + 1
        if nxt < self.level_count():
            self.load_level(nxt)
            return True
        return False

    def propagate_power(self):
        for g in self.gears:
            if g.gear_type != GEAR_SOURCE:
                g.set_powered(False, None)
        if not self.gears:
            return
        flat_edges = []
        for a, b in self.edges:
            flat_edges += [self.gears.index(a), self.gears.index(b)]
        src_idx = next(i for i, g in enumerate(self.gears) if g.gear_type == GEAR_SOURCE)
        dirs = cpp_propagate(len(self.gears), flat_edges, src_idx, CW)
        for i, g in enumerate(self.gears):
            if i != src_idx and dirs[i] != 0:
                g.set_powered(True, dirs[i])

    def check_win(self):
        return all(g.powered for g in self.gears if g.gear_type == GEAR_TARGET)

    def rotate_gear_at(self, col, row):
        for g in self.gears:
            if g.grid_pos == (col, row):
                if g.toggle_direction():
                    self.propagate_power()
                    return True
        return False
