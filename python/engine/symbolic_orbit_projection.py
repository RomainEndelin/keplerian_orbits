from functools import cached_property
from engine.functions import OrbitalVector, TrueAnomalyAtT
from sympy.physics.vector import Point

class SymbolicOrbitProjection:
    def __init__(self, orbit, t):
        self.orbit = orbit
        self.t = t
        
    @cached_property
    def true_anomaly(self):
        return TrueAnomalyAtT(
            self.orbit.true_anomaly_at_epoch,
            self.orbit.eccentricity,
            self.orbit.period,
            self.t
        )
    
    @cached_property
    def orbital_vector(self):
        return OrbitalVector(self.orbit.orbital_frame, self.orbit.semimajor_axis, self.orbit.eccentricity, self.true_anomaly)
    
    # TODO: OrbitProjection shouldn't be responsible for Point
    @cached_property
    def primary_body_as_point(self):
        return Point(self.orbit.primary_body.name)
    
    @cached_property
    def secondary_body_as_point(self):
        return self.primary_body_as_point.locatenew(
            self.orbit.secondary_body.name,
            self.orbital_vector
        )