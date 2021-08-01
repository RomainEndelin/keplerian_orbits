import math

import pytest

from .anomaly_computation import compute_eccentric_anomaly


@pytest.mark.parametrize(
    "mean_anomaly,eccentricity,expected",
    [
        (0, 0, 0),
        (math.pi / 3, 0, math.pi / 3),
        (0, 0.5, 0),
        (math.pi / 3, 0.5, math.pi / 2.0306),
    ],
)
def test_eccentric_anomaly_from_mean_nomaly(mean_anomaly, eccentricity, expected):
    assert compute_eccentric_anomaly(mean_anomaly, eccentricity) == pytest.approx(
        expected, 1e-3
    )
