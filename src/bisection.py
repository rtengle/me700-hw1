import numpy as np
from inspect import signature

def bisection(f, a, b, tol=1e-3, N:int=50):
    """Finds a zero of f(x) within x ∈ [a, b].
    
    Args:
        f: Input function f(x). 1D functions only.
        a: Lower bound of bisection method.
        b: Upper bound of bisection method. Must satisfy sign(f(a)) != sign(f(b)).
        tol: Convergence tolerance for bisection method. Default 1e-3, must be positive.
        N (int): Maximum number of loops. Default 50, must be positive.

    Returns:
        x0: Zero of function f(x)
    """
    validate_input(f, a, b, tol, N)

    # Initializes loop
    A = f(a)
    B = f(b)

    # Checks if a zero is at a or b.
    if A == 0:
        return a
    if B == 0:
        return b
    
    # Actual bisection method.

    for i in range(N):
        # Finds midpoint m and its function value M=f(m)
        m = (a+b)/2
        M = f(m)
        # Checks for convergence
        if abs(M) <= tol:
            print("Converged after %i iterations" % i)
            return m, M
        # Sees if the midpoint should replace a or b
        if np.sign(M) == np.sign(A):
            a = m
            A = M
        else:
            b = m
            B = M
    
    # Failsafe in case of non-convergence.
    print("Maximum number of iterations reached without converging.")
    return m, M
        
            

def validate_input(f, a, b, tol, N):
    """Validates the user inputs to the bisection method function based on the following criteria:

    - Does f(x) only have one argument?
    - Does sign(f(a)) != sign(f(b))
    - Is a < b?
    - Is tol > 0?
    - Is N > 0?

    If it passes all these checks, it returns nothing
    
    Args:
        f: Input function f(x). 1D functions only.
        a: Lower bound of bisection method.
        b: Upper bound of bisection method. Must satisfy sign(f(a)) != sign(f(b)).
        tol: Convergence tolerance for bisection method. Default 1e-3, must be positive.
        N (int): Maximum number of loops. Default 50, must be positive.
    """
    # Checks the number of input arguments using signature(f). Must be done before any calls.
    if len(signature(f).parameters) != 1:
        raise Exception("Function must have exactly one input.")
    # Checks to see if a zero is at either a or b. If so, it returns to the bisection function.
    if f(a) == 0 or f(b) == 0:
        return
    # Checks to see if signs are equivalent
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception("Sign of function the same at f(a) and f(b).")
    # Checks if a < b
    if a >= b:
        raise Exception("The input range must follow a < b.")
    # Checks the tolerancing for the function
    if tol <= 0:
        raise Exception("Tolerance must be a positive non-zero number.")
    # Checks the maximum number of loops
    if N <= 0:
        raise Exception("N must be a positive integer.")
    
    #testing yml