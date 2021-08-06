from sympy.physics.vector import ReferenceFrame


def OrbitalToEquatorialFrameDCM(
    longitude_ascending_node, inclination, argument_of_periapsis
):
    return (
        EquatorialToOrbitalFrameDCM(
            longitude_ascending_node, inclination, argument_of_periapsis
        )
        ** -1
    )


def EquatorialToOrbitalFrameDCM(
    longitude_ascending_node, inclination, argument_of_periapsis
):
    equatorial_frame = ReferenceFrame("E")
    orbital_frame = ReferenceFrame("O")
    orbital_frame.orient_body_fixed(
        equatorial_frame,
        [longitude_ascending_node, inclination, argument_of_periapsis],
        "313",
    )
    return orbital_frame.dcm(equatorial_frame)
