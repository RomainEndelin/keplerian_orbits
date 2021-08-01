import math

import pytest
from pytest import param as p
from sympy.physics.vector import ReferenceFrame

from .state_vector import OrbitalRadius, OrbitalVector


@pytest.mark.parametrize(
    ("semimajor_axis", "eccentricity", "true_anomaly", "expected"),
    [
        p(10, 0, 0, (10, 0), id="circular orbit, anomaly=0"),
        p(10, 0.5, 0, (5, 0), id="anomaly=0"),
        p(10, 0.5, math.pi / 3, (3, 5.1962), id="arbitrary anomaly"),
    ],
)
def test_orbital_vector(semimajor_axis, eccentricity, true_anomaly, expected):
    N = ReferenceFrame("N")
    vector = OrbitalVector(N, semimajor_axis, eccentricity, true_anomaly)
    assert N.x.dot(vector) == pytest.approx(expected[0], 1e-3)
    assert N.y.dot(vector) == pytest.approx(expected[1], 1e-3)
    assert N.z.dot(vector) == 0


@pytest.mark.parametrize(
    ("semimajor_axis", "eccentricity", "true_anomaly", "expected"),
    [
        p(10, 0, math.pi / 3, 10, id="circular orbit"),
        p(10, 0.5, 0, 5, id="at perigee (0)"),
        p(10, 0.5, math.pi / 4, 5.5410, id="at pi / 4"),
        p(10, 0.5, math.pi / 2, 7.5, id="at pi / 2"),
        p(10, 0.5, math.pi, 15, id="at apogee (half revolution)"),
    ],
)
def test_orbital_radius(semimajor_axis, eccentricity, true_anomaly, expected):
    assert OrbitalRadius(semimajor_axis, eccentricity, true_anomaly) == pytest.approx(
        expected, 1e-3
    )
