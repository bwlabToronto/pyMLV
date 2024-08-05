import numpy as np
import warnings

def applyCircularAperture(vecLD,radius=None):
    """
    Clips the contours in a vectorized line drawing at a circular aperture centered at the drawing's center.

    This function applies a circular aperture to a vectorized line drawing, effectively clipping 
    the contours to fit within the specified circular area. The aperture is centered at the center 
    of the line drawing.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        radius (float, optional): The radius of the circular aperture. If not specified, the default 
        is half the minimum dimension of vecLD's image size (min(vecLD.imsize) / 2).

    Returns:
        LineDrawingStructure: The vectorized line drawing with contours clipped to the circular aperture.

    References:
    This procedure was used in the following study:
    Choo, H., & Walther, D. B. (2016). Contour junctions underlie neural representations of scene 
    categories in high-level human visual cortex. Neuroimage, 135, 32-44. 
    https://doi.org/10.1016/j.neuroimage.2016.04.021

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
    if radius is None:
        radius = np.min(vecLD['imsize']) / 2.0

    # Prep the new data structure
    maskedLD = {}
    maskedLD['originalImage'] = vecLD['originalImage'].copy()
    maskedLD['imsize'] = vecLD['imsize'].copy()
    maskedLD['lineMethod'] = vecLD['lineMethod'].copy()
    maskedLD['numContours'] = vecLD['numContours'].copy()*0
    maskedLD['contours'] = np.zeros_like(vecLD['contours'])
    maskedLD['contours'] = [[[] for _ in row] for row in maskedLD['contours']]

    center = np.array(vecLD['imsize']) / 2

    # print("-----------------")
    # print("Original Image: ",maskedLD['originalImage'])
    # print("Image Size: ",maskedLD['imsize'])
    # print("Line Method: ",maskedLD['lineMethod'])
    # print("Number of Contours: ",maskedLD['numContours'])
    # print("Contours: ",maskedLD['contours'])
    # print("Center: ",center, " Radius: ",radius)
    # print("-----------------")

    for c in range(vecLD['numContours'][0][0]):
        # Compute distances of all contour points from the center
        
        A = vecLD['contours'][0][c][:, 0:2]
        A = A.astype(np.float32)
        B = vecLD['contours'][0][c][:, 2:4]
        B = B.astype(np.float64)
        rA = np.sqrt(np.sum((A - center)**2, axis=1))
        rB = np.sqrt(np.sum((B - center)**2, axis=1))

        prevInside = rA[0] <= radius
        # print("Previous Inside: ",prevInside)
        # print("rA: ",np.average(rA), " rB: ",np.average(rB))
        currContour = []
        # for s = 1:size(vecLD.contours{c},1)
        #     currInside = (rB(s) <= radius);
        for s in range(vecLD['contours'][0][c].shape[0]):
            currInside = rB[s] <= radius
            # print("C: ",c," S: ",s," (Current, Previous, XOR): (",currInside, ",",prevInside, ",",currInside ^ prevInside,")")
            # if end points are on different sides, compute the intersection point with the circle
            if currInside ^ prevInside: # Review this
                # Length of segment
                d = np.sqrt(np.sum((B[s, :] - A[s, :])**2))
                if d == 0:
                    warnings.warn('Zero-length segment')
                    # d = np.finfo(float).eps
                # Solve the quadratic equation
                p = -d - (rA[s]**2 - rB[s]**2) / d
                q = rA[s]**2 - radius**2
                QQ = np.sqrt((p / 2)**2 - q)  # Ensure the argument of sqrt is non-negative
                dA1 = -(p / 2) + QQ
                dA2 = -(p / 2) - QQ
                # print("d: ",d," p: ",p," q: ",q," QQ: ",QQ," dA1: ",dA1," dA2: ",dA2)
                # Make sure we pick the right solution
                dA1valid = (0 <= dA1) & (dA1 <= d)
                dA2valid = (0 <= dA2) & (dA2 <= d)
                # print("dA1 Valid: ",dA1valid," dA2 Valid: ",dA2valid)
                if dA1valid:
                    dA = dA1
                    if dA2valid:
                        warnings.warn('Two valid solution - don''t know which one to pick.')
                elif dA2valid:
                    dA = dA2
                else:
                    warnings.warn('No valid solution - don''t know what to do.')
                
                # Compute the intersection point
                # print("______________________")
                # print(np.array(B[s, :] - A[s, :]))
                # print(dA / d)
                # print(np.array(B[s, :]))
                # print(np.array(A[s, :]))
                # print((dA / d) * np.array(B[s, :] - A[s, :]))
                # print(np.array(A[s, :]) + (dA / d) * np.array(B[s, :] - A[s, :]))
                # print("______________________")
                C = np.array(A[s, :]) + (dA / d) * np.array(B[s, :] - A[s, :])
                # print("A: ",A[s, :], " B: ",B[s, :], " C: ",C, " dA: ",dA, " d: ",d)


            # consider all 4 cases
            if prevInside:
                if currInside:
                    # we are completely inside the circle - just keep the segment
                    currContour.append(vecLD['contours'][0][c][s, :])
                else:
                    # going from inside to outside the circle
                    # break the segment and terminate this contour
                    currContour.append([A[s][0], A[s][1], C[0], C[1]])
                    maskedLD['numContours'][0][0] = maskedLD['numContours'][0][0] + 1
                    # print("Masked Num Contours: ",maskedLD['numContours'])
                    maskedLD['contours'][0][maskedLD['numContours'][0][0] - 1] = currContour
                    # print("Masked Contours: ",maskedLD['contours'])
                    currContour = []
            else:
                if currInside:
                    # going from outside to inside the circle
                    # break the segment and start a new contour
                    currContour.append([C[0], C[1], B[s][0], B[s][1]])
                    maskedLD['numContours'][0][0] = maskedLD['numContours'][0][0] + 1
                    # print("Masked Num Contours: ",maskedLD['numContours'])
                    maskedLD['contours'][0][maskedLD['numContours'][0][0] - 1] = currContour
                    # print("Masked Contours: ",maskedLD['contours'])
                    currContour = []
                else:
                    # we are completely outside the circle - just ignore this segment
                    pass
            # print("Changing Previous Inside: ",prevInside, " to Current Inside: ",currInside)
            prevInside = currInside

        # Save the contour if it is not empty
        if len(currContour) > 0:
            maskedLD['numContours'][0][0] = maskedLD['numContours'][0][0] + 1
            maskedLD['contours'][0][maskedLD['numContours'][0][0] - 1] = currContour
        # if maskedLD['numContours'][0][0] > 0:
            # break
    # maskedLD['numContours'][0][0] has a value of 28, but maskedLD['contours'] has a shape of (34,0) so need to remove the empty arrays at the end
    maskedLD['contours'] = [maskedLD['contours'][0][0:maskedLD['numContours'][0][0]]]
    return maskedLD