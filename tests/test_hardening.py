import pytest
import numpy as np
from hardening import EPMaterial

def test_isotropic():
    # Basic test of isotropic stress-strain curve
    strain = [0, 0, 0.0075, 0.03, 0.05, 0]
    dstrain = np.diff(strain)
    E = 1000
    Et = 100
    Y0 = 10
    isomat = EPMaterial(E, Et, 't', Y0, 'i')
    statelist = np.zeros((5, 5))
    for i in range(5):
        isomat.update_state(dstrain[i])
        statelist[i, :] = isomat.return_state()
    
    correct = np.array([
        [0, 0, 0, 10, 0],
        [7.5, 0.0075, 0, 10, 0],
        [12, 0.03, 0.018, 12, 0],
        [14, 0.05, 0.036, 14, 0],
        [-16.2, 0, 0.0558, 16.2, 0]
    ])

    assert np.linalg.norm(correct - statelist) <= 10e-9

def test_kinetic():
    # Basic test of kinetic stress-strain curve
    strain = [0, 0, 0.0075, 0.03, 0.05, 0]
    dstrain = np.diff(strain)

    E = 1000
    Et = 100
    Y0 = 10
    kinmat = EPMaterial(E, Et, 't', Y0, 'k')
    statelist = np.zeros((5, 5))
    for i in range(5):
        kinmat.update_state(dstrain[i])
        statelist[i, :] = kinmat.return_state()

    correct = np.array([
        [0, 0, 0, 10, 0],
        [7.5, 0.0075, 0, 10, 0],
        [12, 0.03, 0.018, 10, 2],
        [14, 0.05, 0.036, 10, 4],
        [-9, 0, 0.063, 10, 1]
    ])

    assert np.linalg.norm(correct - statelist) <= 10e-9

def test_custom():
    # Basic test of custom stress-strain curve
    # This more-so proves it can do it and not that the actual output values are correct.
    strain = [0, 0, 0.0075, 0.03, 0.05, 0]
    dstrain = np.diff(strain)
    def custom(self, state):
        # Calculates changes in strain, stress, and yield center
        dir = np.sign(self.stress - self.alpha)
        dstrain = state/(self.E + self.H)
        dstress = -dir*self.E*dstrain
        dyield = self.H*dstrain/2
        dalpha = dir*self.H*dstrain/2
        # Updates fields in passed class
        self.stress += dstress
        self.pstrain += dstrain
        self.Y0 += dyield
        self.alpha += dalpha
    
    # Defines a material with isotropic hardening
    custommat = EPMaterial(1000, 100, 'T', 10, custom)

    # Defines the state list
    N = len(dstrain)
    statelist = np.zeros((N, 5))

    # Iterates through the changes in strain and outputs the results
    # Iterates through the changes in strain and outputs the results
    for i in range(N):
        custommat.update_state(dstrain[i])
        statelist[i, :] = custommat.return_state()

    correct = np.array([[ 0.00e+00,  0.00e+00,  0.00e+00,  1.00e+01,  0.00e+00],
       [ 7.50e+00,  7.50e-03,  0.00e+00,  1.00e+01,  0.00e+00],
       [ 1.20e+01,  3.00e-02,  1.80e-02,  1.10e+01,  1.00e+00],
       [ 1.40e+01,  5.00e-02,  3.60e-02,  1.20e+01,  2.00e+00],
       [-1.26e+01,  0.00e+00,  5.94e-02,  1.33e+01,  7.00e-01]])
    
    assert np.linalg.norm(correct - statelist) <= 10e-9

def test_plastic():
    # Tests specifying the plastic modulus instead of the tangent modulus
    strain = [0, 0, 0.0075, 0.03, 0.05, 0]
    dstrain = np.diff(strain)
    E = 1000
    Et = 1000/9
    Y0 = 10
    isomat = EPMaterial(E, Et, 'p', Y0, 'i')
    statelist = np.zeros((5, 5))
    for i in range(5):
        isomat.update_state(dstrain[i])
        statelist[i, :] = isomat.return_state()
    
    correct = np.array([
        [0, 0, 0, 10, 0],
        [7.5, 0.0075, 0, 10, 0],
        [12, 0.03, 0.018, 12, 0],
        [14, 0.05, 0.036, 14, 0],
        [-16.2, 0, 0.0558, 16.2, 0]
    ])

    assert np.linalg.norm(correct - statelist) <= 10e-9

def test_modulus_error():
    # Tests inputting an incorrect modulus type
    with pytest.raises(Exception) as exc_info:
        mat = EPMaterial(1000, 100, 'q', 10, 'i')
    
    assert "modulus" in str(exc_info.value)

def test_model_error():
    # Tests specifying an incorrect default model
    with pytest.raises(Exception) as exc_info:
        mat = EPMaterial(1000, 100, 't', 10, 'q')
    
    assert "model" in str(exc_info.value)

def test_print():
    # Tests print representation. I don't know how to access the print statement itself however.
    mat = EPMaterial(1000, 100, 't', 10, 'i')
    print(mat)
    pass