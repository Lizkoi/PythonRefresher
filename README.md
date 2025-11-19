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
