import numpy as np
import math
import warnings
from lineIntersection import lineIntersection


def detectJunctions(vecLD, AE=1, RE=0.3):
    """
    Detects any junctions between contours in the vectorized line drawing (vecLD).

    This function identifies junctions between contours based on specified 
    absolute (AE) and relative (RE) epsilon values. Junction detection considers 
    gaps between contours, using the minimum of the two epsilon measures for detection.

    Args:
        vecLD (dict): The vectorized line drawing data structure.
        AE (float, optional): The absolute epsilon for detecting junctions across gaps, 
                              in pixels. Default is 1 pixel.
        RE (float, optional): The relative epsilon for detecting junctions across gaps, 
                              as a fraction of the participating line segment length. 
                              Default is 0.3.

    Returns:
        list of dicts: A list where each element is a dict representing a junction. Each dict 
                       contains the following keys:
                       - 'Position': The [x, y] coordinates of the junction point.
                       - 'contourIDs': A list with the indices of the contours participating 
                                       in this junction (always two for this function's output).
                       - 'segmentIDs': A list with the indices of the line segments within the 
                                       participating contours.

    Notes:
    - This function is a part of junction detection in vectorized line drawings. Further processing 
      might be necessary to refine or clean up the detected junctions.
    - For junction detection, the minimum of AE and RE measures is used.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Function implementation goes here

    # RE (relative epsilon) - the same relative to the lentgh of a segment - the stricter of the two criteria will be applied.
    # AE (absolute epsilon) - to accept two lines as "intersecting" even when they may be seprated by 0 pixels.

    Junctions = {}
    count = 0

    for queryC in range(vecLD['numContours']):
        if vecLD['contourLengths'][queryC] <AE: # if the curve is too short, then don't consider it
            continue

        queryCurve = vecLD['contours'][queryC]
        for queryS in range(len(queryCurve)-1): # loop over the query line segments
            for refC in range(queryC+1, vecLD['numContours']): # we don't consider intersections fo the curve with itself
                if vecLD['contourLengths'][refC] <AE: # if the curve is too short, then don't consider it
                    continue
                refCurve = vecLD['contours'][refC]

                for refS in range(len(refCurve)): # loop over the reference line segments
                    pos = lineIntersection(queryCurve[queryS], refCurve[refS], RE, AE)
                    if pos is not None:
                        count += 1
                        Junctions[count] = {'Position': pos, 'contourIDs': [queryC, refC], 'segmentIDs': [queryS, refS]}

    return Junctions
