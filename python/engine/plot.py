import numpy as np

def trace_bodies(system, origin, t):
    body_positions = system.all_positions_relative_to(origin, t)
    x, y, z = zip(*[position for _, position in body_positions.items()])
    return go.Scatter3d(x=x, y=y, z=z, mode="markers")

def trace_orbit_trajectory(trajectory):
    x_trajectory, y_trajectory, z_trajectory = np.transpose(trajectory)
    return go.Scatter3d(
        x=x_trajectory,
        y=y_trajectory,
        z=z_trajectory,
        mode="lines",
        line=dict(color="darkblue", width=0.5),
    )

def plot_orbits(system, t):
    origin = system.primary_body
    
    trajectories = [trace_orbit_trajectory(trajectory) for trajectory in system.all_trajectories(origin)]
    bodies = trace_bodies(system, origin, t)
    
    fig = go.Figure(data=[bodies, *trajectories])
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4),
            yaxis=dict(nticks=4),
            zaxis=dict(nticks=4),
        )
    )
    return fig
