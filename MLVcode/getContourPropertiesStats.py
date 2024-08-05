import numpy as np
import warnings
from MLVcode.getOrientationStats import getOrientationStats
from MLVcode.getHorizontalVerticalStats import getHorizontalVerticalStats
from MLVcode.getLengthStats import getLengthStats
from MLVcode.getCurvatureStats import getCurvatureStats
from MLVcode.getJunctionStats import getJunctionStats



def getContourPropertiesStats(vecLD, minmaxLen=[], 
                                whichStats=['orientation',
                                                 'length',
                                                 'curvature',
                                                 'junctions'], 
                                minmaxCurv=[],
                                junctionTypes=[]):
    """
    Computes histograms for the contour properties for the vectorized line drawing LD.

    Input:
        vecLD - vectorized line drawing data structure
        whichStats - string or cell array of strings that defines which
                     properties to compute. Options are:
                     'orientation','length','curvature','junctions'
                     default: {'orientation','length','curvature','junctions'}
        minmaxLen - this minimum and maximum for the length histogram 
                    default: [2, width+length of the image]
        minmaxCurv - this minimum and maximum for the curvature histogram 
                     default: [0, 90]
        junctionTypes - a cell array with the junction types to include in the histogram
                        default: {} - use all junction types present in this
                        image

    Output:
        vecLD - vector line drawing with the individual contour stats added
        histograms - cell array of histograms for the features 
                     in the same order as in whichstats
        bins - cell array of bin centers for those histograms
               in the same order as in whichstats
        statsNames - the order of stats in the histograms and bins
       
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
    numBins = 8
    histograms = []
    bins = []
    statsNames = []
    for i in range(len(whichStats)):
        thisStat = whichStats[i].lower()
        if thisStat == 'orientation':
            vecLD, next_hist, next_bins, next_stat = getOrientationStats(vecLD, numBins)
            histograms.append(next_hist)
            bins.append(next_bins)
            statsNames.append(next_stat)
        elif thisStat == 'horver':
            vecLD, next_hist, next_bins, next_stat = getHorizontalVerticalStats(vecLD, numBins)
            histograms.append(next_hist)
            bins.append(next_bins)
            statsNames.append(next_stat)
        elif thisStat == 'length':
            if len(minmaxLen)==0:
                vecLD, next_hist, next_bins, next_stat = getLengthStats(vecLD,
                                                                            numBins)
            else:
                vecLD, next_hist, next_bins, next_stat = getLengthStats(vecLD,
                                                                            numBins,
                                                                            minmaxLen)
            histograms.append(next_hist)
            bins.append(next_bins)
            statsNames.append(next_stat)
        elif thisStat == 'curvature':
            if len(minmaxCurv)==0:
                vecLD, next_hist, next_bins, next_stat = getCurvatureStats(vecLD,
                                                                               numBins)
            else:
                vecLD, next_hist, next_bins, next_stat = getCurvatureStats(vecLD,
                                                                               numBins,
                                                                               minmaxCurv)
            histograms.append(next_hist)
            bins.append(next_bins)
            statsNames.append(next_stat)
        elif thisStat == 'junctions':
            if len(junctionTypes)==0:
                vecLD, jHist, jBins, jNames = getJunctionStats(vecLD, numBins)
            else:
                vecLD, jHist, jBins, jNames = getJunctionStats(vecLD, numBins, junctionTypes)
            histograms.append(jHist)
            bins.append(jBins)
            statsNames.append(jNames)
        else:
            warnings.warn('Unknown property: ' + thisStat)

    return vecLD,histograms,bins,statsNames