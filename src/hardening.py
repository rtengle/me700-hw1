import numpy as np
from typing import Callable

def kinematic(self, state):
    """Plastic deformation model for kinematic hardening that is passed into the EPMaterial object

    Args:
        self: EPMaterial object
        state: Current state variable of the deformation
    """
    # Calculates changes in strain, stress, and yield center
    dir = np.sign(self.stress - self.alpha)
    dstrain = state/(self.E + self.H)
    dstress = -dir*self.E*dstrain
    dalpha = dir*self.H*dstrain
    # Updates fields in passed class
    self.stress += dstress
    self.pstrain += dstrain
    self.alpha += dalpha

def isotropic(self, state):
    """Plastic deformation model for isotropic hardening that is passed into the EPMaterial object

    Args:
        self: EPMaterial object
        state: Current state variable of the deformation
    """
    dstrain = state/(self.E + self.H)
    dstress = -np.sign(self.stress)*self.E*dstrain
    dyield = self.H*dstrain
    self.stress += dstress
    self.pstrain += dstrain
    self.Y0 += dyield


class EPMaterial:
    """Class that defines a elastoplastic material using a plastic hardening model.

    Attributes:
        E: Elastic modulus
        Et: Tangent modulus
        H: Plastic modulus
        Y0: Starting yield strength
        alpha: Current yield strength center
        stress: Current stress
        strain: Current total strain
        pstrain: Current plastic strain

    Methods:
        trial_elastic(strain): returns the elastic stress for a given strain
        update_plastic(state): updates the material due to plastic deformation with a given state
        update_state(strain): updates the material after a given change of strain
        return_state(): returns a tuple of the stress, total strain, plastic strain, yield strength, and yield center
    """

    def __init__(self, E:float, Ep:float, modulustype:str, Y0:float, model: str | Callable, alpha:float=0, stress:float=0, strain:float=0, pstrain:float=0):
        """Constructs elastoplastic material using the specific properties and hardening model

        Args:
            E: Elastic modulus of materia.
            Ep: Modulus for plastic deformation. Can be either the tangent modulus or plastic modulus.
            modulustype: String specifying which type of modulus it is. Can be shorthanded to 't' or 'p' for tangent and plastic modulus respectively.
            Y0: Initial yield strength.
            model: Hardening model of the material. Can be specified as either kinetic or isotropic as a string. A custom function can also be passed instead.
            alpha: Starting yield center. Defaults to 0.
            stress: Starting stress. Defaults to 0.
            strain: Starting total strain. Defaults to 0.
            pstrain: Starting plastic strain. Defaults to 0.
        """
        # Sets initial values
        self.Y0 = Y0
        self.E = E
        self.alpha = alpha
        self.stress = stress
        self.strain = strain
        self.pstrain = pstrain
        # Sets corresponding plastic deformation modulus
        if modulustype == 'T' or modulustype == 't' or modulustype == 'Tangent' or modulustype == 'tangent':
            self.Et = Ep
            self.H = E*Ep/(E-Ep)
        elif modulustype == 'P' or modulustype == 'p' or modulustype == 'Plastic' or modulustype == 'plastic':
            self.H = Ep
            self.Et = E*Ep/(E+Ep)
        else:
            raise Exception('Secondary modulus was not specified as tangent (\'T\') or plastic (\'P\').')
        
        # Specifies specific hardening model
        if model == 'K' or model == 'l' or model == 'Kinematic' or model == 'kinematic':
            self.modelname = 'Kinematic'
            self.deformation_plastic = kinematic
        elif model == 'I' or model == 'i' or model == 'Isotropic' or model == 'isotropic':
            self.modelname = 'Isotropic'
            self.deformation_plastic = isotropic
        else:
            self.modelname = 'Custom'
            self.deformation_plastic = model

    def deformation_elastic(self, strain):
        """Performs stress calculation from a given strain assuming fully elastic deformation.

        Args:
            strain: Given strain.

        Returns:
            stress: Elastic stress for the given strain and specified modulus.
        """
        return self.E*strain
    
    def update_state(self, strain):
        """Updates the state of the system for a given change in total strain.

        Args:
            strain: Change in strain the system undergoes
        """
        # Updates strain and elastic stress
        self.strain += strain
        self.stress += self.deformation_elastic(strain)
        # Checks if we're in the plastic regime
        eta = self.stress - self.alpha
        state = abs(eta) - self.Y0
        # Updates the  
        if state > 0:
            self.deformation_plastic(self, state)

    def __str__(self):
        """Functions that dictates how the object is converted to a string. Mostly used for printouts

        Returns: 
            String representation of the object
        """
        return ("""%s Elasto-Plastic Model
Elastic Module: %f
Tangent Module: %f
Current Stress: %f
Current Total Strain: %f
Current Plastic Strain: %f
Current Yield Strength: %f
Current Yield Center: %f""") % (self.modelname, self.E, self.Et, self.stress, self.strain, self.pstrain, self.Y0, self.alpha)
    
    def return_state(self):
        """Returns a tuple of the relevant state values.

        Returns:
            Tuple of stress values in the following order:
                stress: Current stress
                strain: Current total strain
                pstrain: Current plastic strain
                Y0: Current yield strength
                alpha: Current yield center
        """
        return (self.stress, self.strain, self.pstrain, self.Y0, self.alpha)
