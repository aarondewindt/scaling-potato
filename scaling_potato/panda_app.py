from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, VBase4
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from direct.task import Task

from math import pi, sin, cos


class PandaApp(ShowBase):
    def __init__(self, pilons=None):
        ShowBase.__init__(self)

        self.pilons = pilons or []

        # Disable the camera trackball controls.
        # self.disableMouse()

        self.load_scene()
        self.load_pilons()

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)
        # self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        # self.camera.setHpr(angleDegrees, 0, 0)
        print self.camera.getPos()
        return Task.cont

    def load_scene(self):
        self.scene_model = self.loader.loadModel("models/scene.egg")
        self.scene_model.reparentTo(self.render)

        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.1, 0.1, 0.1, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

        self.dlight = DirectionalLight('dlight')
        self.dlight.setColor(VBase4(0.8, 0.8, 0.8, 1))
        self.dlnp = self.render.attachNewNode(self.dlight)
        self.dlnp.setHpr(0, -60, 0)
        self.render.setLight(self.dlnp)

        self.plights = []
        for position in [
            [0, 0, 20],
            [10, 10, 20],
            [-10, 10, 20],
            [-10, -10, 20],
            [10, -10, 20],
        ]:
            plight = PointLight('plight_{}'.format(position))
            plight.setColor(VBase4(0.4, 0.4, 0.4, 1))
            plnp = self.render.attachNewNode(plight)
            plnp.setPos(*position)
            self.render.setLight(plnp)
            self.plights.append(plight)

        # self.camera.setPos(0, -20, 3)
        self.trackball.node().setPos(0, 20, -3)

        print(self.camera.getPos())

    def load_pilons(self):
        self.pilon_models = []

        for color, position in self.pilons:
            pilon_model = self.loader.loadModel("models/pilon.egg")
            pilon_model.setPos(position[0], position[1], 0)
            pilon_model.reparentTo(self.render)
            self.pilon_models.append(pilon_model)


pilons = [
    [None, (0, 0)],
    [None, (3, 2)],
    [None, (-9, 3)],
]

app = PandaApp(pilons)
app.run()
