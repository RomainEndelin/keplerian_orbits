from functools import cached_property
from engine.keplerian_orbit import KeplerianOrbit

class System:
    def __init__(self, primary_body, orbit_definitions, OrbitalEngine=KeplerianOrbit):
        self.primary_body = primary_body
        self.orbits = [
            OrbitalEngine(primary_body, secondary_body, **orbital_elements)
            for [secondary_body, orbital_elements]
            in orbit_definitions
        ]
        
    @cached_property
    def all_bodies(self):
        # TODO: Handle tree navigation for nested orbits
        return [self.primary_body, *[orbit.secondary_body for orbit in self.orbits]]
    
    @cached_property
    def all_orbits(self):
        # TODO: Handle tree navigation for nested orbits
        return self.orbits
        
    def all_positions_relative_to(self, reference_body, t):
        if reference_body != self.primary_body:
            raise NotImplementedError("Can only evaluate positions relative to primary body")
        return {
            body: self._body_position_relative_to(body, reference_body, t) for body in self.all_bodies
        }
    
    def all_trajectories(self, reference_body):
        if reference_body != self.primary_body:
            raise NotImplementedError("Can only evaluate trajectories relative to primary body")
        return [orbit.secondary_body_ellipse_points for orbit in self.all_orbits]
    
    def _body_position_relative_to(self, subject_body, reference_body, t):
        # TODO: Provide a referenceFrame as well as/in-lieu of a referenceBody
        if subject_body == reference_body:
            return [0, 0, 0]
        else:
            orbit = next(
                (
                    orbit
                    for orbit in self.orbits
                    if orbit.secondary_body == subject_body and orbit.primary_body == reference_body
                ),
                None
            )
            if orbit is None:
                raise NotImplementedError("Can only evaluate the position of a secondary body relative to primary")
            return orbit.secondary_body_position(t)