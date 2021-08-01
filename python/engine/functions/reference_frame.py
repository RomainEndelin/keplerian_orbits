from sympy.physics.vector import ReferenceFrame


def OrbitalFrame(
    name, equatorial_frame, longitude_ascending_node, inclination, argument_of_periapsis
):
    orbital_frame = ReferenceFrame(name)
    orbital_frame.orient_body_fixed(
        equatorial_frame,
        [longitude_ascending_node, inclination, argument_of_periapsis],
        "313",
    )
    return orbital_frame
