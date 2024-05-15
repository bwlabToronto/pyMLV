import numpy as np
from MLVcode.computeOrientation import computeOrientation
from MLVcode.computeLength import computeLength
# from computeOrientation import computeOrientation

def computeCurvature(vecLD):
    """
    Computes curvature for the contours in the vectorized line drawing vecLD.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.

    Returns:
        LineDrawingStructure: A vector LD of structs with curvature information added.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    if "lengths" not in vecLD:
        # print("No lengths in vecLD")
        vecLD = computeLength(vecLD)
    if "orientations" not in vecLD:
        # print("No orientations in vecLD")
        vecLD = computeOrientation(vecLD)
    # print("vecLD has lengths key: ", len(vecLD['lengths'][0]))


    
    vecLD['curvatures'] = []
    for c in range(vecLD['numContours'][0][0]):
        thisCon = vecLD['contours'][0][c]
        numSegments = thisCon.shape[0]
        vecLD['curvatures'].append([])
        if numSegments == 1:
            vecLD['curvatures'].pop()
            vecLD['curvatures'].append(0) # Special case of only one straight segment
            continue
        for s in range(numSegments):
            if s == numSegments-1:
                s2 = s - 1 # for the last segment, we refer to the previous segment
            else:
                s2 = s + 1 # for all other segments, we refer to the next segment   
            angleDiff = np.abs(vecLD['orientations'][c][s] - vecLD['orientations'][c][s2])
            if angleDiff > 180:
                angleDiff = 360 - angleDiff # For angles > 180, we take the opposite angle
            vecLD['curvatures'][c].append(angleDiff / (vecLD['lengths'][0][c][s]+1e-10)) # Add a small number to avoid division by zero


    return vecLD