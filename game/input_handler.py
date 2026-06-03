from panda3d.core import (CollisionTraverser, CollisionNode, CollisionRay,
                          CollisionHandlerQueue, BitMask32)

class InputHandler:
    def __init__(self, base):
        self.base = base
        self._setup_picker()
        base.accept("mouse1", self.on_click)
        base.accept("escape", base.userExit)

    def _setup_picker(self):
        self.traverser = CollisionTraverser("picker")
        self.queue     = CollisionHandlerQueue()
        pick_node      = CollisionNode("mouse_ray")
        pick_node.setFromCollideMask(BitMask32.bit(1))
        pick_node.setIntoCollideMask(BitMask32.allOff())
        self.ray       = CollisionRay()
        pick_node.addSolid(self.ray)
        self.picker_np = self.base.camera.attachNewNode(pick_node)
        self.traverser.addCollider(self.picker_np, self.queue)
        self.refresh_colliders()

    def refresh_colliders(self):
        for g in self.base.level_manager.gears:
            g.node.setCollideMask(BitMask32.bit(1))

    def on_click(self):
        if not self.base.mouseWatcherNode.hasMouse():
            return
        mpos = self.base.mouseWatcherNode.getMouse()
        self.ray.setFromLens(self.base.camNode, mpos.x, mpos.y)
        self.traverser.traverse(self.base.render)
        if self.queue.getNumEntries() == 0:
            return
        self.queue.sortEntries()
        hit_np = self.queue.getEntry(0).getIntoNodePath()
        col = hit_np.getNetTag("gear_col")
        row = hit_np.getNetTag("gear_row")
        if col and row:
            rotated = self.base.level_manager.rotate_gear_at(int(col), int(row))
            if rotated:
                self.refresh_colliders()
                if self.base.level_manager.check_win():
                    self.base.ui.show_win()
