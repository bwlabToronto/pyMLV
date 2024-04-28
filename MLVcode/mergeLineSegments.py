import numpy as np
from getDistanceFromLineSegment import getDistanceFromLineSegment
from computeLength import computeLength
from scipy.spatial import KDTree


def removeDuplicatedContours(vecLD):
    """
    Removes duplicated or overlapping contours from a vectorized line drawing.

    Args:
        vecLD (dict): Vectorized line drawing data structure with a 'contours' key.

    Returns:
        dict: Updated vectorized line drawing data structure with duplicated contours removed.
    """
    tempLD = computeLength(vecLD)
    finalToBeRemoved = []
    for i in range(vecLD['numContours']):
        contour_i = vecLD['contours'][i]
        XY_i = np.vstack((contour_i[:, :2], contour_i[-1, 2:]))
        toBeRemoved = []
        
        for j in range(i + 1, vecLD['numContours']):
            contour_j = vecLD['contours'][j]
            XY_j = np.vstack((contour_j[:, :2], contour_j[-1, 2:]))
            
            tree_i = KDTree(XY_i)
            tree_j = KDTree(XY_j)
            
            d_j, _ = tree_i.query(XY_j)
            d_i, _ = tree_j.query(XY_i)
            d = max(np.max(d_i), np.max(d_j))
            
            if d < 1:
                toBeRemoved.append(j)
                
        if toBeRemoved:
            toBeRemoved.append(i)
            lengths = vecLD['contourLengths'][toBeRemoved]
            maxInd = np.argmax(lengths)
            finalToBeRemoved.extend([x for idx, x in enumerate(toBeRemoved) if idx != maxInd])
    
    # Update vecLD by removing duplicated contours
    vecLD['contours'] = [c for idx, c in enumerate(vecLD['contours']) if idx not in finalToBeRemoved]
    vecLD['numContours'] = len(vecLD['contours'])
    
    return vecLD

   
def mergeLineSegments(vecLD, threshParam):
    """
    Merges nearly collinear line segments within each contour of a vectorized line drawing.
    
    Args:
        vecLD (dict): Vectorized line drawing with contours.
        threshParam (float): Maximum distance threshold for merging line segments.
        
    Returns:
        dict: Updated vectorized line drawing with merged contours.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """

    for cc in range(vecLD['numContours'][0]):
        curContour = vecLD['contours'][cc]
        X = [curContour[:, 0], curContour[:, 2]]
        Y = [curContour[:, 1], curContour[:, 3]]
        XY = np.array([X, Y])

        counter = 1
        start = 1
        n = len(XY[0][0])
        t = start+2
        toBeRemoved = {}
        lineSegs = []
        while t <= n:
            t = start+2
            stillStriaght = True
            while stillStriaght:
                segXY = XY[:, :, start:t] # Verify
                d = getDistanceFromLineSegment(segXY)
                if d > threshParam or t >= n:
                    stillStriaght = False
                    if n - t <= 1:
                        t = n+1
                    lineSegs.append([start, t-1]) # Verify
                    toBeRemoved.append(np.arange(start+1, t-1)) # Verify
                    counter = counter+1
                    start = t - 1
                else:
                    t = t + 1
        
        startXY = np.zeros((len(lineSegs), 2))
        endXY = np.zeros((len(lineSegs), 2))
        for i in range(len(lineSegs)):
            curLineSeg = lineSegs[i]
            startXY[i, :] = curLineSeg[0] # Verify
            endXY[i, :] = curLineSeg[-1] # Verify
        curSeg = [startXY, endXY]
        if len(curSeg) > 1:
            vecLD['contours'][cc] = [startXY, endXY]

        vecLD  = removeDuplicatedContours(vecLD)

    return vecLD


