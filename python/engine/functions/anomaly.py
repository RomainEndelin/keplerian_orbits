from engine.functions.anomaly_computation import compute_eccentric_anomaly
from sympy import acos, atan, cos, pi, sin, sqrt, tan
from sympy.utilities.lambdify import implemented_function


def TrueAnomalyAtT(true_anomaly_at_epoch, eccentricity, period, t):
    eccentric_anomaly_at_epoch = EccentricAnomalyFromTrueAnomaly(
        true_anomaly_at_epoch, eccentricity
    )
    mean_anomaly_at_epoch = MeanAnomalyFromEccentricAnomaly(
        eccentric_anomaly_at_epoch, eccentricity
    )

    mean_anomaly = MeanAnomalyAtT(mean_anomaly_at_epoch, period, t)

    eccentric_anomaly = EccentricAnomalyFromMeanAnomaly(mean_anomaly, eccentricity)
    return TrueAnomalyFromEccentricAnomaly(eccentric_anomaly, eccentricity)


def EccentricAnomalyFromTrueAnomaly(true_anomaly, eccentricity):
    return acos(
        (eccentricity + cos(true_anomaly)) / (1 + eccentricity * cos(true_anomaly))
    )


def MeanAnomalyFromEccentricAnomaly(eccentric_anomaly, eccentricity):
    return eccentric_anomaly - eccentricity * sin(eccentric_anomaly)


def MeanAnomalyAtT(mean_anomaly_at_epoch, period, t):
    return mean_anomaly_at_epoch + (2 * pi / period) * t


EccentricAnomalyFromMeanAnomaly = implemented_function(
    "Ecc",
    lambda mean_anomaly, eccentricity: compute_eccentric_anomaly(
        float(mean_anomaly), float(eccentricity)
    ),
)


def TrueAnomalyFromEccentricAnomaly(eccentric_anomaly, eccentricity):
    return 2 * atan(
        sqrt((1 + eccentricity) / (1 - eccentricity)) * tan(eccentric_anomaly / 2)
    )
