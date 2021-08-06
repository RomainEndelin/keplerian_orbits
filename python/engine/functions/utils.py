from sympy import Ellipse
from sympy import Point as Point2D
from sympy import symbols

anomaly, t = symbols("anomaly t")


# This function returns the same result as OrbitalVector, but with a different implementation
def EllipseInFrame(frame, semimajor_axis, eccentricity, anomaly):
    # Anomaly is growing linearly here, independant from the true_anomaly
    orbit = Ellipse(
        Point2D(-semimajor_axis * eccentricity, 0),
        hradius=semimajor_axis,
        eccentricity=eccentricity,
    )
    x, y = orbit.arbitrary_point(parameter=anomaly)
    return x * frame.x + y * frame.y
