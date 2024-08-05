import numpy as np
import warnings
from computeLength import computeLength

def removeZeroLengthContours(vecLD):
    """
    Removes zero-length contours from a vectorized line drawing.

    This function processes a vectorized line drawing and removes contours that consist of only one pixel, 
    essentially zero-length contours. It returns the updated line drawing and the indices of the contours 
    that were removed.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.

    Returns:
        tuple: A tuple (resultLD, contourIdxRemoved) where:
            resultLD (LineDrawingStructure): The updated line drawing with zero-length contours removed.
            contourIdxRemoved (list): Indices of contours in vecLD that were removed.

    Notes:
    - A zero-length contour is defined as a contour that consists of only one pixel.
    - The function identifies and removes such contours from the provided line drawing.

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
    if 'contourLengths' not in vecLD:
        vecLD = computeLength(vecLD)
    contourIdxRemoved = np.where(vecLD['contourLengths'] == 0)[0] # Verify that this works

    resultLD = {}
    resultLD['originalImage'] = vecLD['originalImage']
    resultLD['imsize'] = vecLD['imsize']
    resultLD['lineMethod'] = vecLD['lineMethod']
    keepIdx = np.where(vecLD['contourLengths'] != 0)[0] # Verify that this works

    resultLD['numContours'] = len(keepIdx)
    resultLD['contours'] = vecLD['contours'][0][keepIdx]


    return resultLD, contourIdxRemoved