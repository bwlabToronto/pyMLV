import numpy as np
from MLVcode.computeJunctions import computeJunctions


def getJunctionStats(vecLD,
                     numAngleBins = 8,
                     junctionTypes = ['T', 'Y', 'X', 'Arrow', 'Star']):
    """
    Computes the histograms for junction types and junction angles.

    Input:
        vecLD - vectorized line drawing
        numAngleBins - the number of bins for the junction angle histogram
                       default: 8
        junctionTypes - which types of junctions to include
                        default: {'T', 'Y', 'X', 'Arrow', 'Star'}

    Return:
        vecLD - vectorized line drawing with the junction histograms added
        histograms - the histograms of junction types and junction angles, 
                     weighted by their lengths
        bins - a vector with the bin centers
        shortNames - {'juncType', 'juncAngle'}
       
    -----------------------------------------------------
    This file is part of the Mid Level Vision Toolbox: 
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    ------------------------------------------------------
    """
    # Need to fix the junction angles
    if 'junctions' not in vecLD:
        vecLD = computeJunctions(vecLD)

    if len(vecLD['junctions']) == 0:
        vecLD['junctionContourHistograms'] = np.zeros((vecLD['numContours'][0][0],
                                                       len(junctionTypes)))
        vecLD['normJuctionContourHistograms'] = np.zeros((vecLD['numContours'][0][0],
                                                                len(junctionTypes)))
        vecLD['junctionTypeHistogram'] = np.zeros(len(junctionTypes))
        vecLD['normJunctionTypeHistogram'] = np.zeros(len(junctionTypes))
    else:
        these_types = [j['type'] for j in vecLD['junctions']]
        type_hist = np.zeros(len(junctionTypes))
        vecLD['junctionContourHistograms'] = np.zeros((vecLD['numContours'][0][0],
                                                         len(junctionTypes)))
        for t, jt in enumerate(junctionTypes):
            this_j = []
            for j_type in these_types:
                if j_type == jt:
                    this_j.append(1)
                else:
                    this_j.append(0)
            
            type_hist[t] = np.sum(this_j)
            contours = []
            for i in range(len(vecLD['junctions'])):
                if this_j[i] == 1:
                    contours.append(vecLD['junctions'][i]['contourIDs'])
            contours = [item for sublist in contours for item in sublist]
            for c in np.unique(contours):
                vecLD['junctionContourHistograms'][c-1,t] = np.sum(np.array(contours) == c)
            vecLD['normJunctionContourHistograms'] = (
                vecLD['junctionContourHistograms'] / np.tile(vecLD['contourLengths'], (len(junctionTypes))) * 10000
            )
            vecLD['junctionTypeHistogram'] = type_hist
            vecLD['normJunctionTypeHistogram'] = type_hist / np.sum(vecLD['contourLengths']) * 10000

    vecLD['junctionTypeBins'] = junctionTypes

    # Junction Angles
    maxAngle = 120
    binStep = maxAngle / numAngleBins
    angleBins = np.arange(binStep/2, maxAngle, binStep)
    if len(vecLD['junctions']) == 0:
        # print("IF")
        vecLD['junctionAngleHistogram'] = np.zeros(len(junctionTypes))
        vecLD['normJunctionAngleHistogram'] = np.zeros(len(junctionTypes))
        histograms = [np.array([]), np.array([])]
    else:
        # print("ELSE")
        angles = []
        for i in range(len(vecLD['junctions'])):
            angles.append(vecLD['junctions'][i]['minAngle'])
        # angles = vecLD['junctions']['minAngle'][0]
        angleHist, _ = np.histogram(angles, bins=angleBins)
        vecLD['junctionAngleHistogram'] = angleHist
        vecLD['normJunctionAngleHistogram'] = angleHist / np.sum(vecLD['contourLengths']) * 10000
        histograms = [type_hist, angleHist]

    vecLD['junctionAngleBins'] = angleBins

    bins = [junctionTypes, angleBins]
    shortNames = ['juncType', 'juncAngle']

    return vecLD, histograms, bins, shortNames