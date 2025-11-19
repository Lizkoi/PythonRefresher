# Presentation Outline: Unconstrained Optimization Methods

---

### Slide 1: Title Slide

*   **Title:** Implementation of Unconstrained Optimization Methods
*   **Your Name:** [Your Name]
*   **Course:** [Course Name]
*   **Lecturer:** [Lecturer's Name]
*   **Date:** [Date of Presentation]

---

### Slide 2: Introduction & Project Goal

*   **What is Unconstrained Optimization?**
    *   Briefly explain the concept: Finding the minimum of a function without any constraints on the variables.
    *   Mention its importance in fields like machine learning, engineering, and finance.
*   **Project Goal:**
    *   To implement and demonstrate several fundamental unconstrained optimization algorithms in Python.
    *   To understand their strengths, weaknesses, and practical behavior on different types of problems.

---

### Slide 3: Overview of Implemented Algorithms

*   List the four algorithms implemented:
    1.  **Steepest Descent:** The basic gradient-based method.
    2.  **Newton's Method:** A more advanced method using second-order information.
    3.  **Conjugate Gradient:** An iterative method ideal for large-scale problems.
    4.  **Gauss-Newton:** A specialized method for nonlinear least squares.
*   Mention that all are implemented within a single `UnconstrainedOptimizer` class for modularity.

---

### Slide 4: Algorithm 1: Steepest Descent

*   **Core Idea:**
    *   "Go downhill." At each step, move in the direction of the negative gradient.
    *   Show the update formula: `x_{k+1} = x_k - α * ∇f(x_k)`
*   **Key Implementation Detail: Line Search**
    *   Explain why a fixed step size (`α`) can be inefficient.
    *   Introduce the concept of backtracking line search (using the Armijo condition) to find a good step size at each iteration. This is handled by the `_find_good_step_size` method.
*   **Pros & Cons:**
    *   **Pro:** Simple, guaranteed to converge (with proper step size).
    *   **Con:** Can be very slow, especially in "valleys" (exhibits zig-zagging behavior).

---

### Slide 5: Algorithm 2: Newton's Method

*   **Core Idea:**
    *   Use a quadratic model of the function at the current point and jump to the minimum of that model.
    *   Show the update formula: `x_{k+1} = x_k - H(x_k)^{-1} * ∇f(x_k)`
*   **Key Implementation Detail: Handling Singular Hessian**
    *   The Hessian matrix `H(x_k)` might not be invertible (singular).
    *   Explain the fallback mechanism in the code: If `np.linalg.solve` fails, the algorithm uses the steepest descent direction as a backup.
*   **Pros & Cons:**
    *   **Pro:** Very fast convergence (quadratic) near the minimum.
    *   **Con:** Computationally expensive (requires calculating and inverting the Hessian), not guaranteed to converge unless close to the minimum.

---

### Slide 6: Algorithm 3: Conjugate Gradient

*   **Core Idea:**
    *   A clever improvement over steepest descent. It ensures that search directions are "conjugate" to each other, preventing the algorithm from undoing progress made in previous steps.
    *   Ideal for large quadratic problems.
*   **Key Implementation Detail: Fletcher-Reeves vs. Polak-Ribiere**
    *   Explain that the `beta` parameter determines the new search direction.
    *   Show the two formulas implemented (`'fr'` and `'pr'`) and briefly mention that Polak-Ribiere is often more robust for non-quadratic functions.
*   **Pros & Cons:**
    *   **Pro:** Faster than steepest descent, doesn't require storing a Hessian (memory efficient).
    *   **Con:** More complex than steepest descent, convergence theory is based on quadratic functions.

---

### Slide 7: Algorithm 4: Gauss-Newton

*   **Core Idea:**
    *   Specifically for solving **nonlinear least squares** problems (e.g., curve fitting).
    *   The goal is to minimize the sum of squared residuals: `f(x) = 1/2 * Σ r_i(x)^2`
    *   It approximates Newton's method by using `J^T * J` as an approximation for the Hessian, where `J` is the Jacobian of the residuals.
*   **Key Implementation Detail:**
    *   The method takes a `residual_function` and a `jacobian_function` as input, which is different from the other methods.
    *   The line search is performed on the least squares objective function itself.
*   **Pros & Cons:**
    *   **Pro:** Efficient for least squares problems, avoids calculating the full Hessian.
    *   **Con:** Only applicable to least squares problems, can have convergence issues if the initial guess is poor.

---

### Slide 8: Code Structure & Walkthrough

*   **`UnconstrainedOptimizer` Class:**
    *   Show the `__init__` method (tolerance, max_iterations).
    *   Highlight one of the main methods (e.g., `newton_method`) and walk through its logic:
        1.  Start loop and check for convergence (`np.linalg.norm(grad)`).
        2.  Calculate search direction (e.g., `np.linalg.solve(hess, grad)`).
        3.  Use line search to find step length.
        4.  Update the current point `x`.
        5.  Store the history for plotting/analysis.
*   **Test Functions:**
    *   Briefly introduce the test problems:
        *   `get_quadratic_problem()`: A simple, well-behaved problem.
        *   `get_rosenbrock_problem()`: A famous, difficult non-convex problem ("banana function").
        *   `get_curve_fitting_problem()`: A practical example for Gauss-Newton.

---

### Slide 9: Demonstration & Results

*   **Show the output of the script (`if __name__ == "__main__":`)**
*   **Steepest Descent on Quadratic:**
    *   Show the starting point and the final solution. Note how it finds the minimum `(0,0)`.
*   **Newton's Method on Rosenbrock:**
    *   Highlight that this is a hard problem, but Newton's method converges quickly to the known solution `(1,1)`.
*   **Conjugate Gradient on Quadratic:**
    *   Show that it also finds the minimum, likely in fewer iterations than steepest descent would.
*   **Gauss-Newton for Curve Fitting:**
    *   Show the initial parameters and the final fitted parameters (`a` and `b`). Explain that it successfully found the parameters that make the exponential function fit the data.

---

### Slide 10: Conclusion & Summary

*   **Summary of Achievements:**
    *   Successfully implemented four different unconstrained optimization algorithms.
    *   Demonstrated their performance on a variety of test problems.
    *   The code is modular and reusable (`UnconstrainedOptimizer` class).
*   **Key Takeaways:**
    *   There is no "one-size-fits-all" optimizer. The choice depends on the problem structure (e.g., least squares), the cost of computing derivatives (gradient vs. Hessian), and the desired convergence speed.
*   **Possible Future Work:**
    *   Implement Quasi-Newton methods (e.g., BFGS).
    *   Add support for constraints.
    *   Create visualizations of the optimization paths.

---

### Slide 11: Q&A

*   **"Thank you for your attention. Any questions?"**

---
