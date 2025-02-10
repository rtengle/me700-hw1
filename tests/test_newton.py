from newton import newton
import numpy as np
import pytest

@pytest.mark.timeout(300)

def check_outputs(f, x, y, tol=1e-6):
    return np.linalg.norm(f(x[-1])) <= tol and np.linalg.norm(y[-1]) <= tol

def test_scalar_scalar():
    # Basic check for scalar -> scalar function
    def f(x):
       return x**5 - x**3 + 2
    x, y = newton(f, 2)
    assert check_outputs(f, x, y)

def test_scalar_vector():
    # Basic check for scalar -> vector function
    def f(x):
       return np.array([x**2 - 1, x+1])
    
    x, y = newton(f, 2)
    assert check_outputs(f, x, y)

def test_vector_scalar():
    # Basic check for vector -> scalar function
    def f(x):
        return np.linalg.norm(x) - 5
    x, y = newton(f, np.array([3, 5, 3]))
    assert check_outputs(f, x, y)

def test_vector_vector():
    # Basic check for vector -> vector function
    def f(x):
        return x**3
    x, y = newton(f, np.array([3, 5, 3]))
    assert check_outputs(f, x, y)

def test_no_solution():
    # Checks for stopping convergence
    def f(x):
        return x**2 + np.array([1, 1, 1])
    # Need to adjust center difference interval to avoid singular matrix
    x, y = newton(f, np.array([3, 5, 3]), eps=1e-9)
    pass