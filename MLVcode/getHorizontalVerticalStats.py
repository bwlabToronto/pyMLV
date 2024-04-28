import numpy as np
from MLVcode.computeOrientation import computeOrientation
from MLVcode.computeLength import computeLength

def getHorizontalVerticalStats(vecLD,numBins=8):
    """
    Computes the histogram of horizontal-vertical as:
    (abs(cosd(orientation)) - abs(sind(orientation)))
    The histogram is weighted by segment length.

    Input: 
        vecLD - vectorized line drawing
        numBins - number of histogram bins; default: 8

    Output:
        vecLD - the line drawing structure with individual orientation histograms added
        HorVerHistogram - the histogram of orientations of line segments, weighted
                          by their lengths
        bins - a vector with the bin centers
        shortName - 'horver'
       
    -----------------------------------------------------
    This file is part of the Mid Level Vision Toolbox: 
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    ------------------------------------------------------
    """
    if not hasattr(vecLD, 'orientations'):
        vecLD = computeOrientation(vecLD)
    if not hasattr(vecLD, 'lengths'):
        vecLD = computeLength(vecLD)
    
    bwidth = 2/numBins
    binEdges = np.arange(-1+bwidth, 1, bwidth)
    bins = binEdges - bwidth/2
    vecLD['HorVerHistogram'] = np.zeros((vecLD['numContours'][0][0], numBins))

    for c in range(vecLD['numContours'][0][0]):
        thisHist = np.zeros(numBins)
        thisCon = vecLD['contours'][0][c]
        numSegments = thisCon.shape[0]
        for s in range(numSegments):
            thisOri = np.mod(vecLD['orientation'][c][s], 180)
            # thisHV = np.abs(cosd(thisOri)) # Need to write this function
            thisHV = np.abs(np.cos(thisOri)) - np.abs(np.sin(thisOri))
            for b in range(numBins):
                if thisHV < binEdges[b]:
                    thisHist[b] = thisHist[b] + vecLD['lengths'][c][s]
                    break
        vecLD['HorVerHistogram'][c,:] = thisHist
    
    vecLD['sumHorVerHistogram'] = np.sum(vecLD['HorVerHistogram'], axis=0)
    HorVerHistogram = vecLD['sumHorVerHistogram']
    vecLD['HorVerBins'] = bins
    shortName = 'horver'

    
    return vecLD,HorVerHistogram,bins,shortName