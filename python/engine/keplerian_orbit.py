from functools import cached_property

import numpy as np
from sympy.physics.units import gravitational_constant as G

from engine.constants import G as G_val
from engine.functions import (
    OrbitalPeriod,
    OrbitalToEquatorialFrameDCM,
    OrbitalVector,
    TrueAnomalyAtT,
)


class KeplerianOrbit:
    def __init__(
        self,
        primary_body,
        secondary_body,
        semimajor_axis,
        eccentricity,
        true_anomaly_at_epoch,
        longitude_ascending_node,
        inclination,
        argument_of_periapsis,
    ):
        self.primary_body = primary_body
        self.secondary_body = secondary_body
        self.semimajor_axis = semimajor_axis
        self.eccentricity = eccentricity
        self.true_anomaly_at_epoch = true_anomaly_at_epoch
        self.longitude_ascending_node = longitude_ascending_node
        self.inclination = inclination
        self.argument_of_periapsis = argument_of_periapsis

    @cached_property
    def orbital_frame_dcm(self):
        return OrbitalToEquatorialFrameDCM(
            self.longitude_ascending_node, self.inclination, self.argument_of_periapsis
        )

    @cached_property
    def period(self):
        return OrbitalPeriod(
            self.primary_body.mass, self.secondary_body.mass, self.semimajor_axis
        )

    def primary_body_position(self, _t):
        return [0, 0, 0]

    def secondary_body_position(self, t):
        anomaly = self.true_anomaly(t)
        return self.secondary_body_position_for_anomaly(anomaly)

    def secondary_body_position_for_anomaly(self, true_anomaly):
        orbital_state_vector = self.orbital_vector_matrix(true_anomaly)
        equatorial_state_vector = self.orbital_frame_dcm * orbital_state_vector

        return [
            float(i)
            for i in (equatorial_state_vector.subs(G, G_val).transpose().tolist()[0])
        ]

    def true_anomaly(self, t):
        return TrueAnomalyAtT(
            self.true_anomaly_at_epoch, self.eccentricity, self.period, t
        )

    def orbital_vector_matrix(self, true_anomaly):
        return OrbitalVector(self.semimajor_axis, self.eccentricity, true_anomaly)

    @cached_property
    def secondary_body_ellipse_points(self):
        return [
            self.secondary_body_position_for_anomaly(anomaly)
            for anomaly in np.linspace(0, 2 * np.pi, 500)
        ]
