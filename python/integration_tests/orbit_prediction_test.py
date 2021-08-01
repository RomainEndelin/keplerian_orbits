import pytest
from engine.body import Body
from engine.system import System


def test_orbit_projection():
    sun = Body("Sun", mass=100)
    earth = Body("Earth", mass=5)
    mars = Body("Mars", mass=8)

    sun_earth_orbital_elements = {
        "semimajor_axis": 10,
        "eccentricity": 0.7,
        "true_anomaly_at_epoch": 2,
        "longitude_ascending_node": 0.7,
        "inclination": 1,
        "argument_of_periapsis": 1.5,
    }

    sun_mars_orbital_elements = {
        "semimajor_axis": 15,
        "eccentricity": 0.3,
        "true_anomaly_at_epoch": 0,
        "longitude_ascending_node": 0.2,
        "inclination": 0,
        "argument_of_periapsis": 0.4,
    }

    system = System(
        sun, [[earth, sun_earth_orbital_elements], [mars, sun_mars_orbital_elements]]
    )
    t = 5
    assert system.all_positions_relative_to(system.primary_body, t) == {
        sun: [0, 0, 0],
        earth: pytest.approx([-4.2756, -5.3847, -2.1243], 1e-3),
        mars: pytest.approx([8.6659, 5.9289, 0], 1e-3),
    }
