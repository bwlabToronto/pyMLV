import numpy as np
import pandas as pd
from histogramToTable import histogramToTable

def allLDHistogramsToTable(vecLD, imageFeatures, shortNames):
    """
    Converts histograms described in imageFeatures of a vectorized line drawing (vecLD) into a table.

    This function processes a vectorized line drawing or a collection of such drawings. It extracts 
    histograms for specified features and converts them into a structured table format. The table can have 
    one row for each drawing if used for sum histograms, or as many rows as there are contours in a single 
    drawing if used for individual contour histograms.

    Args:
        vecLD (dict or list of dicts): A vectorized line drawing with statistics for properties already computed.
                                       If vecLD is a list of line drawings, a table with a row for each drawing is created.
        imageFeatures (list of str): Names of the fields in vecLD to be included in the table.
        shortNames (list of str): Short names used to name the columns of the table, corresponding to each feature.

    Returns:
        pandas.DataFrame: A DataFrame representing the histograms as a table. The number of rows depends on whether
                          vecLD represents a single line drawing or a collection of line drawings.

    Notes:
    - The function assumes that `vecLD` and the features specified in `imageFeatures` are structured appropriately.
    - This function is useful for statistical and comparative analysis of properties within vectorized line drawings.

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
    histTable = pd.DataFrame()

    # Deal with the case of a vector of vecLD structures
    if isinstance(vecLD, list) and len(vecLD) > 1:
        tables = [allLDHistogramsToTable(ld, imageFeatures, shortNames) for ld in vecLD]
        return pd.concat(tables, ignore_index=True)
    
    # Process each feature
    for f, feature in enumerate(imageFeatures): # Verify this
        bins = vecLD['junctionTypeBins'] if shortNames[f] == 'juncType' else []
        feature_data = vecLD[feature]
        feature_table = histogramToTable(feature_data, shortNames[f], bins)
        histTable = pd.concat([histTable, feature_table], axis=1)

    return histTable