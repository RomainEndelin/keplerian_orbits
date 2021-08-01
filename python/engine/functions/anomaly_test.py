import math

import pytest
from pytest import param as p

from .anomaly import (
    EccentricAnomalyFromMeanAnomaly,
    EccentricAnomalyFromTrueAnomaly,
    MeanAnomalyAtT,
    MeanAnomalyFromEccentricAnomaly,
    TrueAnomalyAtT,
    TrueAnomalyFromEccentricAnomaly,
)


@pytest.mark.parametrize(
    ("true_anomaly_at_epoch", "eccentricity", "period", "t", "expected"),
    [
        p(math.pi / 3, 0.5, 10, 0, math.pi / 3, id="t=0"),
        p(math.pi / 3, 0.5, 10, 10, math.pi / 3, id="After 1 revolution"),
        p(math.pi / 2, 0, 10, 10 / 4, math.pi, id="Circular orbit, 1/4 revolution"),
        p(0, 0.5, 10, 5, math.pi, id="Half a revolution"),
        p(math.pi / 3, 0.5, 10, 4, math.pi / 1.0363, id="Arbitrary time and orbit"),
    ],
)
def test_true_anomaly_at_t(true_anomaly_at_epoch, eccentricity, period, t, expected):
    assert TrueAnomalyAtT(
        true_anomaly_at_epoch, eccentricity, period, t
    ).evalf() == pytest.approx(expected, 1e-3)


@pytest.mark.parametrize(
    ("true_anomaly", "eccentricity"),
    [
        p(0, 0, id="circular orbit, anomaly=0"),
        p(math.pi / 3, 0, id="circular orbit"),
        p(0, 0.5, id="anomaly=0"),
        p(math.pi / 2, 0.5, id="arbitary anomaly"),
    ],
)
def test_true_anomaly_symmetric(true_anomaly, eccentricity):
    assert TrueAnomalyFromEccentricAnomaly(
        EccentricAnomalyFromTrueAnomaly(true_anomaly, eccentricity), eccentricity
    ) == pytest.approx(true_anomaly)


@pytest.mark.parametrize(
    ("eccentric_anomaly", "eccentricity"),
    [
        p(0, 0, id="circular orbit, anomaly=0"),
        p(math.pi / 3, 0, id="circular orbit"),
        p(0, 0.5, id="anomaly=0"),
        p(math.pi / 2, 0.5, id="arbitary anomaly"),
    ],
)
def test_eccentric_anomaly_symmetric(eccentric_anomaly, eccentricity):
    assert EccentricAnomalyFromMeanAnomaly(
        MeanAnomalyFromEccentricAnomaly(eccentric_anomaly, eccentricity), eccentricity
    ).evalf() == pytest.approx(eccentric_anomaly)


@pytest.mark.parametrize(
    ("true_anomaly", "eccentricity", "expected"),
    [
        p(0, 0, 0, id="circular orbit, anomaly=0"),
        p(math.pi / 3, 0, math.pi / 3, id="circular orbit"),
        p(0, 0.5, 0, id="anomaly=0"),
        p(math.pi / 2, 0.5, math.pi / 3, id="arbitary anomaly"),
    ],
)
def test_eccentric_anomaly_from_true_anomaly(true_anomaly, eccentricity, expected):
    assert EccentricAnomalyFromTrueAnomaly(true_anomaly, eccentricity) == pytest.approx(
        expected
    )


@pytest.mark.parametrize(
    ("eccentric_anomaly", "eccentricity", "expected"),
    [
        p(0, 0, 0, id="circular orbit, anomaly=0"),
        p(math.pi / 3, 0, math.pi / 3, id="circular orbit"),
        p(0, 0.5, 0, id="anomaly=0"),
        p(math.pi / 2, 0.5, math.pi / 2.9339, id="abitrary anomaly"),
    ],
)
def test_mean_anomaly_from_eccentric_anomaly(eccentric_anomaly, eccentricity, expected):
    assert MeanAnomalyFromEccentricAnomaly(
        eccentric_anomaly, eccentricity
    ) == pytest.approx(expected, 1e-3)


@pytest.mark.parametrize(
    ("mean_anomaly_at_epoch", "period", "t", "expected"),
    [
        p(math.pi / 3, 10, 0, math.pi / 3, id="t=0"),
        p(0, 10, 10, 2 * math.pi, id="full revolution"),
        p(0, 10, 2.5, math.pi / 2, id="arbitrary t"),
    ],
)
def test_mean_anomaly_at_t(mean_anomaly_at_epoch, period, t, expected):
    assert MeanAnomalyAtT(mean_anomaly_at_epoch, period, t).evalf() == pytest.approx(
        expected
    )


@pytest.mark.parametrize(
    ("mean_anomaly", "eccentricity", "expected"),
    [
        p(0, 0, 0, id="circular_orbit, anomaly=0"),
        p(math.pi / 3, 0, math.pi / 3, id="circular orbit"),
        p(0, 0.5, 0, id="anomaly=0"),
        p(math.pi / 3, 0.5, math.pi / 2.0306, id="arbitrary anomly"),
    ],
)
def test_eccentric_anomaly_from_mean_anomaly(mean_anomaly, eccentricity, expected):
    assert EccentricAnomalyFromMeanAnomaly(
        mean_anomaly, eccentricity
    ).evalf() == pytest.approx(expected, 1e-3)


@pytest.mark.parametrize(
    ("eccentric_anomaly", "eccentricity", "expected"),
    [
        p(0, 0, 0, id="circular orbit, anomaly=0"),
        p(math.pi / 3, 0, math.pi / 3, id="circular orbit"),
        p(0, 0.5, 0, id="anomaly=0"),
        p(math.pi / 3, 0.5, math.pi / 2, id="arbitrary anomaly"),
    ],
)
def test_true_anomaly_from_eccentric_anomaly(eccentric_anomaly, eccentricity, expected):
    assert TrueAnomalyFromEccentricAnomaly(
        eccentric_anomaly, eccentricity
    ) == pytest.approx(expected)
