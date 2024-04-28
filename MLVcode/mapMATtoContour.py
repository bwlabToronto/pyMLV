import numpy as np
from scipy.spatial import cKDTree



def getIntersectionTangents(x1, y1, r1, x2, y2, r2):
    d = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    if d==0:
        FX1 = x1
        FY1 = y1
        FX2 = x1
        FY2 = y1
    else:
        r1MinusR2 = r2 - r1
        cosAlpha = r1MinusR2/d
        if abs(cosAlpha) > 1:
            cosAlpha = cosAlpha/abs(cosAlpha)+0.00001
        sinAlpha = np.sqrt(1-cosAlpha**2)
        FX1 = []
        FY1 = []
        FX2 = []
        FY2 = []

        alpha = 0.5
        beta = 1 - alpha
        mx = alpha*x1 + beta*x2
        my = alpha*y1 + beta*y2
        mr = alpha*r1 + beta*r2

        vx = x1 - mx
        vy = y1 - my

        fvx1 = cosAlpha*vx + sinAlpha*vy
        fvy1 = -sinAlpha*vx + cosAlpha*vy

        fvx2 = cosAlpha*vx - sinAlpha*vy
        fvy2 = sinAlpha*vx + cosAlpha*vy

        nv1 = np.sqrt(fvx1**2 + fvy1**2)
        s1 = mr/nv1
        fvx1 = fvx1*s1
        fvy1 = fvy1*s1

        nv2 = np.sqrt(fvx2**2 + fvy2**2)
        s2 = mr/nv2
        fvx2 = fvx2*s2
        fvy2 = fvy2*s2

        fx1 = mx + fvx1
        fy1 = my + fvy1

        fx2 = mx + fvx2
        fy2 = my + fvy2

        nFX1 = np.vstack((FX1, fx1))
        nFY1 = np.vstack((FY1, fy1))
        nFX2 = np.vstack((FX2, fx2))
        nFY2 = np.vstack((FY2, fy2))
        FX1 = nFX1
        FY1 = nFY1
        FX2 = nFX2
        FY2 = nFY2

    return FX1, FY1, FX2, FY2

def getTangentPointsContour(contour, imsize):
    R = contour['Radius']
    X = contour['X']
    Y = contour['Y']
    SKInds = []
    if len(X)>=1:
        FX1 = []
        FX2 = []
        FY1 = []
        FY2 = []

        for i in range(len(X)-1):
            x1 = X[i]
            y1 = Y[i]
            x2 = X[i+1]
            y2 = Y[i+1]
            rv1 = R[i]
            rv2 = R[i+1]

            r1Range = [rv1-0.1, rv1, rv1+0.1]
            r2Range = [rv2-0.1, rv2, rv2+0.1]
            for r1 in r1Range:
                for r2 in r2Range:
                    fx1, fy1, fx2, fy2 = getIntersectionTangents(x1, y1, r1, x2, y2, r2)
                    skIndex = np.ravel_multi_index((x1, y1), imsize)

                    nFX1 = np.vstack((FX1, fx1))
                    nFY1 = np.vstack((FY1, fy1))
                    nFX2 = np.vstack((FX2, fx2))
                    nFY2 = np.vstack((FY2, fy2))
                    FX1 = nFX1
                    FY1 = nFY1
                    FX2 = nFX2
                    FY2 = nFY2
                    nSKInds = np.vstack((SKInds, skIndex))
                    SKInds = nSKInds

        FP1 = np.column_stack((FX1, FY1))
        FP2 = np.column_stack((FX2, FY2))
    else:
        FP1 = []
        FP2 = []

    return FP1, FP2, SKInds



def mapMATtoContour(skeletalBranches, imgLD, skeletonImageWithRating):
    """
    Maps property scores computed on the Medial Axis Transform (MAT) back to a line drawing image.

    This function takes scores computed on the MAT and maps them back to the corresponding contours
    in a line drawing image. If a line drawing contour corresponds to two medial axis branches, the 
    function computes the maximum of the two scores for mapping.

    Args:
        skeletalBranches: Branches traced from the skeleton representation.
        imgLD (numpy.ndarray): The binary line drawing image.
        skeletonImageWithRating (numpy.ndarray): The 2D matrix of the skeleton image with MAT-based scores.

    Returns:
        numpy.ndarray: A binary line drawing image with property scores mapped from the skeleton image 
                       with MAT-based scores.

    Notes:
    - The function is designed to work with properties computed on the Medial Axis Transform (MAT) 
      of a line drawing.
    - If there are two medial axis branches around a line drawing contour, the function chooses the 
      maximum score between the two for mapping.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Morteza Rezanejad
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: Morteza.Rezanejad@gmail.com
    -----------------------------------------------------
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    """
    if imgLD.ndim == 3:
        imgLD = imgLD[:,:,0]

    imsize = imgLD.shape
    imgLDInds = np.where(imgLD == 0)
    contourXY = np.column_stack(imgLDInds)

    contourImageWithRating = np.zeros(imsize)

    for i in range(len(skeletalBranches)):
        cur_contour = skeletalBranches[i] # Verify this
        FP1, FP2, SKInds = getTangentPointsContour(cur_contour, imsize)
        FP = np.vstack((FP1, FP2))
        AllSKInds = np.vstack((SKInds, SKInds))
        neigh_radius = 4
        if len(FP) > 0:
            # Create a KDTree
            tree = cKDTree(FP)
            # Find the nearest neighbors
            D, IDX = tree.query(contourXY, k=1)

            # IDX, D = knnsearch(FP,contourXY) # Verify this
            T = np.where(D < neigh_radius) # Verify this
            if len(T) > 0:
                reconstrucedInds = imgLDInds(T)
                currentScores = contourImageWithRating[reconstrucedInds]
                newScores = skeletonImageWithRating[AllSKInds(IDX(T))]
                contourImageWithRating[reconstrucedInds] = np.maximum(currentScores, newScores)


    return contourImageWithRating

