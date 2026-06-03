from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode

class GameUI:
    def __init__(self, base):
        self.base    = base
        self.win_msg = None
        self.btn     = None
        self.title   = OnscreenText(
            text="CogShift", pos=(-1.2, 0.90), scale=0.07,
            fg=(1,1,1,1), align=TextNode.ALeft)
        self.level_label = OnscreenText(
            text="", pos=(0, 0.90), scale=0.055, fg=(0.8,0.8,0.8,1))
        self.hint = OnscreenText(
            text="Click a gear to toggle its direction",
            pos=(0, -0.92), scale=0.05, fg=(0.7,0.7,0.7,1))

    def update_level_label(self, num, total, name):
        self.level_label.setText(f"Level {num}/{total}  —  {name}")

    def show_win(self):
        self.win_msg = OnscreenText(
            text="\u2713 Power Delivered!", pos=(0, 0.15),
            scale=0.12, fg=(0.3,1.0,0.5,1))
        self.btn = DirectButton(
            text="Next Level", scale=0.08, pos=(0,0,-0.05),
            command=self._next_level)

    def _next_level(self):
        for w in (self.win_msg, self.btn):
            if w: w.destroy()
        self.win_msg = self.btn = None
        if not self.base.level_manager.next_level():
            OnscreenText(text="\U0001f389 You completed all levels!",
                         pos=(0,0), scale=0.10, fg=(1,0.85,0.2,1))
        self.base.input_handler.refresh_colliders()
