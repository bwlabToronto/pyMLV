import numpy as np
import matplotlib.pyplot as plt
from MLVcode.predictContoursByStatsModel import predictContoursByStatsModel
from MLVcode.computeContourProperties import computeContourProperties

def splitLDbyStatsModel(vecLD,Mdl,fraction):
    """
    Splits up the contours in the line drawing vecLD according to a
    pre-trained regression model.

    Parameters:
    - vecLD (dict): Vectorized line drawing to be split. The structure should
                    already contain all relevant feature histograms.
    - Mdl: The pre-trained regression model to apply to contour features
           in order to split the drawing. This could be an instance of a model
           from scikit-learn or any other library.
    - fraction (float): The fraction of pixels to preserve. Only whole contours
                        will be assigned. The splitting is conservative such
                        that at most this fraction of pixels are preserved.

    Returns:
    - topLD (dict): Line drawing structure with the top-ranked contours.
    - bottomLD (dict): Line drawing structure with the bottom-ranked contours.

    Note:
    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox: 
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """

    # compute the predictions for the individual contours
    scores = predictContoursByStatsModel(vecLD,Mdl)

    # rank the scores and split the line drawings
    totalIdx = np.argsort(scores, axis=0)
    sumLen = np.cumsum(vecLD['contourLengths'][0][0][totalIdx]/np.sum(vecLD['contourLengths'][0][0]))
    bottomIdx = totalIdx[sumLen <= fraction]
    topIdx = totalIdx[sumLen >= (1-fraction)]

    bottomLD = {}
    bottomLD['originalImage'] = vecLD['originalImage']
    bottomLD['imsize'] = vecLD['imsize']
    bottomLD['lineMethod'] = '{} - split bottom - {}'.format(vecLD['lineMethod'],fraction)
    bottomLD['numContours'] = len(bottomIdx)
    bottomLD['contours'] = vecLD['contours'][0][0][bottomIdx]
    bottomLD = computeContourProperties(bottomLD)

    topLD = {}
    topLD['originalImage'] = vecLD['originalImage']
    topLD['imsize'] = vecLD['imsize']
    topLD['lineMethod'] = '{} - split top - {}'.format(vecLD['lineMethod'],fraction)
    topLD['numContours'] = len(topIdx)
    topLD['contours'] = vecLD['contours'][0][0][topIdx]
    topLD = computeContourProperties(topLD)

    return topLD, bottomLD
