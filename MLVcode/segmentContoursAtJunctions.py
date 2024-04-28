import numpy as np

def segmentContoursAtJunctions(vecLD):
    """
    Creates a new line drawing with contours segmented at junction points.

    This function processes a vectorized line drawing, identifying and segmenting contours at junction points.
    In the resulting line drawing, contours will terminate at junction points rather than running through them,
    making the new drawing structurally different from the original while maintaining its visual integrity.

    Args:
        vecLD (dict): The vectorized line drawing data structure with junctions already computed.
                      If there is no 'junctions' key in the dict, junctions will be computed.

    Returns:
        dict: The new line drawing data structure with contours split at junctions.

    Notes:
    - The function assumes that `vecLD` is a dictionary-like structure that may contain a key 'junctions' 
      with computed junction data. If 'junctions' is not present, the function will first compute junctions.
    - This function is useful for preparing line drawings for analyses that require understanding of contour 
      intersections and terminations.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Function implementation goes here
    if 'junctions' not in vecLD:
        vecLD = computeJunctions(vecLD)


    
    # Prepare the new data structure
    newLD = {}
    newLD['originalImage'] = vecLD['originalImage']
    newLD['imsize'] = vecLD['imsize']
    newLD['lineMethod'] = vecLD['lineMethod']
    newLD['numContours'] = vecLD['numContours']
    newLD['contours'] = []

    # Loop over the contours of the old
    for c in range(vecLD['numContours']):
        # Find all junctions for this contour
        thisJunctions = []
        thisSegments = []
        for jj in range(len(vecLD['junctions'])):
            thisCidx = np.where(vecLD['junctions'][jj]['contours'] == c)[0] # VERIFY
            if len(thisCidx) > 0:
                thisJunctions.append(vecLD['junctions'][jj])
                thisSegments.append(vecLD['junctions'][jj]['segmentIDs'][thisCidx[0]]) # VERIFY
        
        # no junctions? Just copy the contour and be done.
        if len(thisJunctions) == 0:
            newLD['numContours'] += 1
            newLD['contours'].append(vecLD['contours'][c])
            continue

        # Sort the segments
        sortedSeg, segIdx = np.sort(thisSegments), np.argsort(thisSegments) # VERIFY

        # loop over the junction points, and deal with the special case of
        # multiple junctions within the same segment
        points = []
        uniqueSeg = np.unique(sortedSeg)
        for u in range(len(uniqueSeg)):
            currSeg = np.where(sortedSeg == uniqueSeg[u])[0] # VERIFY

            # just one junction in this segment? Easy
            if len(currSeg) == 1:
                points.append(vecLD['junctions'][segIdx[currSeg[0]]]['position'])
            else:
                # multiple junctions? Need to figure which ones are clsoest to
                # the start point of this semgent
                startPoint = vecLD['contours'][c]['points'][uniqueSeg[u]][0:1] # VERIFY
                distances = np.zeros(len(currSeg))

                # Compute the distances
                thisPoints = []
                for j in range(len(currSeg)):
                    thisPoints.append(vecLD['junctions'][segIdx[currSeg[j]]]['position'])
                    distances[j] = np.linalg.norm(thisPoints[j] - startPoint)

                # Sort the distances, and store points
                sortedDist, distIdx = np.sort(distances), np.argsort(distances)
                points.append(thisPoints[distIdx[0]])


    # Add the end point of the last segment, unless it's already the last point
    endpoint = vecLD['contours'][c]['points'][uniqueSeg[-1]][-1:] # VERIFY 
    dist = np.linalg.norm(endpoint - points[-1])
    if dist > 0.01:
        points.append(endpoint)
        sortedSeg = np.concatenate((sortedSeg, [vecLD['contours'][c]['numPoints']])) # VERIFY

    # set the start point to the start point of the first segment
    prevSeg = 0
    prevPoint = vecLD['contours'][c]['points'][0:1]
    newContour = {}

    # Loop over all junction points and cut and assign segments as needed
    for s in range(len(sortedSeg)):
        seg = sortedSeg[s]

        # special case if we stay within the same segment
        if seg == prevSeg:
            newContour = [prevPoint, points[s]]
            prevPoint = points[s]
        else:
            # add the remaining bit from the previous segment
            newContour = [prevPoint, vecLD['contours'][c]['points'][2:3]]
            prevSeg += 1

            # now add whole segments until we hit the segment with the next junction
            if prevSeg < seg:
                newContour.append(vecLD['contours'][c]['points'][prevSeg:seg-1]) # VERIFY
            
            # now add the bit of the current segment until the junction
            newContour.append(vecLD['contours'][c]['points'][seg-1:seg]) # VERIFY
            prevSeg = seg
            prevPoint = points[s]

        # Add the newly constructed contour to the new LD
        newLD['numContours'] += 1
        newLD['contours'].append(newContour)

    return newLD