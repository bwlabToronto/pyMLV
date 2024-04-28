import numpy as np
# NEEDS TO BE VERIFIED
from getDistanceFromLineSegment import getDistanceFromLineSegment

def fitLineSegments(XY):
    """
    Fits a set of line segments to a sequence of traced XY coordinates.

    This function takes a sequence of XY coordinates and fits line segments to them. It computes 
    the line segments, the distances of each point to the nearest line segment, and a score 
    representing the amount of bending using the number of points in each line segment.

    Args:
        XY (numpy.ndarray): An n x 2 array of xy coordinates, where each row represents 
                            a point in 2D space.

    Returns:
        tuple: A tuple (lineSegs, dists, scores) where:
            lineSegs (list): A list of line segments computed from XY.
            dists (numpy.ndarray): An array of distances from each point in XY to its nearest line segment.
            scores (numpy.ndarray): An array representing the amount of bending, computed using 
                                    the number of points in each line segment.

    Notes:
    - The algorithm for fitting line segments to the XY coordinates is not specified and would 
      need to be implemented.
    - This function is useful for tasks such as simplifying traced outlines or paths by approximating 
      them with a series of straight line segments.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Morteza Rezanejad
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: Morteza.Rezanejad@gmail.com
    -----------------------------------------------------
    """
    counter = 1
    start = 1
    n = XY.shape[0]
    t = start + 2
    threshVal = 1
    toBeRemoved = []
    lineSegs = []
    dists = []
    while t <= n:
        t = start + 2
        stillStraight = True
        while stillStraight:
            segXY = XY[start:t, :]
            d = getDistanceFromLineSegment(segXY)
            if d > threshVal or t >= n:
                stillStraight = False
                if n - t <= 1:
                    t = n + 1

            lineSegs[counter] = XY[start:t, :]
            dists[counter] = d
            toBeRemoved.append(start:t) # TODO: check this
            counter += 1
            start = t - 1
        else:
            t += 1

    scores = np.zeros((1, counter)) # TODO: check this
    counter = 1
    for i in range(len(lineSegs)):
        curLS = lineSegs[i]
        N = curLS.shape[0]
        scores[counter:counter + N-1] = 1-1/N # TODO: check this
        counter += N-1

    return lineSegs, dists, scores


    