# Unconstrained Optimization Methods

## Overview

This project provides a Python implementation of several unconstrained optimization algorithms. The `UnconstrainedOptimizer` class includes methods for Steepest Descent, Newton's Method, Conjugate Gradient, and the Gauss-Newton method for nonlinear least squares problems. The script also includes a set of test functions to demonstrate the usage and effectiveness of these algorithms.

## Implemented Algorithms

### 1. Steepest Descent

This is a first-order optimization algorithm that iteratively moves in the direction of the negative gradient of the objective function. It's simple to implement but can be slow to converge, especially in narrow valleys. The implementation includes an optional backtracking line search to find an appropriate step size.

### 2. Newton's Method

This is a second-order optimization algorithm that uses the Hessian matrix to find the optimal direction and step size. It converges much faster than Steepest Descent but requires the computation of the Hessian matrix, which can be computationally expensive. The implementation includes a fallback to the steepest descent direction if the Hessian is singular.

### 3. Conjugate Gradient

This algorithm is an improvement over Steepest Descent that avoids the zigzagging behavior often observed with that method. It uses a series of conjugate directions to find the minimum of a quadratic function in at most *n* steps, where *n* is the number of dimensions. The implementation includes both the Fletcher-Reeves and Polak-Ribiere methods for calculating the conjugate direction.

### 4. Gauss-Newton Method

This is an algorithm for solving nonlinear least squares problems. It's an approximation of Newton's method that avoids the need to compute the full Hessian matrix. Instead, it uses the Jacobian of the residual function to approximate the Hessian.

## How to Run

To run the script and see the test results, you will need to have Python and the `numpy` library installed.

1.  **Install `numpy`:**
    ```bash
    pip install numpy
    ```
2.  **Run the script:**
    ```bash
    python3 optimization_methods.py
    ```

The script will then execute the test functions and print the results to the console.

## Dependencies

*   Python 3.x
*   NumPy

## Code Structure

*   `optimization_methods.py`: This file contains the `UnconstrainedOptimizer` class, the implemented optimization algorithms, and the test functions.

## Detailed Code Explanation

### `UnconstrainedOptimizer` Class

This class encapsulates all the optimization algorithms.

#### `__init__(self, tolerance=1e-6, max_iterations=1000)`

*   **Purpose:** Initializes the optimizer with settings that control its behavior.
*   `self.tolerance`: A small number that determines when the algorithm has converged. Convergence is declared when the norm of the gradient is less than this value.
*   `self.max_iterations`: A safety measure to prevent the algorithm from running indefinitely.

#### `steepest_descent(...)`

*   **Purpose:** Implements the steepest descent algorithm.
*   `current_x = starting_point.copy()`: Creates a local copy of the starting point to avoid modifying the original array.
*   `path_history = [current_x.copy()]`: Stores the sequence of points visited by the algorithm, which is useful for visualizing the optimization path.
*   `while iteration_count < self.max_iterations:`: The main loop of the algorithm.
*   `grad = gradient_func(current_x)`: Computes the gradient of the objective function at the current point.
*   `if np.linalg.norm(grad) < self.tolerance:`: Checks for convergence.
*   `if use_line_search:`: Decides whether to use a fixed step size or a more sophisticated line search.
*   `alpha = self._find_good_step_size(...)`: Calls the line search helper method.
*   `current_x = current_x - alpha * grad`: Takes a step in the direction of the negative gradient.

#### `newton_method(...)`

*   **Purpose:** Implements Newton's method.
*   `hess = hessian_func(current_x)`: Computes the Hessian matrix at the current point.
*   `try...except np.linalg.LinAlgError`: This block handles cases where the Hessian matrix is singular (i.e., not invertible).
*   `newton_direction = -np.linalg.solve(hess, grad)`: Solves the linear system `H * p = -g` to find the Newton direction `p`. This is more numerically stable than computing the inverse of the Hessian directly.
*   `newton_direction = -grad`: If the Hessian is singular, the algorithm falls back to using the steepest descent direction.
*   `step_length = 1.0`: For a pure Newton's method, the step length is typically 1.

#### `conjugate_gradient(...)`

*   **Purpose:** Implements the conjugate gradient method.
*   `search_direction = -current_grad`: The first search direction is always the steepest descent direction.
*   `next_grad = gradient_func(next_x)`: Computes the gradient at the *next* point.
*   `beta_value = ...`: Calculates the `beta` value, which is used to combine the new gradient with the previous search direction to form a new, conjugate search direction.
*   `if cg_method.lower() == 'fr'`: Implements the Fletcher-Reeves formula for `beta`.
*   `elif cg_method.lower() == 'pr'`: Implements the Polak-Ribiere formula.
*   `search_direction = -next_grad + beta_value * search_direction`: Updates the search direction.

#### `gauss_newton(...)`

*   **Purpose:** Implements the Gauss-Newton method for nonlinear least squares.
*   `residuals = residual_function(current_x)`: Computes the vector of residuals.
*   `jacobian_matrix = jacobian_function(current_x)`: Computes the Jacobian matrix.
*   `grad_val = jacobian_matrix.T @ residuals`: In least squares, the gradient is `J^T * r`.
*   `gauss_newton_step = -np.linalg.solve(jacobian_matrix.T @ jacobian_matrix, grad_val)`: Solves the normal equations `(J^T * J) * p = -J^T * r` to find the search direction `p`. `J^T * J` is the approximation of the Hessian.
*   `least_squares_objective` and `least_squares_gradient`: These inner functions are defined so that the `_find_good_step_size` method can be reused.

#### `_find_good_step_size(...)`

*   **Purpose:** Implements a backtracking line search with the Armijo condition.
*   `directional_derivative = np.dot(grad_value, search_direction)`: Computes the derivative of the objective function in the search direction.
*   `while objective_func(...) > func_value + armijo_const * alpha * directional_derivative`: This is the Armijo condition. It ensures that the step size `alpha` leads to a sufficient decrease in the objective function.
*   `alpha *= shrink_factor`: If the condition is not met, the step size is reduced.

### Test Functions

These functions define mathematical problems used to test the optimizers.

#### `get_quadratic_problem()`

*   **Purpose:** Defines a simple quadratic function. Optimization algorithms are often first tested on quadratic functions because their behavior is well-understood. The minimum of this function is at `(0, 0)`.

#### `get_rosenbrock_problem()`

*   **Purpose:** Defines the Rosenbrock function, a famous and challenging test problem for optimization algorithms. It has a narrow, curved valley, which can be difficult for algorithms like steepest descent to navigate. The minimum is at `(1, 1)`.

#### `get_curve_fitting_problem()`

*   **Purpose:** Defines a nonlinear least squares problem.
*   `data_x`, `data_y`: The data points to be fitted.
*   `residuals(params)`: Calculates the difference between the model's predictions and the actual data.
*   `jacobian(params)`: Calculates the matrix of first-order partial derivatives of the residuals with respect to the parameters `a` and `b`.

### Main Execution Block (`if __name__ == "__main__":`)

*   **Purpose:** This block demonstrates how to use the `UnconstrainedOptimizer` class.
*   It initializes the optimizer, sets up each test problem, calls the relevant optimization method, and prints the results. This makes the script a self-contained example.
