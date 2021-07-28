from engine.fixtures.system import make_system
from engine.plot import plot_orbits


def main():
    system = make_system()

    t_val = 5

    fig = plot_orbits(system, t_val)
    fig.show()


if __name__ == "__main__":
    main()
