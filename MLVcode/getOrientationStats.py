import numpy as np
import matplotlib.pyplot as plt
from MLVcode.computeOrientation import computeOrientation
from MLVcode.computeLength import computeLength

def getOrientationStats(vecLD, numBins=8):
    """
    Computes the orientation histogram of a vectorized line drawing, weighted by segment length.

    This function calculates the histogram of orientations of line segments in a vectorized line 
    drawing (vecLD). The histogram is weighted by the length of each line segment. The number of 
    bins for the histogram can be specified.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        numBins (int, optional): Number of histogram bins. Defaults to 8.

    Returns:
        tuple: A tuple (vecLD, oriHistogram, bins, shortName) where:
            vecLD (LineDrawingStructure): The updated line drawing structure with orientation histogram added.
            oriHistogram (numpy.ndarray): The histogram of orientations of line segments, weighted by their lengths.
            bins (numpy.ndarray): A vector with the bin centers.
            shortName (str): A short name identifier for the histogram, 'ori'.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Check if vecLD's orientation key exists
    if 'orientations' not in vecLD:
        vecLD = computeOrientation(vecLD)
    if 'lengths' not in vecLD:
        vecLD = computeLength(vecLD)


    bwidth = 180/numBins
    bins = np.arange(0, 180, bwidth)
    binEdges = bins + bwidth/2
    # vecLD['orientationHistograms'] = np.zeros((vecLD['numContours'][0][0], numBins))
    # vecLD['normOrientstionHistograms'] = np.zeros((vecLD['numContours'][0][0], numBins))
    vecLD['orientationHistograms'] = np.full((vecLD['numContours'][0][0], numBins), np.nan)
    vecLD['normOrientstionHistograms'] = np.full((vecLD['numContours'][0][0], numBins), np.nan)
    for c in range(vecLD['numContours'][0][0]):
        thisHist = np.zeros(numBins)
        thisCon = vecLD['contours'][0][c]
        numSegments = thisCon.shape[0]

        for s in range(numSegments):
            this_ori = (vecLD['orientations'][c][s] + bwidth / 2) % 180 - bwidth / 2
            # print(c, s, thisOri)
            for b in range(numBins):
                # print(this_ori, binEdges[b])
                if this_ori < binEdges[b]: 
                    thisHist[b] = thisHist[b] + vecLD['lengths'][0][c][s]
                    break


        vecLD['orientationHistograms'][c,:] = thisHist
        vecLD['normOrientstionHistograms'][c,:] = vecLD['orientationHistograms'][c,:] / vecLD['contourLengths'][c] * 10000

    vecLD['sumOrientationHistogram'] = np.sum(vecLD['orientationHistograms'], axis=0)
    vecLD['normSumOrientationHistogram'] = vecLD['sumOrientationHistogram'] / np.sum(vecLD['contourLengths']) * 10000
    oriHistogram = vecLD['sumOrientationHistogram']
    vecLD['orientationBins'] = bins
    shortName = 'ori'
    return vecLD, oriHistogram, bins, shortName