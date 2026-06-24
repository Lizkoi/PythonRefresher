import numpy as np
from typing import Callable, Tuple, List

class UnconstrainedOptimizer:
    def __init__(self, tolerance=1e-6, max_iterations=1000):
        # I prefer more readable parameter names
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def steepest_descent(self, objective_func, gradient_func, starting_point,
                         step_size=0.01, use_line_search=False):
        # Making a copy so we don't mess with the original
        current_x = starting_point.copy()
        path_history = [current_x.copy()]

        iteration_count = 0
        while iteration_count < self.max_iterations:
            grad = gradient_func(current_x)

            # Check if we've converged
            gradient_norm = np.linalg.norm(grad)
            if gradient_norm < self.tolerance:
                print(f"Converged after {iteration_count} iterations")
                break

            # Decide on step size
            if use_line_search:
                alpha = self._find_good_step_size(objective_func, gradient_func, current_x, -grad)
            else:
                alpha = step_size

            # Take the step
            current_x = current_x - alpha * grad
            path_history.append(current_x.copy())
            iteration_count += 1

        return current_x, path_history

    def newton_method(self, objective_func, gradient_func, hessian_func,
                      starting_point, use_line_search=True):
        current_x = starting_point.copy()
        path_history = [current_x.copy()]

        for iter_num in range(self.max_iterations):
            grad = gradient_func(current_x)
            hess = hessian_func(current_x)

            if np.linalg.norm(grad) < self.tolerance:
                print(f"Newton method converged at iteration {iter_num}")
                break

            # Try to solve the Newton system
            try:
                newton_direction = -np.linalg.solve(hess, grad)
            except np.linalg.LinAlgError:
                # Fallback when Hessian is problematic
                print("Oops! Hessian is singular, using steepest descent direction instead")
                newton_direction = -grad

            # Determine step length
            if use_line_search:
                step_length = self._find_good_step_size(objective_func, gradient_func, current_x, newton_direction)
            else:
                step_length = 1.0  # Full Newton step

            current_x = current_x + step_length * newton_direction
            path_history.append(current_x.copy())

        return current_x, path_history

    def conjugate_gradient(self, objective_func, gradient_func, starting_point,
                           cg_method='fr'):
        # Fletcher-Reeves is my go-to, but Polak-Ribiere works too
        current_x = starting_point.copy()
        path_history = [current_x.copy()]

        current_grad = gradient_func(current_x)
        search_direction = -current_grad  # Start with steepest descent

        for i in range(self.max_iterations):
            if np.linalg.norm(current_grad) < self.tolerance:
                print(f"CG converged at iteration {i}")
                break

            # Line search to find optimal step size
            step_size = self._find_good_step_size(objective_func, gradient_func, current_x, search_direction)

            # Update position
            next_x = current_x + step_size * search_direction
            next_grad = gradient_func(next_x)

            # Calculate beta for conjugate direction
            if cg_method.lower() == 'fr':
                # Fletcher-Reeves formula
                beta_value = np.dot(next_grad, next_grad) / np.dot(current_grad, current_grad)
            elif cg_method.lower() == 'pr':
                # Polak-Ribiere formula (sometimes works better in practice)
                beta_value = np.dot(next_grad, next_grad - current_grad) / np.dot(current_grad, current_grad)
            else:
                raise ValueError("CG method should be either 'fr' or 'pr'")

            # Update search direction
            search_direction = -next_grad + beta_value * search_direction

            # Move to next iteration
            current_x = next_x
            current_grad = next_grad
            path_history.append(current_x.copy())

        return current_x, path_history

    def gauss_newton(self, residual_function, jacobian_function,
                     starting_point, use_line_search=True):
        # For nonlinear least squares problems
        current_x = starting_point.copy()
        path_history = [current_x.copy()]

        for iteration in range(self.max_iterations):
            residuals = residual_function(current_x)
            jacobian_matrix = jacobian_function(current_x)

            # Gradient is J^T * r for least squares
            grad_val = jacobian_matrix.T @ residuals

            if np.linalg.norm(grad_val) < self.tolerance:
                print(f"Gauss-Newton converged at iteration {iteration}")
                break

            # Solve normal equations: (J^T * J) * p = -J^T * r
            try:
                gauss_newton_step = -np.linalg.solve(jacobian_matrix.T @ jacobian_matrix, grad_val)
            except np.linalg.LinAlgError:
                print("Warning: Normal matrix (J^T*J) is singular, falling back to gradient step")
                gauss_newton_step = -grad_val

            if use_line_search:
                # Need to define objective function for line search
                def least_squares_objective(x_val):
                    r_val = residual_function(x_val)
                    return 0.5 * np.dot(r_val, r_val)

                def least_squares_gradient(x_val):
                    J_val = jacobian_function(x_val)
                    r_val = residual_function(x_val)
                    return J_val.T @ r_val

                alpha_step = self._find_good_step_size(least_squares_objective, least_squares_gradient,
                                                       current_x, gauss_newton_step)
            else:
                alpha_step = 1.0

            current_x = current_x + alpha_step * gauss_newton_step
            path_history.append(current_x.copy())

        return current_x, path_history

    def _find_good_step_size(self, objective_func, gradient_func,
                           current_point, search_direction,
                           initial_alpha=1.0, shrink_factor=0.5,
                           armijo_const=1e-4):
        # Backtracking line search with Armijo condition
        func_value = objective_func(current_point)
        grad_value = gradient_func(current_point)
        directional_derivative = np.dot(grad_value, search_direction)

        alpha = initial_alpha
        # Keep shrinking step size until Armijo condition is satisfied
        while objective_func(current_point + alpha * search_direction) > func_value + armijo_const * alpha * directional_derivative:
            alpha *= shrink_factor
            if alpha < 1e-10:  # Prevent infinite loop
                break

        return alpha

