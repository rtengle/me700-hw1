from bisection import bisection
import pytest

@pytest.mark.timeout(300)

def test_default():
    # Basic test of a window w/ one zero
    a = -2
    b = 5
    def f(x):
        return x*(2**x)
    x0, y0 = bisection(f, a, b)
    assert abs(f(x0[-1])) <= 1e-3

def test_quintic():
    # Test of a window w/ multiple zeros
    a = -2
    b = 3
    def f(x):
        return x**5 - x**4 - 2*x**3 - x**2 + x + 1
    
    x0, y0 = bisection(f, a, b)
    assert abs(f(x0[-1])) <= 1e-3

def test_double_input():
    # Tests checking how many inputs a function can have
    a = -3
    b = 6
    def f(x, y):
        return x + y
    f(2, 3)
    
    with pytest.raises(Exception) as exc_info:
        bisection(f, a, b)

    assert "input" in str(exc_info.value)
    
def test_sign_definite():
    # Tests the bound-checking
    a = 1
    b = 4
    def f(x):
        return x + 3
    
    with pytest.raises(Exception) as exc_info:
        bisection(f, a, b)
    
    assert "Sign" in str(exc_info.value)

def test_bad_bounds():
    # Tests the bound-checking
    a = 4
    b = 1
    def f(x):
        return x - 3
    
    with pytest.raises(Exception) as exc_info:
        bisection(f, a, b)

    assert "a < b" in str(exc_info.value)

def test_neg_tol():
    a = -2
    b = 5
    def f(x):
        return x*(2**x)

    with pytest.raises(Exception) as exc_info:
        x0, y0 = bisection(f, a, b, tol=-2e-3)

    assert "Tolerance" in str(exc_info.value)

def test_neg_maxiter():
    a = -2
    b = 5
    def f(x):
        return x*(2**x)

    with pytest.raises(Exception) as exc_info:
        x0, y0 = bisection(f, a, b, N=-2)

    assert "N must" in str(exc_info.value)
    
def test_step():
    # Tests what happens if there's no zero in the window
    a = -5
    b = 4

    def f(x):
        if x < 0:
            return -1
        else:
            return 1
        
    x0, y0 = bisection(f, a, b)
    pass

def test_autosuccess_a():
    a = -1
    b = 2

    def f(x):
        return x**2 - 1
    x0, y0 = bisection(f, a, b)
    assert x0[-1] == a

def test_autosuccess_b():
    a = -2
    b = 1

    def f(x):
        return x**2 - 1
    x0, y0 = bisection(f, a, b)
    assert x0[-1] == b