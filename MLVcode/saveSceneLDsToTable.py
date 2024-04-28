import numpy as np
import math
import warnings
import pandas as pd
from getContourPropertiesStats import getContourPropertiesStats
# from convertHistogramsToTable import convertHistogramsToTable # To be implemented
from histogramToTable import histogramToTable

def saveSceneLDsToTable(csvFileName):
    """
    Writes the histogram properties of all scene line drawings to a CSV file.

    This function processes vectorized line drawings, computes their statistical properties, 
    and writes these properties to a CSV file. The function returns the data table that was 
    written to the file and the updated vectorized line drawings with their statistics.

    Args:
        csvFileName (str): The file name for the CSV file where the data will be saved.

    Returns:
        tuple: A tuple (resultsTable, statsLD) where:
            resultsTable (pandas.DataFrame): The table that got written to the CSV file.
            statsLD (list or similar structure): Vectorized line drawings with their statistics added.

    Notes:
    - The function is intended for use with a collection of scene line drawings, where each 
      drawing is represented in a vectorized format.
    - The statistical properties are likely based on the histogram properties of these line drawings.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    categories = ['beaches','cities','forests','highways','mountains','offices']
    allLDs = []
    allMaxLen = []
    minCurv = np.nan
    maxCurv = np.nan
    minLen = np.nan
    maxLen = np.nan

    for c in range(len(categories)):
        print(f'\n{categories[c]}\n===============\n')
        path_name = 'vecLD_'+categories[c]+'.npy'
        # print("Path Name: ",path_name)
        vecLD = np.load('vecLD_'+categories[c]+'.npy',allow_pickle=True)
        # print("VecLD: ",vecLD)
        for l in range(len(vecLD)):
            # print(f"{l}. {vecLD[l]['originalImage']}\n")
            imageName = vecLD[l]['originalImage']
            print(f'\t{l}. {imageName}\n')
            thisCurv = np.concatenate(vecLD[l]['curvatures'])
            minCurv = np.nanmin([minCurv,np.nanmin(thisCurv)])
            maxCurv = np.nanmax([maxCurv,np.nanmax(thisCurv)])
            minLen = np.nanmin([minLen,np.nanmin(vecLD[l]['contourLengths'])])
            maxLen = np.nanmax([maxLen,np.nanmax(vecLD[l]['contourLengths'])])
            allMaxLen = np.concatenate([allMaxLen,vecLD[l]['contourLengths']])
        allLDs = np.concatenate([allLDs,vecLD])

    print(f'\nmin/max Length = {minLen} / {maxLen}\n')
    print(f'min/max Curvature = {minCurv} / {maxCurv}\n')

    resultsTable = pd.DataFrame()
    whichStats = ['orientation','horver','length','curvature','junctions']
    junctionTypes = ['Arrow','T','X','Y']

    statsLDs = []
    for l in range(len(allLDs)):
        imageName = allLDs[l]['originalImage']
        #[thisLD,histograms,bins,statsNames] = getContourPropertiesStats(allLDs(l),whichStats,[minLen,maxLen],[minCurv,maxCurv],junctionTypes);
        [thisLD,histograms,bins,statsNames] = getContourPropertiesStats(allLDs[l],whichStats)
        tt = pd.DataFrame({'ImageName':imageName})
        tt = pd.concat([tt,histogramToTable(histograms,bins,statsNames)],axis=1)
        resultsTable = pd.concat([resultsTable,tt],axis=0)
        statsLDs = np.concatenate([statsLDs,thisLD])

    statsLD = statsLDs
    print('\n\n')
    print('\n Results table written to: %s\n',csvFileName)
    print('\n Stats saved in statsLDs\n')

    return resultsTable, statsLD