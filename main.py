from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LVecBase4f, Point3
from game.level_manager import LevelManager
from game.input_handler import InputHandler
from game.ui import GameUI

class CogShift(ShowBase):
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(0.08, 0.08, 0.12, 1)
        self.setup_lighting()
        self.setup_camera()
        self.level_manager = LevelManager(self)
        self.ui = GameUI(self)
        self.input_handler = InputHandler(self)
        self.level_manager.load_level(0)

    def setup_lighting(self):
        ambient = AmbientLight("ambient")
        ambient.setColor(LVecBase4f(0.4, 0.4, 0.4, 1))
        self.render.setLight(self.render.attachNewNode(ambient))
        sun = DirectionalLight("sun")
        sun.setColor(LVecBase4f(0.9, 0.85, 0.7, 1))
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(45, -45, 0)
        self.render.setLight(sun_np)

    def setup_camera(self):
        self.disableMouse()
        self.camera.setPos(0, -20, 14)
        self.camera.lookAt(Point3(0, 0, 0))

app = CogShift()
app.run()
