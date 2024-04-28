import numpy as np
import cv2
import pandas as pd
import os
import matplotlib.pyplot as plt
from MLVcode.computeContourProperties import computeContourProperties

def splitLDbyProperties(vecLD, properties, fraction=0.5, weights=[]):
    """
    Splits up the contours in the line drawing vecLD according to feature properties.

    Inputs:
        vecLD - Vectorized line drawing to be split. The structure should already contain
                all relevant feature histograms. 
                See also: getContourPropertiesStats

        properties - The property or properties to be considered. These properties are implemented:
                     'Length', 'Orientation', 'Curvature', 'Junctions', 'Random'
                     Properties can either be one of these strings or a list of more than one.
                     If more than one property is included, the rankings according to the properties
                     are linearly combined using weights.
                     Features are ranked as follows:
                       'Length': by total length of contours (sum of the histogram)
                                 topLD: longest; bottomLD: shortest
                       'Curvature': by the average curvature, weighted by segment length
                                    topLD: most angular; bottomLD: most straight
                       'Orientation': weighted by cos - sin of the orientation angle
                                      topLD: most horizontal; bottomLD: most vertical
                       'Junctions': weighted by the total number of junctions
                                    that the contour participates in.
                                    topLD: most junctions; bottomLD: least junctions
                       'Random': a random split of the contours

        fraction - The fraction of pixels to preserve. Default: 0.5
                   Only whole contours will be assigned. The splitting is conservative such
                   that *at most* fraction pixels are preserved. This means that it could happen
                   that one contour in the middle of the distribution does not get assigned to
                   either topLD or bottomLD.

        weights - Array of weights of the same size as properties.
                  Default: [] - all properties are weighted equally, same as ones(1,N)

    Returns:
        topLD - Line drawing structure with the top-ranked contours.
        bottomLD - Line drawing structure with the bottom-ranked contours.

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
    if len(weights) == 0:
        weights = np.ones(len(properties))
    # print("Properties: ",properties)
    # print("Weights: ",weights)
    # print("Fraction: ",fraction)
    totalRank = np.zeros(vecLD['numContours'][0][0])
    for p in range(len(properties)):
        # print(properties[p])
        if properties[p].lower() == 'length':
            thisCriterion = vecLD['contourLengths']
            thisCriterion = thisCriterion.flatten()
            # print("This Criterion: ",thisCriterion)

        elif properties[p].lower() == 'curvature':
            # Compute weighted average curvature
            # thisCriterion = np.array([np.sum(vecLD['curvatures'][c] * vecLD['lengths'][0][c])
            #                       for c in range(vecLD['numContours'][0][0])])
            thisCriterion = np.array([np.sum(vecLD['curvatures'][c] * vecLD['lengths'][0][c])
                                  for c in range(vecLD['numContours'][0][0])], dtype=float)
            # print("This Criterion: ",thisCriterion)
        elif properties[p].lower() == 'orientation':
            thisCriterion = np.array([np.sum((np.abs(np.cos(np.radians(vecLD['orientations'][c]))) - np.abs(np.sin(np.radians(vecLD['orientations'][c])))) * np.array(vecLD['lengths'][0][c]).T) for c in range(len(vecLD['orientations']))])
        elif properties[p].lower() == 'junctions':
            # Just use the sum of all junctions
            thisCriterion = np.sum(vecLD['junctionContourHistograms'], axis=1)
            
        
        elif properties[p].lower() == 'random':
            thisCriterion = np.random.permutation(vecLD['numContours'][0][0])

        else:
            raise ValueError('Unknown property: ' + properties[p])
        # Step 1: Get the indices that would sort the array.
        thisIdx = np.argsort(thisCriterion)
        # Step 2: Rank the elements based on their sorted order. np.arange starts from 0 by default, so we add 1.
        thisRank = np.zeros_like(thisCriterion, dtype=float)
        thisRank[thisIdx] = np.arange(1, len(thisCriterion) + 1)
        # Step 3: Update totalRank with the weighted ranks.
        totalRank += weights[p] * thisRank

    
    # Split by totalRank
    totalIdx = np.argsort(totalRank)
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
    bottomLD['numContours'] = np.array([[len(bottomIdx)]])
    # print("Number of Contours: ",bottomLD['numContours'], " ",vecLD['numContours'])
    bottomLD['contours'] = np.array(vecLD['contours'].flatten()[bottomIdx])
    bottomLD['contours'] = np.array([[np.array(a, dtype=np.float64) for a in bottomLD['contours']]], dtype=object)
    # bottomLD['contours'] = bottomLD['contours'].reshape(-1, 1)
    # print("Contours: \n",bottomLD['contours'], "\n\n\n\n",vecLD['contours'])
    # bottomLD['lengths'] = []
    bottomLD['contourLengths'] = []

    bottomLD = computeContourProperties(bottomLD,whichProps=properties)

    topLD = {}
    topLD['originalImage'] = vecLD['originalImage']
    topLD['imsize'] = vecLD['imsize']
    topLD['lineMethod'] = f"{vecLD['lineMethod'][0]} - split top {fraction}"
    topLD['numContours'] = np.array([[len(topIdx)]])
    topLD['contours'] = np.array(vecLD['contours'].flatten()[topIdx])
    topLD['contours'] = np.array([[np.array(a, dtype=np.float64) for a in topLD['contours']]], dtype=object)
    # From [a, b, c] to [[a], [b], [c]]
    topLD = computeContourProperties(topLD,whichProps=properties)
    # Plot the split line drawings
    # drawLinedrawing(topLD)
    return topLD, bottomLD
    



    

