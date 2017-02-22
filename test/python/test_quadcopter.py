from __future__ import absolute_import

import unittest
from math import pi

from scaling_potato.quadcopter import Quadcopter

import numpy as np
import numpy.testing as npt




class TestQuadcopter(unittest.TestCase):
    def test_state_vector(self):
        qc = Quadcopter([1, 2, 3])
        npt.assert_allclose(qc.state_vector, [1, 2, 3, 0, 0, 0, 0, 0])
        qc.state_vector = np.array([9., 8., 7., 6., 5., 4., 3., 2])
        npt.assert_allclose(qc.state_vector, [9., 8., 7., 6., 5., 4., 3., 2])
        npt.assert_allclose(qc.x, np.array([9., 8., 7.]))
        npt.assert_allclose(qc.v, np.array([6., 5., 4.]))
        self.assertAlmostEqual(qc.yaw, 3.)
        self.assertAlmostEqual(qc.yaw_rate, 2.)

    def test_state_vector_dot(self):
        qc = Quadcopter([1, 2, 3])
        npt.assert_allclose(qc.state_vector_dot, [0, 0, 0, 0, 0, 0, 0, 0])
        qc.state_vector_dot = np.array([9., 8., 7., 6., 5., 4., 3., 2])
        npt.assert_allclose(qc.state_vector_dot, [9., 8., 7., 6., 5., 4., 3., 2])
        npt.assert_allclose(qc.v, np.array([9., 8., 7.]))
        npt.assert_allclose(qc.a, np.array([6., 5., 4.]))
        self.assertAlmostEqual(qc.yaw_rate, 3.)
        self.assertAlmostEqual(qc.yaw_acc, 2.)

    def test_simple_simulation(self):
        qc = Quadcopter([0, 0, 0])
        qc.a = np.array([[1, 0, 0]])
        qc.step(0)
        qc.step(1)
        npt.assert_allclose(qc.x, np.array([.5, 0., 0.]))
        npt.assert_allclose(qc.v, np.array([1., 0., 0.]))

    def test_yaw_simulation(self):
        qc = Quadcopter([0, 0, 0])
        qc.yaw_acc = 6 * pi
        qc.step(0)
        qc.step(1)
        self.assertAlmostEqual(qc.yaw, pi)
        self.assertAlmostEqual(qc.yaw_rate, 6 * pi)


if __name__ == '__main__':
    unittest.main()


