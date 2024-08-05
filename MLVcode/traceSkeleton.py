import numpy as np
import cv2
import matplotlib.pyplot as plt
from GetConSeg import GetConSeg # Need to add

def traceSkeleton(MAT):
    """
    Traces all branches of the Medial Axis Transform (MAT) data structure.

    Parameters:
    - MAT: The given MAT data structure.

    Returns:
    - allBranches: A dictionary that includes all branches computed from MAT.
                   This includes the X and Y position of each branch point as well as the
                   Radius value (radius function) and the average outward flux value (AOF)
                   along each branch.

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
    SegList = GetConSeg(MAT['skeleton'])
    allBranches = []

    for i in range(len(SegList)):
        XY = SegList[i]
        X = XY[:, 0]
        Y = XY[:, 1]
        C = np.ravel_multi_index((Y, X), MAT['skeleton'].shape)

        R = MAT['distance_map'][C]
        F = MAT['AOF'][C]
        branch = {'X': X, 'Y': Y, 'R': R, 'F': F}
        allBranches.append(branch)

    return allBranches