import numpy as np
import matplotlib.pyplot as plt

from MLVcode.segmentContoursAtJunctions import segmentContoursAtJunctions
from MLVcode.computeLength import computeLength

def splitLDmiddleSegmentsVsJunctions(vecLD):
    """
    Divides the contours into middle segments between junctions and the end
    quarters of the segments around junctions.

    Parameters:
    - vecLD: The vectorized line drawing to be split.

    Returns:
    - middleLD: Vectorized line drawing with the middle segments.
    - junctionLD: Vectorized line drawing with segments at the junctions.

    This functionality was utilized in the research:
    John Wilder, Sven Dickinson, Allan Jepson, Dirk B. Walther,
    "Spatial relationships between contours impact rapid scene classification."
    Journal of Vision 2018;18(8):1. doi: https://doi.org/10.1167/18.8.1.

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

    # First, segment the LD at the junctions
    vecLD = segmentContoursAtJunctions(vecLD)

    # Compute lengths for dividing the contours
    vecLD = computeLength(vecLD)

    # Setup the new data structure
    middleLD = {}
    middleLD['originalImage'] = vecLD['originalImage']
    middleLD['imsize'] = vecLD['imsize']
    middleLD['lineMethod'] = vecLD['lineMethod']
    middleLD['numContours'] = 0
    middleLD['contours'] = []
    junctionLD = middleLD

    # Loop over the contours and split them up
    for c in range(len(vecLD['numContours'][0][0])):
        # Skip contours with zero length
        if vecLD['contourLengths'][c] == 0:
            continue

        ll = vecLD['lengths'][c]
        cs = np.cumsum(ll) / np.sum(ll)
        thisC = vecLD['contours'][0][c]

        # First quarter
        seg = np.where(cs < 0.25)[0]
        if seg > 1:
            q1 = thisC[:seg[-1]+1,:] # Verify this
            prevCS = cs[seg[-1]]
        else:
            q1 = []
            prevCS = 0
        
        # Did we happen to get exactly the whole segment?
        if cs[seg] == 0.25:
            q1 = np.concatenate((q1, thisC[seg,:]))
            prevPoint = thisC[seg,0:1]
            prevSeg = seg + 1
        else:
            proportion = (0.25 - prevCS) / (cs[seg] - prevCS)
            thisPoint = (1-proportion) * thisC[seg-1,0:1] + proportion * thisC[seg,2:3]
            q1 = np.concatenate((q1, np.array([np.concatenate((seg[0:1], thisPoint))])))
            prevPoint = thisPoint
            prevSeg = seg

        # Save the first quarter
        junctionLD['numContours'] = junctionLD['numContours'] + 1
        junctionLD['contours'][junctionLD['numContours']-1] = q1

        # Middle Half
        seg = np.where(cs >= 0.75)[0]
        
        if seg == prevSeg:
            # We are still in the same segment
            proportion = (0.75 - prevCS) / (cs[seg] - prevCS)
            currPoint = (1-proportion) * thisC[seg,0:1] + proportion * thisC[seg,2:3]
            q23 = np.array([np.concatenate((prevPoint, currPoint))])
            prevPoint = currPoint
        else:
            # First save the remainder of the previous segment
            q23 = np.array([np.concatenate((prevPoint, thisC[prevSeg,2:3]))])

            # Add any whole segments 
            if seg - prevSeg >= 2:
                q23 = np.concatenate((q23, thisC[prevSeg+1:seg-1,:]))
            
            # Now deal with the portion of the partial segment
            prevCS = cs[seg-1]

            # Did we happen to get exactly the whole segment?
            if cs[seg] == 0.75:
                q23 = np.concatenate((q23, thisC[seg,:]))
                prevPoint = thisC[seg+1,0:1]
                prevSeg = seg + 1
            else:
                proportion = (0.75 - prevCS) / (cs[seg] - prevCS)
                thisPoint = (1-proportion) * thisC[seg-1,0:1] + proportion * thisC[seg,2:3]
                q23 = np.concatenate((q23, np.array([np.concatenate((seg[0:1], thisPoint))])))
                prevPoint = thisPoint
                prevSeg = seg

        # Save the middle half
        middleLD['numContours'] = middleLD['numContours'] + 1
        middleLD['contours'][middleLD['numContours']-1] = q23

        # Now the last quarter
        q4 = np.array([np.concatenate((prevPoint, thisC[prevSeg,2:3]))])

        # Add any full segments that may be left
        if seg < len(cs)-1:
            q4 = np.concatenate((q4, thisC[seg+1:,:]))
        
        # Store the last quarter
        junctionLD['numContours'] = junctionLD['numContours'] + 1
        junctionLD['contours'][junctionLD['numContours']-1] = q4

        # Done with this contour
    return middleLD, junctionLD

# Example usage
# junctionLD['numContours'] = len(junctionLD['contours'])
# middleLD['numContours'] = len(middleLD['contours'])