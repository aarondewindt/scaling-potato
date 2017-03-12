import numpy as np


class PIDControl:
    def __init__(self, k_p, k_i, k_d):
        self.command = None
        self.output = np.empty((0,))
        self.integral = np.empty((0,))
        self.derivative = np.empty((0,))
        self.prev_error = None
        self.time = None
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d

    def step(self, time, value):
        if self.prev_error is None:
            length = len(value)
            if self.command is None:
                self.command = np.zeros((length,))
            self.output = np.zeros((length,))
            self.integral = np.zeros((length,))
            self.derivative = np.zeros((length,))
            self.prev_error = value - self.command
            self.time = time
        else:
            error = self.command - value
            dt = time - self.time
            self.time = time

            self.integral += (self.prev_error + error) / 2 * dt
            self.derivative = (error - self.prev_error) / dt
            self.prev_error = error

            self.output = error * self.k_p + self.integral * self.k_i + self.derivative * self.k_d
