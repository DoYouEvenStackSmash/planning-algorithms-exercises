import numpy as np
import matplotlib.pyplot as plt

# B-spline basis function (degree = 3 cubic B-spline)
def b_spline_basis(i, k, u, knots):
    if k == 0:
        return 1.0 if knots[i] <= u < knots[i + 1] else 0.0
    else:
        d1 = (u - knots[i]) / (knots[i + k] - knots[i]) if knots[i + k] != knots[i] else 0
        d2 = (knots[i + k + 1] - u) / (knots[i + k + 1] - knots[i + 1]) if knots[i + k + 1] != knots[i + 1] else 0
        return d1 * b_spline_basis(i, k - 1, u, knots) + d2 * b_spline_basis(i + 1, k - 1, u, knots)

# B-spline trajectory generation
def generate_b_spline(control_points, n_points=100):
    n_control_points = len(control_points)
    degree = 4
    # Knot vector (uniform)
    knots = np.linspace(0, 1, n_control_points + degree + 1)

    # Generate trajectory points
    u_vals = np.linspace(0, 1, n_points)
    trajectory = np.zeros((n_points, 2))

    for j, u in enumerate(u_vals):
        for i in range(n_control_points):
            basis = b_spline_basis(i, degree, u, knots)
            trajectory[j] += basis * control_points[i]
    
    return trajectory

# Objective function: minimize the total length of the trajectory
def trajectory_length(trajectory):
    return np.sum(np.sqrt(np.sum(np.diff(trajectory, axis=0)**2, axis=1)))

# Numerical gradient descent to optimize control points
def optimize_trajectory(control_points, learning_rate=0.001, n_iterations=1000):
    control_points = np.array(control_points).astype(float)
    
    for iteration in range(n_iterations):
        # Generate B-spline trajectory
        trajectory = generate_b_spline(control_points)
        
        # Compute the objective (trajectory length)
        length = trajectory_length(trajectory)
        
        # Numerical gradient computation (simple finite difference)
        grad = np.zeros_like(control_points)
        control_points+=1e-5
        new_trajectory = generate_b_spline(control_points)
        new_length = trajectory_length(new_trajectory)
        grad = (new_length - length) / 1e-5
        control_points -= 1e-5
        # for i in range(len(control_points)):
        #     for j in range(2):  # x and y coordinates
        #         control_points[i, j] += 1e-5
        #         new_trajectory = generate_b_spline(control_points)
        #         new_length = trajectory_length(new_trajectory)
        #         grad[i, j] = (new_length - length) / 1e-5
        #         control_points[i, j] -= 1e-5  # Restore control point

        # Update control points using gradient descent
        control_points -= learning_rate * grad

        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Trajectory length = {length}")

    return control_points

# Example waypoints (initial control points)
waypoints = [(0, 0), (1, 2), (2, 1), (3, 3), (4, 0), (5, 2)]

# Optimize the control points
optimized_control_points = optimize_trajectory(waypoints[1:-1])
print(optimized_control_points)
# exit()
# Generate the optimized trajectory
optimized_trajectory = generate_b_spline(optimized_control_points)

# Plot the original waypoints and the optimized trajectory
plt.figure(figsize=(8, 6))
plt.plot(*zip(*waypoints), 'ro-', label="Waypoints (Initial Control Points)")
plt.plot(optimized_trajectory[:, 0], optimized_trajectory[:, 1], 'b-', label="Optimized Trajectory")
plt.legend()
plt.title('B-Spline Optimized Trajectory')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid()
plt.show()
