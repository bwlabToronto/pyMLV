import numpy as np
from scipy.spatial import KDTree

def recursiveClasses(J, mergeMatrix, isJunctionAvailable):
    if isJunctionAvailable[J]:
        allJs = J
        isJunctionAvailable[J] = False
    else:
        allJs = []
        return allJs, mergeMatrix, isJunctionAvailable

    newJs = np.where(mergeMatrix[J, :])[0] # Verify
    mergeMatrix[J, :] = False
    mergeMatrix[:, J] = False
    for j in range(len(newJs)):
        thisJs, mergeMatrix, isJunctionAvailable = recursiveClasses(newJs[j], mergeMatrix, isJunctionAvailable)
        isJunctionAvailable[thisJs] = False
        allJs = np.concatenate((allJs, thisJs))
    
    return allJs, mergeMatrix, isJunctionAvailable

def cleanupJunctions(Junctions, Thresh=2):
    """
    Cleans up junctions by merging junctions that are within Thresh pixels of each other.

    Args:
        Junctions (list of dict): Junctions as computed by detectJunctions, 
            where each junction is a dict with at least a 'Position' key.
        Thresh (float): The threshold for merging junctions (in pixels). Default is 2.

    Returns:
        list of dict: Cleaned and merged junctions.
    """

    Thresh2 = Thresh**2

    # Determine which junctions need to be merged
    mergeMatrix = np.zeros((len(Junctions), len(Junctions)), dtype=bool)
    for j1 in range(len(Junctions)):
        for j2 in range(j1+1, len(Junctions)):
            mergeMatrix[j1, j2] = np.sum((Junctions[j1]['Position'] - Junctions[j2]['Position'])**2) <= Thresh2

    # Determine equivalence classes
    equivalenceClasses = []
    isJunctionAvailable = np.ones(len(Junctions), dtype=bool)
    while np.any(mergeMatrix[:]): # Verify
        j1, _ = np.where(mergeMatrix) # Verify
        equiClass, mergeMatrix, isJunctionAvailable = recursiveClasses(j1, mergeMatrix, isJunctionAvailable)
        equivalenceClasses.append(equiClass)
    
    # Double check that they are all disjoint
    equJuncts = np.concatenate(equivalenceClasses)
    uniqueEquJuncts = np.unique(equJuncts)
    if len(uniqueEquJuncts) < len(equJuncts):
        raise ValueError('Error: Equivalence classes are not disjoint')
    
    # initialize the resulting junctions with all jucntions that do not have neighbors
    cleanedJunctions = Junctions[isJunctionAvailable]

    # Now actually merge junctions that are in equivalence classes
    thisJunct = {}
    for cl in range(len(equivalenceClasses)):
        thisClass = equivalenceClasses[cl]
        allPos = np.array([Junctions[j]['Position'] for j in thisClass]) # Verify
        thisJunct['position'] = np.mean(allPos, axis=0) # Use the center of mass between the junction points

        # Combine contour segments
        thisJunct['contourIDs'] = []
        thisJunct['segmentIDs'] = []
        for j in range(len(thisClass)):
            thisCont = Junctions[thisClass[j]]['contourIDs']
            thisSegm = Junctions[thisClass[j]]['segmentIDs']
            for s in range(len(thisCont)):
                # Make sure we don't already have this contour-segment combination
                if (thisCont[s] not in thisJunct['contourIDs']) or (thisSegm[s] not in thisJunct['segmentIDs']):
                    thisJunct['contourIDs'].append(thisCont[s])
                    thisJunct['segmentIDs'].append(thisSegm[s])
        
        cleanedJunctions.append(thisJunct)

    return cleanedJunctions


