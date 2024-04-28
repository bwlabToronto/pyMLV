import numpy as np

def getDistanceFromLineSegment(XY):
    """
    Calculates the distance of each point in a set from a line segment.

    This function computes the distance of all points in a given set from the line segment 
    that connects the last point to the first point in the set. The set of points and the 
    line segment are defined in 2D space.

    Args:
        XY (numpy.ndarray): An n x 2 array of xy coordinates, where each row represents 
        a point in 2D space.

    Returns:
        numpy.ndarray: An array of distances, where each element is the distance of the 
        corresponding point in XY from the line segment connecting the first and last points of XY.

    Notes:
    - The line segment is defined by the first and last points in the XY array.
    - The distance is computed for each point in XY to this line segment.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Morteza Rezanejad
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: Morteza.Rezanejad@gmail.com
    -----------------------------------------------------
    """
    if XY.shape[0] <=2:
        d = 0
    else:
        x1 = XY[0,0]
        y1 = XY[0,1]
        x2 = XY[-1,0]
        y2 = XY[-1,1]
        mx = x1-x2
        my = y1-y2
        a = 1
        n = XY.shape[0]
        total_d = 0
        if my !=0:
            b = -mx/my
            c = -(x1+b*y1)

            for i in range(1,n-1):
                x0 = XY[i,0]
                y0 = XY[i,1]
                d = abs(a*x0+b*y0+c)/np.sqrt(a*a+b*b)
                total_d = total_d + d
        else:
            for i in range(1,n-1):
                y0 = XY[i,1]
                total_d = total_d + abs(y0-y1)
        d = total_d/(n-2)
    
    return d


