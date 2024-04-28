import numpy as np
from smoothData import smoothData # Need to add
from diff import diff # Need to add


def getBranchDerivative(branch):
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
