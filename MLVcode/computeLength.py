import numpy as np

def computeLength(vecLD):
    """
    Computes the length for the contours in the vectorized line drawing vecLD.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.

    Returns:
        LineDrawingStructure: A vector LD of structs with length information added.

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
    vecLD['lengths'] = []
    vecLD['contourLengths'] = []
    for c in range(vecLD['numContours'][0][0]):
        thisCon = vecLD['contours'][0][c]
        val = np.sqrt((thisCon[:,2]-thisCon[:,0])**2+ (thisCon[:,3]-thisCon[:,1])**2)
        vecLD['lengths'].append(np.array(val))
        vecLD['contourLengths'].append([np.sum(val)]) # Need to verify this
    vecLD['contourLengths'] = np.array(vecLD['contourLengths'])
    # print("Contour Len: ", vecLD['contourLengths'])
    # print("Lengths: ", vecLD['lengths'])
    vecLD['lengths'] = [vecLD['lengths']]

    return vecLD