# Test function definitions
def get_quadratic_problem():
    # Simple quadratic: x1^2 + 2*x2^2 + x1*x2
    def objective(x):
        return x[0]**2 + 2*x[1]**2 + x[0]*x[1]

    def gradient(x):
        return np.array([2*x[0] + x[1], 4*x[1] + x[0]])

    def hessian(x):
        return np.array([[2, 1], [1, 4]])

    return objective, gradient, hessian

def get_rosenbrock_problem():
    # Classic Rosenbrock function - notoriously tricky!
    def objective(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def gradient(x):
        df_dx1 = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        df_dx2 = 200*(x[1] - x[0]**2)
        return np.array([df_dx1, df_dx2])

    def hessian(x):
        h11 = 2 - 400*x[1] + 1200*x[0]**2
        h12 = -400*x[0]
        h21 = -400*x[0]  # symmetric
        h22 = 200
        return np.array([[h11, h12], [h21, h22]])

    return objective, gradient, hessian

def get_curve_fitting_problem():
    # Exponential decay fitting problem
    data_x = np.array([0, 1, 2, 3, 4])
    data_y = np.array([1.0, 0.5, 0.25, 0.125, 0.0625])  # Perfect exponential decay

    def residuals(params):
        a, b = params
        predicted_y = a * np.exp(b * data_x)
        return predicted_y - data_y

    def jacobian(params):
        a, b = params
        num_points = len(data_x)
        J = np.zeros((num_points, 2))
        exp_terms = np.exp(b * data_x)
        J[:, 0] = exp_terms  # derivative w.r.t. a
        J[:, 1] = a * data_x * exp_terms  # derivative w.r.t. b
        return J

    return residuals, jacobian

if __name__ == "__main__":
    # Let's test all our optimization methods!
    my_optimizer = UnconstrainedOptimizer(tolerance=1e-6, max_iterations=1000)

    print("="*50)
    print("Testing Steepest Descent Method")
    print("="*50)
    obj_func, grad_func, _ = get_quadratic_problem()
    start_point = np.array([2.0, 3.0])
    solution, trajectory = my_optimizer.steepest_descent(obj_func, grad_func, start_point, use_line_search=True)
    print(f"Problem: Simple quadratic function")
    print(f"Started from: {start_point}")
    print(f"Found solution: {solution}")
    print(f"Function value at solution: {obj_func(solution):.8f}")
    print(f"Total iterations: {len(trajectory)-1}")
    print()

    print("="*50)
    print("Testing Newton's Method")
    print("="*50)
    obj_func, grad_func, hess_func = get_rosenbrock_problem()
    start_point = np.array([-1.0, 1.0])
    solution, trajectory = my_optimizer.newton_method(obj_func, grad_func, hess_func, start_point)
    print(f"Problem: Rosenbrock function (the banana function!)")
    print(f"Started from: {start_point}")
    print(f"Found solution: {solution}")
    print(f"Function value at solution: {obj_func(solution):.8f}")
    print(f"Total iterations: {len(trajectory)-1}")
    print()

    print("="*50)
    print("Testing Conjugate Gradient Method")
    print("="*50)
    obj_func, grad_func, _ = get_quadratic_problem()
    start_point = np.array([3.0, -2.0])
    solution, trajectory = my_optimizer.conjugate_gradient(obj_func, grad_func, start_point, cg_method='pr')
    print(f"Problem: Quadratic function again")
    print(f"Started from: {start_point}")
    print(f"Found solution: {solution}")
    print(f"Function value at solution: {obj_func(solution):.8f}")
    print(f"Total iterations: {len(trajectory)-1}")
    print()

    print("="*50)
    print("Testing Gauss-Newton Method")
    print("="*50)
    residual_func, jacobian_func = get_curve_fitting_problem()
    start_params = np.array([1.0, -1.0])
    solution, trajectory = my_optimizer.gauss_newton(residual_func, jacobian_func, start_params)
    print(f"Problem: Exponential curve fitting")
    print(f"Initial guess: a={start_params[0]}, b={start_params[1]}")
    print(f"Fitted parameters: a={solution[0]:.6f}, b={solution[1]:.6f}")
    residual_norm = np.linalg.norm(residual_func(solution))
    print(f"Final residual norm: {residual_norm:.8f}")
    print(f"Total iterations: {len(trajectory)-1}")
