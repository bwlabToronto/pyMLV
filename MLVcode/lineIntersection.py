import numpy as np
import math
import warnings


def lineIntersection(query_line, ref_line, re = 0.3, ae = 2.0):
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
    
    ay = query_line[2] - query_line[0]
    ax = query_line[3] - query_line[1]
    # print("Term1: ", query_line[3], "Term2: ", query_line[1], "Term3: ", ax)
    by = ref_line[2] - ref_line[0]
    bx = ref_line[3] - ref_line[1]
    cy = ref_line[0] - query_line[0]
    cx = ref_line[1] - query_line[1]

    d = ay * bx - ax * by
    
    if d == 0:  # Lines are parallel or coincident
        return None

    a = (bx * cy - by * cx) / d
    b = (ax * cy - ay * cx) / d

    at = min(re, ae / max(abs(ax), abs(ay)))
    bt = min(re, ae / max(abs(bx), abs(by)))

    if (-at <= a <= 1 + at) and (-bt <= b <= 1 + bt):
        # Check for special cases where a or b are 0 or 1
        if abs(a) < eps:
            return np.array(query_line[:2])
        elif abs(a - 1) < eps:
            return np.array(query_line[2:])
        elif abs(b) < eps:
            return np.array(ref_line[:2])
        elif abs(b - 1) < eps:
            return np.array(ref_line[2:])
        else:
            # General case for calculating the intersection
            a1 = query_line[1] - query_line[3]
            b1 = query_line[2] - query_line[0]
            c1 = query_line[0] * query_line[3] - query_line[1] * query_line[2]

            a2 = ref_line[1] - ref_line[3]
            b2 = ref_line[2] - ref_line[0]
            c2 = ref_line[0] * ref_line[3] - ref_line[1] * ref_line[2]

            dd = a1 * b2 - a2 * b1

            x = (b1 * c2 - b2 * c1) / dd
            y = (a2 * c1 - a1 * c2) / dd
            
            return np.array([x, y])
    else:
        return None