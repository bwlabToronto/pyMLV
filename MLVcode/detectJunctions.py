import numpy as np
import math
import warnings
from MLVcode.lineIntersection import lineIntersection


def detectJunctions(vec_ld, ae=1, re=0.3):
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

    Python Implementation: Aravind Narayanan
    Original MATLAB Implementation: Dirk Bernhardt-Walther
    Copyright: Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2024

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    junctions = []

    for query_c in range(vec_ld['numContours'][0][0]):
        if vec_ld['contourLengths'][query_c][0] < ae:  # Ignore too short curves
            continue
        
        query_curve = vec_ld['contours'][0][query_c]
        for query_s in range(len(query_curve)):
            for ref_c in range(query_c + 1, vec_ld['numContours'][0][0]):
                if vec_ld['contourLengths'][ref_c][0] < ae:  # Ignore too short curves
                    continue
                
                ref_curve = vec_ld['contours'][0][ref_c]
                
                for ref_s in range(len(ref_curve)):
                    position = lineIntersection(query_curve[query_s].astype(float), ref_curve[ref_s].astype(float), re, ae)
                    
                    if position is not None:
                        junction = {
                            'position': position,
                            'contourIDs': [query_c, ref_c],
                            'segmentIDs': [query_s, ref_s]
                        }
                        junctions.append(junction)
    
    return junctions

