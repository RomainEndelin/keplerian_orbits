from functools import cached_property

from sympy import symbols

from engine.functions import OrbitalFrame


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
