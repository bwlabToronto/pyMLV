import numpy as np
def rotateLinedrawing(vecLD, angle):
    """
    Rotates the contours in a vectorized line drawing by a specified angle.

    This function applies a rotation transformation to all contours in a vectorized 
    line drawing. The rotation is performed based on a given angle in degrees.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        angle (float): The rotation angle in degrees. Range: 0 - 360.

    Returns:
        LineDrawingStructure: The rotated vectorized line drawing with transformed contours.

    References:
    This procedure was used in the following study:
    Choo, H., & Walther, D. B. (2016). Contour junctions underlie neural 
    representations of scene categories in high-level human visual cortex. 
    Neuroimage, 135, 32-44. https://doi.org/10.1016/j.neuroimage.2016.04.021

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    rotateLinedrawing = {}
    rotateLinedrawing['originalImage'] = vecLD['originalImage'].copy()
    rotateLinedrawing['imsize'] = vecLD['imsize'].copy()
    rotateLinedrawing['lineMethod'] = vecLD['lineMethod'].copy()
    rotateLinedrawing['numContours'] = vecLD['numContours'].copy()
    rotateLinedrawing['contours'] = vecLD['contours'].copy()

    centerPoint = np.array([rotateLinedrawing['imsize'][0][0],
                            rotateLinedrawing['imsize'][0][1],
                            rotateLinedrawing['imsize'][0][0],
                            rotateLinedrawing['imsize'][0][1]]) / 2
    
    sinAngle = np.sin(np.deg2rad(angle))
    cosAngle = np.cos(np.deg2rad(angle)) 
    # Roun off the values to 5 decimal places
    sinAngle = round(sinAngle, 5)
    cosAngle = round(cosAngle, 5)

    
    for c in range(rotateLinedrawing['numContours'][0][0]):
        offset = np.tile(centerPoint,(rotateLinedrawing['contours'][0][c].shape[0],1))

        con = rotateLinedrawing['contours'][0][c] - offset
        rot = np.zeros(con.shape)
        rot[:,0] = cosAngle * con[:,0] - sinAngle * con[:,1]
        rot[:,1] = sinAngle * con[:,0] + cosAngle * con[:,1]
        rot[:,2] = cosAngle * con[:,2] - sinAngle * con[:,3]
        rot[:,3] = sinAngle * con[:,2] + cosAngle * con[:,3]
        rotateLinedrawing['contours'][0][c] = rot + offset

    return rotateLinedrawing


