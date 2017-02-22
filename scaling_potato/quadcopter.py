from scipy.integrate import ode
import numpy as np
from math import pi
from panda3d.core import WindowProperties, VBase3

__author__ = "Aaron M. de Windt"


class Quadcopter(object):
    """
    Object handling the quadcopter dynamics and simulated camera.

    :param list init_x: Initial position of the quadcopter.
    :param direct.showbase.ShowBase.ShowBase pbase: Main Panda3d ShowBase
    """

    def __init__(self, init_x, pbase=None):
        self.x = np.array(init_x)
        self.v = np.array([0]*3)
        self.a = np.array([0]*3)
        self.yaw = 0.
        self.yaw_rate = 0.
        self.yaw_acc = 0.

        self.time = None

        # Explicit runge-kutta method of order (4)5 due to Dormand & Prince
        self.integrator = ode(self.rhs_equation).set_integrator('dopri5')

        self.pbase = pbase
        if pbase is not None:
            # Create new window for the quadcopter view.
            wp = WindowProperties()
            wp.setSize(500, 400)
            wp.setOrigin(512, 128)
            win = pbase.openWindow(props=wp, )  # aspectRatio=1

            # Create quadcopter node.
            self.node_path = pbase.render.attachNewNode("Quadcopter")
            self.node_path.setPos(*self.x)

            # Configure camera
            self.camera = pbase.camList[-1]
            self.camera.reparentTo(self.node_path)
            self.camera.setH(-90)

            # Load in quadcopter model
            self.model = pbase.loader.loadModel("models/cube.egg")
            self.model.reparentTo(self.node_path)
            self.model.setScale(1/8., 1/8., 1/8.)

    @property
    def state_vector(self):
        state_vector = np.append([], self.x)
        state_vector = np.append(state_vector, self.v)
        state_vector = np.append(state_vector, self.yaw)
        state_vector = np.append(state_vector, self.yaw_rate)
        return state_vector

    @state_vector.setter
    def state_vector(self, value):
        self.x = value[:3]
        self.v = value[3:6]
        self.yaw = value[6] % (2 * pi)
        self.yaw_rate = value[7]

    @property
    def state_vector_dot(self):
        """
        Property with the state vector that's passed to the integrator.
        """
        state_vector = np.append([], self.v)
        state_vector = np.append(state_vector, self.node_path.getMat().xformVec(VBase3(*self.a)))
        state_vector = np.append(state_vector, self.yaw_rate)
        state_vector = np.append(state_vector, self.yaw_acc)
        return state_vector

    @state_vector_dot.setter
    def state_vector_dot(self, value):
        self.v = value[:3]
        self.a = value[3:6]
        self.yaw_rate = value[6]
        self.yaw_acc = value[7]

    def step(self, time):
        if self.time is None:
            self.integrator.set_initial_value(self.state_vector, time)
            self.time = time
        else:
            self.integrator.integrate(time)
            self.time = self.integrator.t
            self.state_vector = self.integrator.y
        if self.pbase is not None:
            self.node_path.setPos(*self.x)
            self.node_path.setH(self.yaw * 180 / pi)

    def rhs_equation(self, t, y):
        self.state_vector = y
        return self.state_vector_dot
