from functools import cached_property
from engine.functions import OrbitalFrame, OrbitalPeriod, EllipseInFrame
from sympy import symbols


class SymbolicOrbit:
    def __init__(self, primary_body, secondary_body):
        self.primary_body = primary_body
        self.secondary_body = secondary_body

        self.eccentricity = symbols(f"e_{secondary_body.name}")
        self.semimajor_axis = symbols(f"a_{secondary_body.name}")
        self.true_anomaly_at_epoch = symbols(f"ν_{secondary_body.name}")
        self.inclination = symbols(f"i_{secondary_body.name}")
        self.longitude_ascending_node = symbols(f"Ω_{secondary_body.name}")
        self.argument_of_periapsis = symbols(f"ω_{secondary_body.name}")

    @cached_property
    def orbital_frame(self):
        return OrbitalFrame(
            f"O_{self.secondary_body.name}",
            self.primary_body.equatorial_frame,
            self.longitude_ascending_node,
            self.inclination,
            self.argument_of_periapsis,
        )

    @cached_property
    def period(self):
        return OrbitalPeriod(
            self.primary_body.mass, self.secondary_body.mass, self.semimajor_axis
        )

    @cached_property
    def orbital_ellipse_point(self):
        anomaly = symbols("anomaly")
        # TODO: EllipseInFrame should be relative to primary body's point
        return EllipseInFrame(
            self.orbital_frame, self.semimajor_axis, self.eccentricity, anomaly
        ).express(self.primary_body.equatorial_frame)

