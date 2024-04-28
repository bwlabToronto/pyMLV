import numpy as np
import math
import warnings


def lineIntersection(queryLine, refLine, RE = 0.3, AE = 2.0):
    """
    Determines the intersection point, if any, between two line segments.

    Given two line segments represented by their start and end points, and flexibility conditions 
    defined by relative and absolute epsilon values, this function judges whether the two line 
    segments intersect and, if so, returns the coordinates of the intersection point.

    Args:
        queryLine (list or numpy.ndarray): A vector of length 4 representing the first line 
        segment with start and end point coordinates: [X1, Y1, X2, Y2].
        refLine (list or numpy.ndarray): A vector of length 4 representing the second line 
        segment with start and end point coordinates: [X1, Y1, X2, Y2].
        RE (float, optional): The relative epsilon used to judge the intersection of two lines. 
        Default is 0.3.
        AE (float, optional): The absolute epsilon used to judge the intersection of two lines. 
        Default is 2 pixels.

    Returns:
        list or None: The coordinates [x, y] of the intersection point if the lines do intersect. 
        If there is no intersection, returns None.

    Notes:
    - 'RE' (relative epsilon) and 'AE' (absolute epsilon) are thresholds used to determine the 
      intersection under flexible geometric constraints.
    - The function assumes line segments are defined in 2D space.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    eps = 1e-4

    Ay = queryLine[3] - queryLine[1]
    Ax = queryLine[2] - queryLine[0]
    By = refLine[3] - refLine[1]
    Bx = refLine[2] - refLine[0]
    Cy = refLine[0] - queryLine[0]
    Cx = refLine[1] - queryLine[1]

    D = Ay * Bx - Ax * By

    warnings.filterwarnings("ignore", category=RuntimeWarning)  # divide by zero is okay here
    a = (Bx * Cy - By * Cx) / D
    b = (Ax * Cy - Ay * Cx) / D

    at = min(RE, AE / max(abs(Ax), abs(Ay)))  # calculate the threshold of the ratio
    bt = min(RE, AE / max(abs(Bx), abs(By)))  # calculate the threshold of the ratio

    if (-at <= a) and (a <= 1 + at) and (-bt <= b) and (b <= 1 + bt):
        # special cases where a or b are 0 or 1
        if abs(a) < eps:
            Position = queryLine[0:2]
        elif abs(a - 1) < eps:
            Position = queryLine[2:4]
        elif abs(b) < eps:
            Position = refLine[0:2]
        elif abs(b - 1) < eps:
            Position = refLine[2:4]
        else:
            # General case
            A1 = queryLine[1] - queryLine[3]
            B1 = queryLine[2] - queryLine[0]
            C1 = queryLine[0] * queryLine[3] - queryLine[1] * queryLine[2]

            A2 = refLine[1] - refLine[3]
            B2 = refLine[2] - refLine[0]
            C2 = refLine[0] * refLine[3] - refLine[1] * refLine[2]

            D = A1 * B2 - A2 * B1

            Position = np.zeros(2)
            Position[0] = (B1 * C2 - B2 * C1) / D
            Position[1] = (A2 * C1 - A1 * C2) / D
            if any(Position < 0):
                Position = []
    else:
        Position = []

    return Position