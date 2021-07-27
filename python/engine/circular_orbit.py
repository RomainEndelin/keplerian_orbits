from functools import cached_property
import math
import numpy as np
from engine.constants import G


class CircularOrbit:
    def __init__(self, primary_body, secondary_body, radius):
        # TODO: To better handle nested orbits, this should receive parent_system and child_system
        # instead of primary_body and secondary_body
        self.primary_body = primary_body
        self.secondary_body = secondary_body
        self.radius = radius

    @cached_property
    def period(self):
        angular_motion = math.sqrt(
            G * (self.primary_body.mass + self.secondary_body.mass) / (self.radius ** 3)
        )
        return 2 * math.pi / angular_motion

    @cached_property
    def secondary_body_ellipse_points(self):
        return [
            self._secondary_body_position_at_anomaly(anomaly)
            for anomaly in np.linspace(0, 2 * np.pi, 500)
        ]

    def anomaly(self, t):
        return (t / self.period) * 2 * math.pi

    def secondary_body_position(self, t):
        return self._secondary_body_position_at_anomaly(self.anomaly(t))

    def _secondary_body_position_at_anomaly(self, anomaly):
        return [self.radius * math.cos(anomaly), self.radius * math.sin(anomaly), 0]
