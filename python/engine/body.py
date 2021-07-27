from functools import cached_property
from engine.symbolic_body import SymbolicBody


class Body:
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass

    @cached_property
    def backend(self):
        return SymbolicBody(self.name)
