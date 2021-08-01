import math

import pytest
from pytest import param as p
from sympy.physics.vector import ReferenceFrame

from .reference_frame import OrbitalFrame


@pytest.mark.parametrize(
    ("longitude_ascending_node", "inclination", "argument_of_periapsis", "expected"),
    [
        p(0, 0, 0, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], id="no rotation"),
        p(
            math.pi / 3,
            0,
            0,
            [[0.5, 0.8660, 0], [-0.8660, 0.5, 0], [0, 0, 1]],
            id="with longitude of ascending node",
        ),
        p(
            0,
            math.pi / 3,
            0,
            [[1, 0, 0], [0, 0.5, 0.8660], [0, -0.8660, 0.5]],
            id="with inclination",
        ),
        p(
            0,
            0,
            math.pi / 3,
            [[0.5, 0.8660, 0], [-0.8660, 0.5, 0], [0, 0, 1]],
            id="with argument of periapsis",
        ),
        p(
            math.pi / 4,
            math.pi / 2,
            math.pi / 3,
            [[0.3536, 0.3536, 0.8660], [-0.6124, -0.6124, 0.5], [0.7071, -0.7071, 0.0]],
            id="with arbitrary parameters",
        ),
    ],
)
def test_orbital_frame(
    longitude_ascending_node, inclination, argument_of_periapsis, expected
):
    E = ReferenceFrame("E")
    assert OrbitalFrame(
        "a", E, longitude_ascending_node, inclination, argument_of_periapsis
    ).dcm(E).tolist() == [pytest.approx(row, 1e-3) for row in expected]
