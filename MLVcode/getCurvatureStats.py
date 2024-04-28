import numpy as np
from MLVcode.computeCurvature import computeCurvature


def getCurvatureStats(vecLD,
                      numBins=8,
                      minmaxCurvature=[0, 90]):
    """
    Computes the curvature histogram with logarithmically scaled bins, weighted by segment length.

    Input: 
        vecLD - vectorized line drawing
        numBins - number of histogram bins; default: 8
        minmaxCurvature - the minimum and maximum curvature: used as the lower bound of the histogram
                          (default: [0, 90])

    Output:
        vecLD - the line drawing structure with curvature histogram added for each contour
        curvatureHistogram - the histogram of curvature of line segments, 
                              weighted by their lengths
        bins - a vector with the bin centers
        shortName - 'curv'
       
    -----------------------------------------------------
    This file is part of the Mid Level Vision Toolbox: 
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    ------------------------------------------------------
    """
    if 'curvatures' not in vecLD:
        vecLD = computeCurvature(vecLD)
        
    logMinMax = np.log10(np.array(minmaxCurvature)+1)
    binWidth = (logMinMax[1]-logMinMax[0])/numBins # the range of the original length is from max to min length value
    binBoundary = np.arange(logMinMax[0], logMinMax[1]+binWidth, binWidth) # Verify this
    bins = 10 ** (binBoundary[1:]-binWidth/2) - 1


    vecLD['curvatureHistograms'] = np.zeros((vecLD['numContours'][0][0], numBins))
    vecLD['normCurvatureHistograms'] = np.zeros((vecLD['numContours'][0][0], numBins))

    for c in range(vecLD['numContours'][0][0]):
        logCurvatures = np.log10(np.array(vecLD['curvatures'][c])+1)
        # print(logCurvatures)
        if type(logCurvatures) == np.float64:
            logCurvatures = np.array([logCurvatures])
        for s in range(len(logCurvatures)):
            for b in range(numBins):
                if logCurvatures[s] < binBoundary[b+1] or (b == numBins-1):
                    vecLD['curvatureHistograms'][c,b] += vecLD['lengths'][0][c][s]
                    break

        vecLD['normCurvatureHistograms'][c,:] = vecLD['curvatureHistograms'][c,:] / vecLD['contourLengths'][c] * 10000

    vecLD['sumCurvatureHistogram'] = np.sum(vecLD['curvatureHistograms'], axis=0)
    vecLD['normSumCurvatureHistogram'] = vecLD['sumCurvatureHistogram'] / np.sum(vecLD['contourLengths']) * 10000
    curvatureHistogram = vecLD['sumCurvatureHistogram']
    vecLD['curvatureBins'] = bins
    shortName = 'curv'

    return vecLD,curvatureHistogram,bins,shortName