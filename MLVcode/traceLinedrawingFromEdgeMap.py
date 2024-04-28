import numpy as np
import cv2
import matplotlib.pyplot as plt
from GetConSeg import GetConSeg # Need to add
from setdiff import setdiff # Need to add
from mergeLineSegments import mergeLineSegments # Need to add

def traceLinedrawingFromEdgeMap(fileName):
    """
    Converts a drawing image (assumed to be a black pencil-like drawing on a white background)
    into a vectorized line drawing data structure.

    Parameters:
    - fileName: Path to the drawing image file.

    Returns:
    - vecLD: Vectorized line drawing data structure.

    Note:
    This function is part of the Mid Level Vision Toolbox: http://www.mlvtoolbox.org

    Copyright:
    Morteza Rezanejad, University of Toronto, Toronto, Ontario, Canada, 2022.

    Contact: Morteza.Rezanejad@gmail.com
    """
    I = cv2.imread(fileName, 0)
    if len(I.shape) > 2:
        I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    imsize = I.shape
    vecLD = {}
    vecLD['originalImage'] = fileName
    vecLD['imsize'] = [imsize[1], imsize[0]]
    vecLD['lineMethod'] = fileName # Need to fix, matlab code is probably wrong

    # Binarize the image
    _, I = cv2.threshold(I, 127, 255, cv2.THRESH_BINARY)[1] # Need to check

    # Bwmorph - thinning
    image = cv2.ximgproc.thinning(I)

    SegList = GetConSeg(image)
    # Find the boundary points where image~=0
    all_boundary_points = np.where(image != 0)

    vecLD['numContours'] = len(SegList)
    vecLD['contours'] = []
    for i in range(len(SegList)):
        contour = SegList[i]

        indices = np.ravel_multi_index((contour[:, 1], contour[:, 0]), image.shape) # Need to fix
        all_boundary_points = setdiff(all_boundary_points, indices) # Need to fix
        Ys = contour[:, 0]
        Xs = contour[:, 1]
        vecLD['contours'].append([Xs[0:-1], Ys[0:-1], Xs[1:], Ys[1:]])

    vecLD = mergeLineSegments(vecLD,1)
    return vecLD
