from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, VBase4, TextNode
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from direct.task import Task
from direct.gui.DirectGui import *
from collections import OrderedDict
import enum

quat_params = ("x", "v_i", "a_i", "v_b", "a_b", "roll", "pitch", "yaw", "omega", "omega_dot", "error")

from math import pi, sin, cos

import numpy as np

from scaling_potato.quadcopter import Quadcopter

__author__ = "Aaron M. de Windt"

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                        parent=base.a2dTopLeft, align=TextNode.ALeft,
                        pos=(0.08, -pos - 0.04), scale=.05, font=base.font_ubuntu_mono)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, pos=(-0.1, 0.09), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1))

class mv(enum.Enum):
    forward = 0
    backwards = 1
    left = 2
    right = 3
    rotate_left = 4
    rotate_right = 5
    roll_left = 6
    roll_right = 7
    pitch_up = 8
    pitch_down = 9


class World(ShowBase):
    def __init__(self, pilons=None):
        ShowBase.__init__(self)

        self.pilons = pilons or []

        # Disable the camera trackball controls.
        # self.disableMouse()

        self.accept("w", self.handle_key_press, [mv.forward, True])
        self.accept("w-up", self.handle_key_press, [mv.forward, False])
        self.accept("a", self.handle_key_press, [mv.left, True])
        self.accept("a-up", self.handle_key_press, [mv.left, False])
        self.accept("s", self.handle_key_press, [mv.backwards, True])
        self.accept("s-up", self.handle_key_press, [mv.backwards, False])
        self.accept("d", self.handle_key_press, [mv.right, True])
        self.accept("d-up", self.handle_key_press, [mv.right, False])
        self.accept("q", self.handle_key_press, [mv.rotate_left, True])
        self.accept("q-up", self.handle_key_press, [mv.rotate_left, False])
        self.accept("e", self.handle_key_press, [mv.rotate_right, True])
        self.accept("e-up", self.handle_key_press, [mv.rotate_right, False])
        self.accept("1", self.handle_key_press, [mv.roll_left, True])
        self.accept("1-up", self.handle_key_press, [mv.roll_left, False])
        self.accept("2", self.handle_key_press, [mv.roll_right, True])
        self.accept("2-up", self.handle_key_press, [mv.roll_right, False])
        self.accept("3", self.handle_key_press, [mv.pitch_down, True])
        self.accept("3-up", self.handle_key_press, [mv.pitch_down, False])
        self.accept("4", self.handle_key_press, [mv.pitch_up, True])
        self.accept("4-up", self.handle_key_press, [mv.pitch_up, False])

        # Load fonts
        # These are here so clion can find them.
        self.font_ubuntu_mono = self.loader.loadFont('fonts/UbuntuMono-R.ttf')

        self.load_scene()
        self.load_pilons()

        self.taskMgr.add(self.main_loop, "main_loop")
        self.quadcopter_text = OrderedDict([(name, addInstructions((1 + i) * 0.06, name)) for i, name in enumerate(quat_params)])

        self.quadcopter = Quadcopter([0, -20, 1], self)
        self.movements = []

    def update_quatcopter_text(self):
        formatter = {"float_kind": lambda x: "{:10.4f}".format(x)}
        for name, text_node in self.quadcopter_text.iteritems():
            value = getattr(self.quadcopter, name)
            if isinstance(value, np.ndarray):
                value = np.array2string(value, formatter=formatter)

            text_node.setText("{:10} {}".format(name, value))

    def handle_key_press(self, movement, down):
        if down:
            if movement not in self.movements:
                self.movements.append(movement)
        else:
            if movement in self.movements:
                self.movements.remove(movement)

    # Define a procedure to move the camera.
    def main_loop(self, task):
        self.quadcopter.step(task.time)
        self.update_quatcopter_text()

        v_command = np.zeros((3,))
        omega_command = np.zeros((3,))
        if mv.forward in self.movements:
            v_command += [0, 1, 0]
        if mv.backwards in self.movements:
            v_command += [0, -1, 0]
        if mv.left in self.movements:
            v_command += [-1, 0, 0]
        if mv.right in self.movements:
            v_command += [1, 0, 0]



        if mv.roll_left in self.movements:
            omega_command += [0, -1, 0]
        if mv.roll_right in self.movements:
            omega_command += [0, 1, 0]

        if mv.pitch_up in self.movements:
            omega_command += [1, 0, 0]
        if mv.pitch_down in self.movements:
            omega_command += [-1, 0, 0]

        if mv.rotate_left in self.movements:
            omega_command += [0, 0, 1]
        if mv.rotate_right in self.movements:
            omega_command += [0, 0, -1]

        self.quadcopter.v_control(task.time, v_command*3)
        self.quadcopter.omega_control(task.time, omega_command)
        # self.quadcopter.a_b = np.array(v_command)
        # self.quadcopter.omega_dot = [0.01, 0, 0]

        return Task.cont

    def load_scene(self):
        self.scene_model = self.loader.loadModel("models/scene.egg")
        self.scene_model.reparentTo(self.render)

        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.1, 0.1, 0.1, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

        self.dlight = DirectionalLight('dlight')
        self.dlight.setColor(VBase4(0.5, 0.5, 0.5, 0.5))
        self.dlnp = self.render.attachNewNode(self.dlight)
        self.dlnp.setHpr(0, -60, 0)
        self.render.setLight(self.dlnp)

        self.plights = []
        for position in [
            [0, 0, 20],
            # [10, 10, 20],
            # [-10, 10, 20],
            # [-10, -10, 20],
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

app = World(pilons)
app.run()
