import numpy as np

def computeOrientation(vecLD):
    """
    Computes orientations for the contours in the vectorized line drawing vecLD.
    
    Note that this function computes orientations from 0 to 360 degrees.
    To obtain orientation from 0 to 180, use mod(ori, 180).

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.

    Returns:
        LineDrawingStructure: A vector LD of structs with orientation information added.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright (c) 2022 Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    vecLD['orientations'] = []
    for c in range(vecLD['numContours'][0][0]):
        thisCon = vecLD['contours'][0][c]
        ori = np.mod(np.degrees(np.arctan2(thisCon[:,1].astype(np.int32) - thisCon[:,3].astype(np.int32), 
                                           thisCon[:,2].astype(np.int32) - thisCon[:,0].astype(np.int32))), 360)
        vecLD['orientations'].append(ori)
    return vecLD