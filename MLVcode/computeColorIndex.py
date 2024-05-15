import numpy as np
import matplotlib.pyplot as plt
import warnings

def computeColorIndex(vecLD, property):
    """
    Computes a color index for drawing line drawings with their properties.
    Used by drawLinedrawingProperty and drawAllProperties.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing with its properties computed.
        property (str): One of 'length', 'curvature', 'orientation'.

    Returns:
        tuple: A tuple containing:
            - colorIdx (list): A list with one vector per cell, specifying the index into the color map for each line segment.
            - cmap (str): The color map appropriate for this property.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    property = property.lower()
    colorIdx = []
    numCols = 256

    if property == 'length':
        # Log 10 of the length
        allLengths = np.log10(vecLD['contourLengths']+1)
        minProp = np.min(allLengths)
        maxProp = np.max(allLengths)
        col = np.round((allLengths - minProp) / (maxProp - minProp) * (numCols - 1) + 1).astype(int)
        for c in range(vecLD['numContours'][0][0]):
            colorIdx.append(np.zeros(len(vecLD['contours'][0][c])) + col[c])
        cmap = plt.get_cmap('jet', numCols)
    elif property == 'curvature':
        allCurv = []
        rowCurv = []
        for i in range(len(vecLD['curvatures'])):
            val1  = np.squeeze(vecLD['curvatures'][i]).astype(float)
            # print(val1)
            # Check if 0-d array
            if val1.ndim == 0:
                allCurv.append(0.0)
                rowCurv.append(np.array([0.0]))
            else:
                for j in val1:
                    allCurv.append(j)
                rowCurv.append(val1)
        allCurv = np.log10(np.array(allCurv)+1)
        maxProp = np.max(allCurv)*0.8 # Here we're fudging the range a little so that high curvatures are emphasized more
        minProp = np.min(allCurv)
        max_min = maxProp - minProp
        for i in range(vecLD['numContours'][0][0]):
            # curv_log = np.log10(rowCurv[i] + 1)
            # scaled_value = (curv_log - minProp) / (max_min + 1e-10) * 255 + 1
            # colorIdx.append(int(np.minimum(np.round(scaled_value), 256)))
            colorIdx.append(np.minimum(np.round((np.log10(rowCurv[i]+1)-minProp)/(max_min+1e-10)*(255)+1),256))
        cmap = plt.get_cmap('jet', numCols)
    elif property == 'orientation':
        colorIdx = []
        for c in range(vecLD['numContours'][0][0]):
            colorIdx.append(np.round(np.mod(vecLD['orientations'][c], 180) / 180 * (numCols - 1) + 1))
        cmap = plt.get_cmap('hsv', numCols)
    else:
        warnings.warn('Unknown property: ' + property)
        colorIdx = []
        cmap = []
    return colorIdx, cmap