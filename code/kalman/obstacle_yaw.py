import numpy as np


class Obstacle:
    def __init__(self, x, y, theta, v, yaw):
        # Initial State x_0
        self.x = np.matrix([[x, y, theta, v, yaw]]).T
        self.P = np.diag([1000.0, 1000.0, 1000.0, 1000.0, 1000.0])

        varGPS = 6.0  # Standard Deviation of GPS Measurement
        varspeed = 1.0  # Variance of the speed measurement
        varyaw = 0.1  # Variance of the yawrate measurement
        self.R = np.matrix([[varGPS ** 2, 0.0, 0.0, 0.0],
                            [0.0, varGPS ** 2, 0.0, 0.0],
                            [0.0, 0.0, varspeed ** 2, 0.0],
                            [0.0, 0.0, 0.0, varyaw ** 2]])

    def predict(self, dt):
        if np.abs(self.x[4]) < 0.0001:  # Driving straight
            self.x[0] = self.x[0] + self.x[3] * dt * np.cos(self.x[2])
            self.x[1] = self.x[1] + self.x[3] * dt * np.sin(self.x[2])
            self.x[2] = self.x[2]
            self.x[3] = self.x[3]
            self.x[4] = 0.0000001  # avoid numerical issues in Jacobians
            JA = np.matrix([[1.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0, dt],
                            [0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0]])

        else:  # otherwise
            self.x[0] = self.x[0] + (self.x[3] / self.x[4]) * (np.sin(self.x[4] * dt + self.x[2]) - np.sin(self.x[2]))
            self.x[1] = self.x[1] + (self.x[3] / self.x[4]) * (-np.cos(self.x[4] * dt + self.x[2]) + np.cos(self.x[2]))
            self.x[2] = (self.x[2] + self.x[4] * dt + np.pi) % (2.0 * np.pi) - np.pi
            self.x[3] = self.x[3]
            self.x[4] = self.x[4]
            # Calculate the Jacobian of the Dynamic Matrix A
            # see "Calculate the Jacobian of the Dynamic Matrix with respect to the state vector"
            a13 = float((self.x[3] / self.x[4]) * (np.cos(self.x[4] * dt + self.x[2]) - np.cos(self.x[2])))
            a14 = float((1.0 / self.x[4]) * (np.sin(self.x[4] * dt + self.x[2]) - np.sin(self.x[2])))
            a15 = float((dt * self.x[3] / self.x[4]) * np.cos(self.x[4] * dt + self.x[2]) - (self.x[3] / self.x[4] ** 2) * (
                np.sin(self.x[4] * dt + self.x[2]) - np.sin(self.x[2])))
            a23 = float((self.x[3] / self.x[4]) * (np.sin(self.x[4] * dt + self.x[2]) - np.sin(self.x[2])))
            a24 = float((1.0 / self.x[4]) * (-np.cos(self.x[4] * dt + self.x[2]) + np.cos(self.x[2])))
            a25 = float((dt * self.x[3] / self.x[4]) * np.sin(self.x[4] * dt + self.x[2]) - (self.x[3] / self.x[4] ** 2) * (
                -np.cos(self.x[4] * dt + self.x[2]) + np.cos(self.x[2])))
            JA = np.matrix([[1.0, 0.0, a13, a14, a15],
                            [0.0, 1.0, a23, a24, a25],
                            [0.0, 0.0, 1.0, 0.0, dt],
                            [0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1.0]])

        sGPS = 0.5 * 8.8 * dt ** 2  # assume 8.8m/s2 as maximum acceleration, forcing the vehicle
        sCourse = 0.1 * dt  # assume 0.1rad/s as maximum turn rate for the vehicle
        sVelocity = 8.8 * dt  # assume 8.8m/s2 as maximum acceleration, forcing the vehicle
        sYaw = 1.0 * dt  # assume 1.0rad/s2 as the maximum turn rate acceleration for the vehicle

        Q = np.diag([sGPS ** 2, sGPS ** 2, sCourse ** 2, sVelocity ** 2, sYaw ** 2])

        # Project the error covariance ahead
        self.P = JA * self.P * JA.T + Q

    def correct(self, Z):
        # Measurement Function
        hx = np.matrix([[float(self.x[0])],
                        [float(self.x[1])],
                        [float(self.x[3])],
                        [float(self.x[4])]])

        JH = np.matrix([[1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0]])

        S = JH * self.P * JH.T + self.R

        K = (self.P * JH.T) * np.linalg.inv(S)

        # Update the estimate via
        Z = Z.reshape(JH.shape[0], 1)
        y = Z - (hx)  # Innovation or Residual
        self.x = self.x + (K * y)

        # Update the error covariance
        I = np.eye(5)
        self.P = (I - (K * JH)) * self.P
