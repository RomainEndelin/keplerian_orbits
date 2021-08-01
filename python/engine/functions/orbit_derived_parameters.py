from sympy import pi, sqrt
from sympy.physics.units import gravitational_constant as G


def OrbitalPeriod(
    primary_mass, secondary_mass, semimajor_axis, gravitational_constant=G
):
    mean_angular_motion = sqrt(
        gravitational_constant * (primary_mass + secondary_mass) / (semimajor_axis ** 3)
    )
    return 2 * pi / mean_angular_motion
