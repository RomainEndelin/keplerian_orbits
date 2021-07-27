from sympy import Ellipse, Function
from sympy import Point as Point2D
from sympy import acos, atan, cos, pi, sin, sqrt, symbols, tan
from sympy.physics.units import gravitational_constant as G
from sympy.physics.vector import ReferenceFrame
from sympy.utilities.lambdify import implemented_function

from engine.computations import compute_eccentric_anomaly

anomaly, t = symbols("anomaly t")


def OrbitalFrame(
    name, equatorial_frame, longitude_ascending_node, inclination, argument_of_periapsis
):
    orbital_frame = ReferenceFrame(name)
    orbital_frame.orient_body_fixed(
        equatorial_frame,
        [longitude_ascending_node, inclination, argument_of_periapsis],
        "313",
    )
    return orbital_frame


def OrbitalPeriod(
    primary_mass, secondary_mass, semimajor_axis, gravitational_constant=G
):
    mean_angular_motion = sqrt(
        gravitational_constant * (primary_mass + secondary_mass) / (semimajor_axis ** 3)
    )
    return 2 * pi / mean_angular_motion


def EllipseInFrame(frame, semimajor_axis, eccentricity, anomaly):
    # Anomaly is growing linearly here, independant from the true_anomaly
    orbit = Ellipse(
        Point2D(-semimajor_axis * eccentricity, 0),
        hradius=semimajor_axis,
        eccentricity=eccentricity,
    )
    x, y = orbit.arbitrary_point(parameter=anomaly)
    return x * frame.x + y * frame.y


def EccentricAnomalyFromTrueAnomaly(true_anomaly, eccentricity):
    return acos(
        (eccentricity + cos(true_anomaly)) / (1 + eccentricity * cos(true_anomaly))
    )


def MeanAnomalyFromEccentricAnomaly(eccentric_anomaly, eccentricity):
    return eccentric_anomaly - eccentricity * sin(eccentric_anomaly)


def MeanAnomalyAtT(mean_anomaly_at_epoch, period, t):
    return mean_anomaly_at_epoch + (2 * pi / period) * t


def EccentricAnomalyFromMeanAnomaly(mean_anomaly, eccentricity):
    compute_eccentric_anomaly_function = implemented_function(
        Function("Ecc"), compute_eccentric_anomaly
    )
    return compute_eccentric_anomaly_function(mean_anomaly, eccentricity)


def TrueAnomalyFromEccentricAnomaly(eccentric_anomaly, eccentricity):
    return 2 * atan(
        sqrt((1 + eccentricity) / (1 - eccentricity)) * tan(eccentric_anomaly / 2)
    )


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


def OrbitalRadius(semimajor_axis, eccentricity, true_anomaly):
    return (semimajor_axis * (1 - eccentricity ** 2)) / (
        1 + eccentricity * cos(true_anomaly)
    )


def OrbitalVector(orbital_frame, semimajor_axis, eccentricity, true_anomaly):
    radius = OrbitalRadius(semimajor_axis, eccentricity, true_anomaly)
    return orbital_frame.x * radius * cos(
        true_anomaly
    ) + orbital_frame.y * radius * sin(true_anomaly)
