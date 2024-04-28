import numpy as np
from MLVcode.computeLength import computeLength


def getLengthStats(vecLD,
                   numBins=8,
                   minmaxLength=None):
    """
    Computes the length histogram of a vectorized line drawing with logarithmically scaled bins, 
    weighted by segment length.

    This function calculates the histogram of lengths of line segments in a vectorized line 
    drawing (vecLD). The bins for the histogram are logarithmically scaled. The histogram is 
    weighted by the length of each line segment.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        numBins (int, optional): Number of histogram bins. Defaults to 8.
        minmaxLength (list, optional): The minimum and maximum length to be considered for 
        the histogram. The minimum length is used as the lower bound of the histogram.
        Defaults to [2, sum(vecLD.imsize)].

    Returns:
        tuple: A tuple (vecLD, lengthHistogram, bins, shortName) where:
            vecLD (LineDrawingStructure): The updated line drawing structure with length histogram added.
            lengthHistogram (numpy.ndarray): The histogram of lengths of line segments, weighted by their lengths.
            bins (numpy.ndarray): A vector with the bin centers.
            shortName (str): A short name identifier for the histogram, 'len'.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    if 'lengths' not in vecLD:
        vecLD = computeLength(vecLD)

    if minmaxLength is None:
        minmaxLength = [2, np.sum(vecLD['imsize'])]

        
    logMinMax = np.log10(np.array(minmaxLength)+1)
    binWidth = (logMinMax[1]-logMinMax[0])/numBins # the range of the original length is from max to min length value
    binBoundary = np.arange(logMinMax[0], logMinMax[1]+binWidth, binWidth) # Verify this
    bins = 10 ** (binBoundary[1:]-binWidth/2) - 1
    logLengths = np.log10(vecLD['contourLengths']+1)

    vecLD['lengthHistogram'] = np.full((vecLD['numContours'][0][0], numBins), np.nan)
    vecLD['normLengthHistogram'] = np.full((vecLD['numContours'][0][0], numBins), np.nan)
    for c in range(vecLD['numContours'][0][0]):
        thisHist = np.zeros(numBins)
        for b in range(numBins):
            if logLengths[c] < binBoundary[b+1] or (b == numBins-1):
                thisHist[b] = thisHist[b] + vecLD['contourLengths'][c]
                break
            
        vecLD['lengthHistogram'][c,:] = thisHist
        vecLD['normLengthHistogram'][c,:] = thisHist / vecLD['contourLengths'][c] * 10000
    
    vecLD['sumLengthHistogram'] = np.sum(vecLD['lengthHistogram'], axis=0)
    vecLD['normSumLengthHistogram'] = vecLD['sumLengthHistogram'] / np.sum(vecLD['contourLengths']) * 10000
    lengthHistogram = vecLD['sumLengthHistogram']
    vecLD['lengthBins'] = bins
    shortName = 'len'
    return vecLD,lengthHistogram,bins,shortName