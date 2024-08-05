import numpy as np

def getMATpropertyStats(vecLD, prop, numBins = 8): # Not using property as a variable name because it is a reserved word in Python
    """
    Computes the histogram for a MAT (Mirror, Asymmetry, Taper) property in a vectorized line drawing.

    This function processes a vectorized line drawing structure and computes a histogram for a specified
    MAT property. The property should already be computed in the vectorized line drawing structure.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing structure with the MAT property already computed.
        property (str): The name of the property, used to read the property from vecLD.
        numBins (int, optional): The number of bins for the histogram. Default is 8.

    Returns:
        tuple: A tuple (vecLD, histogram, bins, shortName) where:
            vecLD (LineDrawingStructure): The updated line drawing structure with property histogram added for each contour.
            histogram (numpy.ndarray): The summary histogram of the property for the entire drawing.
            bins (numpy.ndarray): A vector with the bin centers.
            shortName (str): A shortened name of the property (first 3 letters).

    Notes:
    - This function is typically used in the context of Mirror, Asymmetry, Taper (MAT) properties of line drawings.
    - The histogram provides a statistical summary of the specified property across the entire drawing.

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
    binWidth = 1/numBins
    # bins = np.arange(binWidth, 1, binWidth) - binWidth / 2
    # Create an array of bin edges
    bin_edges = np.linspace(0, 1, numBins + 1)
    # Calculate bin centers
    bins = (bin_edges[:-1] + bin_edges[1:]) / 2
    # print("Bins: ",bins, "\nBin Width: ",binWidth, "\nNum Bins: ",len(bins))
    # Initializing histograms in the vecLD dictionary
    vecLD[prop + 'Bins'] = bins
    vecLD[prop + 'Histograms'] = np.zeros((vecLD['numContours'][0][0], numBins))
    vecLD[prop + 'NormHistograms'] = np.zeros((vecLD['numContours'][0][0], numBins))

    for c in range(vecLD['numContours'][0][0]):
        thisProp = vecLD[prop][0][c]
        thisProp = thisProp[~np.isnan(thisProp)]
        # print("This Prop: ",thisProp, "\nLength of Prop: ",len(thisProp))
        thisHist = np.histogram(thisProp, bins=bin_edges)[0]
        # print("This Hist: ",thisHist, "\nLength of Hist: ",len(thisHist))
        # print("C: ",c)
        # print(vecLD[prop + 'Histograms'].shape)
        vecLD[prop + 'Histograms'][c, :] = thisHist
        vecLD[prop + 'NormHistograms'][c, :] = thisHist / vecLD['contourLengths'][c] * 10000

    hist = np.sum(vecLD[prop + 'Histograms'], axis=0)
    vecLD[prop + 'SumHistogram'] = hist
    vecLD[prop + 'NormSumHistogram'] = hist / np.sum(vecLD['contourLengths']) * 10000
    # Short name for the property
    shortName = prop[:3]

    return vecLD, hist, bins, shortName # Not using histogram as a variable name because it is a reserved word in Python