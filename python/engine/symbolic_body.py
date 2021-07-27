from sympy import symbols
from sympy.physics.vector import ReferenceFrame

class SymbolicBody:
    def __init__(self, name):
        self.name = name
        self.mass = symbols(f"m_{name}")
        self.equatorial_frame = ReferenceFrame(f"E_{name}")