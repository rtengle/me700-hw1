import numpy as np
from numpy import linalg as la
from typing import Callable

def jacobian(f: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps:float=2.22e-16) -> np.ndarray:
    """Computes the Jacobian matrix for a function f(x) based on an input x using the center difference method.

    Args:
        f: Input function f(x). Must accept and return a numpy array.
        x: Input variable x. Must be a numpy array or scalar.
        eps: Machine epsilon of data type in ndarray used to determine distance used. Default is 2.22e-16 corresponding to float64.
    """
    # Converts scalar x into ndarray x
    x = floatarray_convert(x)

    # Sets up difference vector dx and the number of dimenions in x
    dx = np.array(x*np.sqrt(eps))
    Nx = len(x)

    # Determines dimension of output
    f0 = floatarray_convert(f(x))
    Nf = len(f0)

    # Initializes Jacobian matrix J
    J = np.zeros([Nf, Nx])

    # Iterates through x-variables, determining the Jacobian column-by-column
    for i in range(Nx):
        # Isolates difference direction dx to the component x_i
        # Checks to see if x variable is smaller than esp to avoid numerical errors
        dxn = np.zeros(Nx)
        if dx[i] < eps:
            dxn[i] = eps
        else:
            dxn[i] = dx[i]

        # Calculates the partial derivative of x_i and assigns the output to the Jacobian
        J[:, i] = center_difference(f, x, dxn).T

    return J

def center_difference(f: Callable[[np.ndarray], np.ndarray], x: np.ndarray, dx: np.ndarray) -> np.float64:
    """Performs center difference across a function f(x) in the direction dx.

    Args:
        f: Input function f(x). Must accept and return one numpy array.
        x: Location of the center difference. Must be a numpy array.
        dx: Direction array along which the difference takes place. Must be a numpy array.

    """
    # Left and right function values
    a = f(x+dx)
    b = f(x-dx)
    # Returns the center difference result
    return (a-b)/(2*la.norm(dx))

def floatarray_convert(x):
    # Converts any non-ndarray to ndarray
    if type(x) == np.ndarray:
        return x
    else:
        return np.array([x])
    
def floatarray_extract(x):
    # Returns value of single-element ndarray
    if np.shape(x) == (1) or np.shape(x) == (1,):
        return x[0]
    else:
        return x

def newton(f: Callable[[np.ndarray], np.ndarray], x0: np.ndarray, tol:float = 1e-6, maxiter:int = 50, eps=2.22e-16):
    """Finds the value value y = f(x) where norm(y) = 0. 

    Args:
        f: Input function f(x). Input and output must be 1D vectors as ndarray.
        x0: Initial guess for the method.
        tol: Convergence tolerance for bisection method. Default 1e-6, must be positive.
        N (int): Maximum number of loops. Default 50. Must be positive.
        eps: Interval scaling factor used in center difference method. Must be positive.
    
    Returns:
        x: List of guesses
        y: List of values for f(x)
    """

    # Initializes the list of guesses and values. Floatarray_convert is used to handle if the input or output is a scalar
    x = [floatarray_convert(x0)]
    y = [floatarray_convert(f(x0))]

    # Checks tolerance and maxiter for proper ranges
    if tol<=0:
        raise Exception('Tolerance must be positive')
    if maxiter <= 0:
        raise Exception('Maximum number of iterations must be positive')
    if eps <= 0:
        raise Exception('Epsilon parameter must be positive')
    
    # Checks to make sure input and output are 1D
    if len(x[0].shape) > 1:
        raise Exception('Input must be 1D numpy array or scalar')
    if len(y[0].shape) > 1:
        raise Exception('Function output must be 1D numpy array or scalar')
    
    # Gets the number of input and output dimensions
    Nx = len(x[0])
    Nf = len(y[0])
    
    # Checks if input guess is good enough as-is
    if la.norm(y[0]) <= tol:
        return x, y
    
    # Main iterative loop
    for i in range(maxiter):
        # Calculates the Jacobian of the function at the input
        J = jacobian(f, x[i], eps=eps)
        # Performs the relevant generalized inverse as described in the README then appends the change to the guess list
        if Nx == Nf:
            # Square inverse
            x.append(x[i] - la.inv(J) @ y[i])
        elif Nx > Nf:
            # Right inverse
            x.append(x[i] - J.T @ la.inv(J @ J.T) @ y[i])
        else:
            # Left inverse
            x.append(x[i] - la.inv(J.T @ J) @ J.T @ y[i])
        # Appends the result of the guess to the results list
        y.append(floatarray_convert(f(floatarray_extract(x[i+1]))))
        
        # Returns the lists if the tolerance is reached
        if la.norm(y[i+1]) <= tol:
            return x, y

    return x, y

# Basic check for vector -> scalar function
def f(x):
    return np.array([x**4 - np.sin(x), x**5 - x**3 + 2])

x, y = newton(f, 2)
print(x)
print(y)