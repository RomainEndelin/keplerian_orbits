import math

import pytest
from pytest import param as p

from engine.body import Body

from .keplerian_orbit import KeplerianOrbit


@pytest.fixture
def primary_body(request):
    return Body("primary", request.param)


@pytest.fixture
def secondary_body(request):
    return Body("secondary", request.param)


# TODO: Find a better way to not duplicate parameters between tests
@pytest.mark.parametrize(
    (
        "primary_body",
        "secondary_body",
        "semimajor_axis",
        "eccentricity",
        "true_anomaly_at_epoch",
        "longitude_ascending_node",
        "inclination",
        "argument_of_periapsis",
        "t",
        "expected",
    ),
    [
        p(1e10, 1, 10, 0, 0, 0, 0, 0, 0, [0, 0, 0], id="basic orbit, t=0"),
        p(
            1e10,
            1,
            10,
            0.5,
            5 * math.pi / 3,
            math.pi / 2,
            math.pi / 5,
            math.pi / 3,
            100,
            [0, 0, 0],
            id="arbitrary orbit",
        ),
    ],
    indirect=["primary_body", "secondary_body"],
)
def test_primary_body_position(
    primary_body,
    secondary_body,
    semimajor_axis,
    eccentricity,
    true_anomaly_at_epoch,
    longitude_ascending_node,
    inclination,
    argument_of_periapsis,
    t,
    expected,
):
    orbit = KeplerianOrbit(
        primary_body,
        secondary_body,
        semimajor_axis,
        eccentricity,
        true_anomaly_at_epoch,
        longitude_ascending_node,
        inclination,
        argument_of_periapsis,
    )
    assert orbit.primary_body_position(t) == pytest.approx(expected, 1e-3)


@pytest.mark.parametrize(
    (
        "primary_body",
        "secondary_body",
        "semimajor_axis",
        "eccentricity",
        "true_anomaly_at_epoch",
        "longitude_ascending_node",
        "inclination",
        "argument_of_periapsis",
        "t",
        "expected",
    ),
    [
        p(1e10, 1, 10, 0, 0, 0, 0, 0, 0, [10, 0, 0], id="basic orbit, t=0"),
        p(
            1e10,
            1,
            10,
            0.5,
            5 * math.pi / 3,
            math.pi / 2,
            math.pi / 5,
            math.pi / 3,
            100,
            [9.9375, -8.5197, -7.2200],
            id="arbitrary orbit",
        ),
    ],
    indirect=["primary_body", "secondary_body"],
)
def test_secondary_body_position(
    primary_body,
    secondary_body,
    semimajor_axis,
    eccentricity,
    true_anomaly_at_epoch,
    longitude_ascending_node,
    inclination,
    argument_of_periapsis,
    t,
    expected,
):
    orbit = KeplerianOrbit(
        primary_body,
        secondary_body,
        semimajor_axis,
        eccentricity,
        true_anomaly_at_epoch,
        longitude_ascending_node,
        inclination,
        argument_of_periapsis,
    )
    assert orbit.secondary_body_position(t) == pytest.approx(expected, 1e-3)
