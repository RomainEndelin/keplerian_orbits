import numpy as np
from scipy import optimize


def eccentric_anomaly_solution(eccentric_anomaly, eccentricity, mean_anomaly):
    return eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly) - mean_anomaly


def fprime_eccentric_anomaly(eccentric_anomaly, eccentricity, _):
    return 1 - eccentricity * np.cos(eccentric_anomaly)


def compute_eccentric_anomaly(mean_anomaly, eccentricity):
    return optimize.newton(
        eccentric_anomaly_solution,
        mean_anomaly,
        fprime_eccentric_anomaly,
        (eccentricity, mean_anomaly),
        maxiter=1000,
        tol=1e-10,
    )
