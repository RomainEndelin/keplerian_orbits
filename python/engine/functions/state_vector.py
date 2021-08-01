from sympy import cos, sin


def OrbitalVector(orbital_frame, semimajor_axis, eccentricity, true_anomaly):
    radius = OrbitalRadius(semimajor_axis, eccentricity, true_anomaly)
    return orbital_frame.x * radius * cos(
        true_anomaly
    ) + orbital_frame.y * radius * sin(true_anomaly)


def OrbitalRadius(semimajor_axis, eccentricity, true_anomaly):
    return (semimajor_axis * (1 - eccentricity ** 2)) / (
        1 + eccentricity * cos(true_anomaly)
    )
