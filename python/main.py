from engine.body import Body
from engine.system import System
from engine.circular_orbit import CircularOrbit
from engine.plot import plot_orbits

def main():
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
    sun_earth_circular_orbital_element = {
        "radius": sun_earth_orbital_elements["semimajor_axis"]
    }

    sun_mars_orbital_elements = {
        "semimajor_axis": 15,
        "eccentricity": 0.3,
        "true_anomaly_at_epoch": 0,
        "longitude_ascending_node": 0.2,
        "inclination": 0,
        "argument_of_periapsis": 0.4,
    }
    sun_mars_circular_orbital_element = {
        "radius": sun_mars_orbital_elements["semimajor_axis"]
    }

    simplified = True
    if simplified:
        system = System(
            sun,
            [
                [earth, sun_earth_circular_orbital_element],
                [mars, sun_mars_circular_orbital_element]
            ],
            OrbitalEngine=CircularOrbit
        )
    else:
        system = System(
            sun,
            [
                [earth, sun_earth_orbital_elements],
                [mars, sun_mars_orbital_elements]
            ]
        )

    t_val = 5

    fig = plot_orbits(system, t_val)
    fig.show()

if __name__ == "__main__":
    main()