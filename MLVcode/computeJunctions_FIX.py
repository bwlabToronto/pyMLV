import numpy as np
from MLVcode.computeOrientation import computeOrientation
from MLVcode.computeLength import computeLength


# To be fixed
def computeJunctions(vecLD):
    """
    Computes all junctions between contours in the vectorized line drawing vecLD.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.

    Returns:
        LineDrawingStructure: A vector LD of structs with junction information added.

    Output Structure:
        Each junction consists of the following information:
        - contourIDs (list): Vector of IDs of contours involved in the junction.
        - segmentIDs (list): Vector of IDs of the segments within these contours.
        - position (list): Location of the junction [x, y].
        - angle (float): Smallest angle of the junction.
        - type (str): Based on the largest angle a, one of: 'T', 'Y', 'X', 'Arrow', 'Star'.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    if not hasattr(vecLD, 'orientations'):
        vecLD = computeOrientation(vecLD)
    if not hasattr(vecLD, 'lengths'):
        vecLD = computeLength(vecLD)
    
    # 3 Step Process

    # 1. Detect any intersections between line segments
    jcts = detectIntersections(vecLD) # Need to write this function

    # 2. Merge Junctions that the close by
    jcts = cleanupJunctions(jcts) # Need to write this function

    # 3. Measure angles and classify junctions
    vecLD['junctions'] = computeJunctionAnglesTypes(jcts, vecLD)    # Need to write this function

    return vecLD
