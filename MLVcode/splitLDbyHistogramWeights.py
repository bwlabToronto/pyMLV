import numpy as np
import matplotlib.pyplot as plt
from MLVcode.computeContourProperties import computeContourProperties

def splitLDbyHistogramWeights(vecLD,properties,fraction,histogramWeights):
    """
    Splits up the contours in the line drawing vecLD according to feature
    properties, weighted by the histogramWeights.

    Parameters:
    - vecLD (dict): Vectorized line drawing to be split. The structure should
      already contain all relevant feature histograms. See also: getContourPropertiesStats.
    - properties (list of str): The property or properties to be considered.
      Implemented properties include 'Length', 'Orientation', 'Curvature', 'Junctions'.
      Properties can either be one of these strings or a list of more than one.
      If more than one property is included, the rankings according to the properties
      are linearly combined using weights.
    - fraction (float): The fraction of pixels to preserve. Only whole contours will
      be assigned. The splitting is conservative such that *at most* this fraction
      of pixels are preserved. This means that it could happen that one contour
      in the middle of the distribution does not get assigned to either topLD or bottomLD.
    - histogramWeights (list of lists): A list of weight vectors corresponding to each
      property in `properties`, used for weighting the histograms for each property.
      The histograms are weighted and summed according to these weight vectors, then
      combined and ranked.

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
    if not isinstance(properties, list):
        properties = [properties]
    
    totalScore = np.zeros(vecLD['numContours'][0][0])
    for p in range(len(properties)):
        weights = np.array(histogramWeights[p])
        if properties[p].lower() == 'length':
            thisScore = np.sum(vecLD['lengthHistograms'][0][0] * weights.reshape(1, -1), axis=1, keepdims=True)
        elif properties[p].lower() == 'curvature':
            thisScore = np.sum(vecLD['curvatureHistograms'][0][0] * weights.reshape(1, -1), axis=1, keepdims=True)
        elif properties[p].lower() == 'orientation':
            thisScore = np.sum(vecLD['orientationHistograms'][0][0] * weights.reshape(1, -1), axis=1, keepdims=True)
        elif properties[p].lower() == 'junctions':
            thisScore = np.sum(vecLD['junctionContourHistograms'][0][0] * weights.reshape(1, -1), axis=1, keepdims=True)
        else:
            raise ValueError('Error: Unknown property')
        totalScore += thisScore

    # Split by totalRank
    totalIdx = np.argsort(totalScore.flatten())
    # Step 2: Calculate the cumulative sum of normalized contour lengths.
    normalized_lengths = np.cumsum(vecLD['contourLengths'].flatten()[totalIdx]) / np.sum(vecLD['contourLengths'].flatten())
    # Step 3: Get indices for bottom and top based on the fraction.
    bottomIdx = totalIdx[normalized_lengths <= fraction]
    topIdx = totalIdx[normalized_lengths >= (1 - fraction)]

    bottomLD = {}
    bottomLD['originalImage'] = vecLD['originalImage']
    # print("Original Image: ",bottomLD['originalImage'], " ",vecLD['originalImage'])
    bottomLD['imsize'] = vecLD['imsize']
    # print("Image Size: ",bottomLD['imsize'], " ",vecLD['imsize'])
    bottomLD['lineMethod'] = [f"{vecLD['lineMethod'][0]} - split bottom {fraction}"]
    # print("Line Method: ",bottomLD['lineMethod'], " ",vecLD['lineMethod'])
    bottomLD['numContours'] = np.array([[len(bottomIdx)]]).astype(np.uint8)
    # print("Number of Contours: ",bottomLD['numContours'], " ",vecLD['numContours'])
    bottomLD['contours'] = np.array(vecLD['contours'].flatten()[bottomIdx])
    bottomLD['contours'] = np.array([[np.array(a, dtype=np.float64) for a in bottomLD['contours']]], dtype=object)
    # bottomLD['contours'] = bottomLD['contours'].reshape(-1, 1)
    # print("Contours: \n",bottomLD['contours'], "\n\n\n\n",vecLD['contours'])
    bottomLD['lengths'] = []
    bottomLD['contourLengths'] = []
    bottomLD = computeContourProperties(bottomLD,whichProps=properties)

    topLD = {}
    topLD['originalImage'] = vecLD['originalImage']
    topLD['imsize'] = vecLD['imsize']
    topLD['lineMethod'] = f"{vecLD['lineMethod'][0]} - split top {fraction}"
    topLD['numContours'] = np.array([[len(topIdx)]]).astype(np.uint8)
    topLD['contours'] = np.array(vecLD['contours'].flatten()[topIdx])
    topLD['contours'] = np.array([[np.array(a, dtype=np.float64) for a in topLD['contours']]], dtype=object)
    # From [a, b, c] to [[a], [b], [c]]
    # topLD['contours'] = topLD['contours'].reshape(-1, 1)
    topLD = computeContourProperties(topLD,whichProps=properties)

    return topLD, bottomLD