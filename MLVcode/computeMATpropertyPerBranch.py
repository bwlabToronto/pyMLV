import numpy as np
from getBranchDerivative import getBranchDerivative # Need to add
from fitLineSegments import fitLineSegments # Need to add
from smoothData import smoothData # Need to add
from diff import diff # Need to add

def computeMATpropertyPerBranch(curBranch, prop, K=5):
    """
    Computes the specified MAT property for a particular skeletal branch.

    Parameters:
    - curBranch: The skeletal branch for which the property should be computed.
    - property (str): A string signaling the property that should be computed,
                      one of: 'parallelism', 'separation', 'taper', 'mirror'.
    - K (int, optional): The length of the window on the skeletal branch for computing
                         the property. Default is 5.

    Returns:
    - result: The skeletal branch with the respective scores applied.

    Note:
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

    # Here is the main scoring function --> please note that we originally started with saliency scores based on symmetry and later added separation

    # This does not mean all the scores computed here are just symmetry

    N = len(curBranch['X'])
    R, dR, dX, dY = getBranchDerivative(curBranch)
    result = np.zeros(N)

    if prop == 'parallelism':
        # This is computing the first derivative of the arc length
        skeletalAxisLength = np.cumsum(np.sqrt(dX**2 + dY**2)) # Check if dX, dY was an array or single value
        arcLengthVar = np.cumsum(np.sqrt(dX**2 + dY**2 + dR**2))

        if N >= 3:
            for i in range(1, N-1):
               # Effective K
                eK = min(K, i-1, N-i-1) # Check
                nom = np.sum(skeletalAxisLength[i-eK:i+eK+1])
                denom = np.sum(arcLengthVar[i-eK:i+eK+1])
                result[i] = nom / denom
        
    elif prop == 'separation':
        # This is computing the inverse of the radius function
        result = 1.0 - 1.0/R

    elif prop == 'taper':
        # This is computing the second derivative of the arc length
        dR = smoothData(dR)
        ddR = diff(dR)
        if(len(ddR) >= 1):
            # newddR = np.insert(ddR, 0, ddR[0]) # Need to fix this
            newddR = np.append(newddR, ddR[-1])
        else:
            newddR = dR
        ddT = newddR
        ddR = smoothData(ddR)

        skeletalAxisLength = np.cumsum(np.sqrt(dX**2 + dY**2))
        arcLengthVar = np.cumsum(np.sqrt(dX**2 + dY**2 + dR**2))

        if N >= 3:
            for i in range(1, N-1):
                eK = min(K, i-1, N-i-1)
                nom = np.sum(skeletalAxisLength[i-eK:i+eK+1])
                denom = np.sum(arcLengthVar[i-eK:i+eK+1])
                result[i] = nom / denom

    elif prop == 'mirror':
        # Computing curvature of the medial axis
        X = curBranch['X']
        Y = curBranch['Y']
        if len(X) >= 3:
            result = fitLineSegments([X, Y])
    else:
        raise ValueError('Unknown property: ' + prop)
    
    result = smoothData(result, 'movemean', 3)
    result = np.power(result, 10)

    return result


