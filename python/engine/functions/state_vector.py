from sympy import cos, sin
from sympy.matrices import Matrix


def OrbitalVector(semimajor_axis, eccentricity, true_anomaly):
    radius = OrbitalRadius(semimajor_axis, eccentricity, true_anomaly)
    return Matrix([radius * cos(true_anomaly), radius * sin(true_anomaly), 0])


def OrbitalRadius(semimajor_axis, eccentricity, true_anomaly):
    return (semimajor_axis * (1 - eccentricity ** 2)) / (
        1 + eccentricity * cos(true_anomaly)
    )
