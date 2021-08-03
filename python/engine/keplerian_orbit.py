from functools import cached_property

import numpy as np
from sympy.physics.units import gravitational_constant as G

from engine.constants import G as G_val
from engine.functions import OrbitalPeriod, OrbitalVector, TrueAnomalyAtT
from engine.symbolic_orbit import SymbolicOrbit


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
    def backend(self):
        return SymbolicOrbit(self.primary_body.backend, self.secondary_body.backend)

    @cached_property
    def eval_proper_parameters(self):
        return {
            self.backend.longitude_ascending_node: self.longitude_ascending_node,
            self.backend.inclination: self.inclination,
            self.backend.argument_of_periapsis: self.argument_of_periapsis,
        }

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
        # TODO: reference frame should be configurable, not always primary_body.equatorial_frame
        orbital_state_vector = self.orbital_vector(true_anomaly)
        equatorial_state_vector = orbital_state_vector.express(
            self.backend.primary_body.equatorial_frame
        )

        return [
            float(i)
            for i in (
                equatorial_state_vector.to_matrix(
                    self.backend.primary_body.equatorial_frame
                )
                .subs({**self.eval_proper_parameters, G: G_val})
                .transpose()
                .tolist()[0]
            )
        ]

    def true_anomaly(self, t):
        return TrueAnomalyAtT(
            self.true_anomaly_at_epoch, self.eccentricity, self.period, t
        )

    def orbital_vector(self, true_anomaly):
        return OrbitalVector(
            self.backend.orbital_frame,
            self.semimajor_axis,
            self.eccentricity,
            true_anomaly,
        )

    @cached_property
    def secondary_body_ellipse_points(self):
        return [
            self.secondary_body_position_for_anomaly(anomaly)
            for anomaly in np.linspace(0, 2 * np.pi, 500)
        ]
