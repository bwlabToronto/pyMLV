import numpy as np
from smoothData import smoothData # Need to add
from diff import diff # Need to add


def getBranchDerivative(branch):
    """
    Calculates the smoothed radius and its derivatives along with the derivatives 
    of the x and y coordinates for a given branch structure.

    This function takes in a branch structure containing radius and coordinate information 
    and computes the derivatives of these quantities. The radius is first smoothed using 
    a moving mean filter before computing the derivatives.

    Args:
        branch (dict): A dictionary containing the following keys:
            - 'Radius' (list or ndarray): The radius values along the branch.
            - 'X' (list or ndarray): The x-coordinates of points along the branch.
            - 'Y' (list or ndarray): The y-coordinates of points along the branch.

    Returns:
        tuple:
            - R (ndarray): The smoothed radius values along the branch.
            - dR (ndarray): The derivative of the radius values.
            - dX (ndarray): The derivative of the x-coordinates.
            - dY (ndarray): The derivative of the y-coordinates.

    Notes:
    - The radius values are smoothed using a moving mean filter with a window size of 3.
    - The `diff` function is used to calculate the differences between consecutive values in the radius, 
      x, and y arrays.
    - For the x and y derivatives, the final value is duplicated to maintain the same length as the input arrays.
    - If the radius array contains only a single value, the derivatives are set to zero.

    Raises:
        KeyError: If the input dictionary does not contain the keys 'Radius', 'X', or 'Y'.
        TypeError: If the values associated with 'Radius', 'X', or 'Y' are not lists or ndarrays.
        
    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Python Implementation: Aravind Narayanan
    Original MATLAB Implementation: Dirk Bernhardt-Walther
    Copyright: Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2024

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    R = branch['Radius']
    R = smoothData(R, 'movemean', 3)

    if len(R)>1:
        X = branch['X']
        Y = branch['Y']
        dX = diff(X)
        dY = diff(Y)
        dR = diff(R)
        
        dX = np.concatenate((dX, [dX[-1]])) # Check
        dY = np.concatenate((dY, [dY[-1]])) # Check

    else:
        dX = 0
        dY = 0
        dR = 0

    return R, dR, dX, dY
