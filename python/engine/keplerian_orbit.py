from functools import cached_property
from engine.symbolic_orbit import SymbolicOrbit
from engine.symbolic_orbit_projection import SymbolicOrbitProjection
from engine.functions import t, anomaly
from engine.constants import G
import numpy as np
from sympy.utilities.lambdify import lambdify

class KeplerianOrbit:
    def __init__(self, primary_body, secondary_body, semimajor_axis, eccentricity, true_anomaly_at_epoch, longitude_ascending_node, inclination, argument_of_periapsis):
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
    def projection_backend(self):
        return SymbolicOrbitProjection(self.backend, t)
    
    @cached_property
    def eval_proper_parameters(self):
        return {
            self.backend.semimajor_axis: self.semimajor_axis,
            self.backend.eccentricity: self.eccentricity,
            self.backend.true_anomaly_at_epoch: self.true_anomaly_at_epoch,
            self.backend.longitude_ascending_node: self.longitude_ascending_node,
            self.backend.inclination: self.inclination,
            self.backend.argument_of_periapsis: self.argument_of_periapsis,
            self.primary_body.backend.mass: self.primary_body.mass,
            self.secondary_body.backend.mass: self.secondary_body.mass,
        }
    
    @cached_property # returns a function
    def primary_body_position(self):
        return self._make_body_position_lambda(self.projection_backend.primary_body_as_point)
        
    @cached_property # returns a function
    def secondary_body_position(self):
        return self._make_body_position_lambda(self.projection_backend.secondary_body_as_point)
    

    @cached_property
    def secondary_body_ellipse_points(self):
        return [
            self._secondary_body_ellipse_point(anomaly)
            for anomaly in np.linspace(0, 2 * np.pi, 500)
        ]
    
    @cached_property # returns a function
    def _secondary_body_ellipse_point(self):
        return lambdify(
            (anomaly),
            # TODO: reference frame should be configurable, not always primary_body.equatorial_frame
            self.backend.orbital_ellipse_point
            .to_matrix(self.primary_body.backend.equatorial_frame)
            .subs(self.eval_proper_parameters)
            .transpose()
            .tolist()[0],
        )
    
    def _make_body_position_lambda(self, body):
        return lambdify(
            (self.projection_backend.t),
            body.pos_from(self.projection_backend.primary_body_as_point)
            # TODO: reference frame should be configurable, not always primary_body.equatorial_frame
            .to_matrix(self.primary_body.backend.equatorial_frame)
            .subs({**self.eval_proper_parameters, G: G})
            .transpose()
            .tolist()[0],
        )