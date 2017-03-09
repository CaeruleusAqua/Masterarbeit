import numpy as np


class Obstacle:
    def __init__(self, x, y):
        # Initial State x_0
        self.x = np.matrix([[x, y, 0.0, 0.0]]).T

        # Initial Uncertainty P_0
        self.P = np.diag([1000.0, 1000.0, 1000.0, 1000.0])
        self.H = np.eye(4)

        ra = 10.0 ** 2

        self.R = np.eye(4) * ra

    def predict(self, dt):
        A = np.matrix([[1.0, 0.0, dt, 0.0],
                       [0.0, 1.0, 0.0, dt],
                       [0.0, 0.0, 1.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

        # Process Noise Covariance Q
        sv = 8.8
        G = np.matrix([[0.5 * dt ** 2],
                       [0.5 * dt ** 2],
                       [dt],
                       [dt]])

        Q = G * G.T * sv ** 2

        self.x = A * self.x

        # Project the error covariance ahead
        self.P = A * self.P * A.T + Q

    def correct(self, Z):
        # Measurement Update (Correction)
        # ===============================
        # Compute the Kalman Gain
        S = self.H * self.P * self.H.T + self.R
        K = (self.P * self.H.T) * np.linalg.pinv(S)

        # Update the estimate via z
        w = Z - (self.H * self.x)  # Innovation or Residual
        self.x = self.x + (K * w)

        I = np.eye(4)
        # Update the error covariance
        self.P = (I - (K * self.H)) * self.P
