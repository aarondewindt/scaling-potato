from scipy.integrate import ode
import numpy as np
from math import pi
from panda3d.core import WindowProperties, VBase3, LQuaternionf

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
        self.q = np.array([0, 1, 0, 0])
        self.omega = np.array([0]*3)
        self.omega_dot = np.array([0]*3)

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
            self.q = np.array(self.node_path.getQuat())

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
        state_vector = np.append(state_vector, self.q)
        state_vector = np.append(state_vector, self.omega)
        return state_vector

    @state_vector.setter
    def state_vector(self, value):
        self.x = value[:3]
        self.v = value[3:6]
        self.q = value[6:10]
        self.omega = value[10:]

    @property
    def state_vector_dot(self):
        """
        Property with the state vector that's passed to the integrator.
        """
        state_vector = np.append([], self.v)
        state_vector = np.append(state_vector, self.node_path.getMat().xformVec(VBase3(*self.a)))
        state_vector = np.append(state_vector, omega2qdot(self.omega, self.q))
        state_vector = np.append(state_vector, self.omega_dot)
        return state_vector

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
            self.node_path.setQuat(LQuaternionf(*self.q))

    def rhs_equation(self, t, y):
        self.state_vector = y
        return self.state_vector_dot


def omega2qdot(omega, quat, K=1.0):
    """Converts Rotational Rates (omega) to Quaternion rates

    :param omega: Rotational Rate column vector
    :type omega: numpy_array
    :param q: Quaternions column vector
    :type q: numpy_array
    :return: Quaternion Rates
    :rtype: numpy_array
    """

    p = omega[0]
    q = omega[1]
    r = omega[2]

    e = K * (1-(quat[0] * quat[0] + quat[1] * quat[1] + quat[2] * quat[2] + quat[3] * quat[3]))

    qdot = 0.5*np.array([[e*quat[0] - p*quat[1] - q*quat[2] - r*quat[3]],
                         [p*quat[0] + e*quat[1] + r*quat[2] - q*quat[3]],
                         [q*quat[0] - r*quat[1] + e*quat[2] + p*quat[3]],
                         [r*quat[0] + q*quat[1] - p*quat[2] + e*quat[3]]])

    return qdot