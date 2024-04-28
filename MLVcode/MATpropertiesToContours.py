import numpy as np
import cv2

def MATpropertiesToContours(vecLD, MATpropertyImage, property):
    """
    Maps the MAT properties from the MATpropertyImage back onto the contours
    given by vecLD and stores the results for each contour in the vecLD data structure.

    Args:
        vecLD (dict): The vectorized line drawings data structure.
        MATpropertyImage (numpy.ndarray): Image with the MAT properties.
        property (str): Name of the property, which will be used to name the field inside vecLD.

    Returns:
        dict: The updated vecLD data structure with MAT properties mapped to each contour.
    
    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """

    # Define a vector for scaling the coordinates up or down as needed
    # MATpropertyImage = np.transpose(MATpropertyImage) 
    imsize = (MATpropertyImage.shape[0], MATpropertyImage.shape[1])
    # print("Image Size: ",imsize)
    scaleVec = (imsize[1] / vecLD['imsize'][0][0], imsize[0] / vecLD['imsize'][0][1])
    # scaleVec = (vecLD['imsize'][0][1] / imsize[0], vecLD['imsize'][0][0] / imsize[1])
    scaleVec = np.array([scaleVec, scaleVec]).flatten()
    # print("Scale Vector: ",scaleVec)
    vecLD[property] = np.zeros(vecLD['numContours'][0][0], dtype=object)
    allMeans = np.zeros(vecLD['numContours'][0][0])

    # Collect all scores for the entire image
    allInd = []
    allProp = []

    for c in range(vecLD['numContours']):
        img = np.zeros(imsize, dtype=np.uint8)
        scaledCoords = np.array(vecLD['contours'][0][c]) * scaleVec
        # Convert scaledCoords into format expected by cv2.polylines or cv2.line
        scaledCoords = scaledCoords.reshape((-1, 1, 2)).astype(np.int32)

        # Drawing lines on the image
        img = cv2.polylines(img, [scaledCoords], isClosed=False, color=(255,), thickness=1)

        # Finding indices where img > 0
        thisInd = np.where(img > 0)
        thisProp = MATpropertyImage[thisInd].flatten()
        validProp = (thisProp != 0)

        # Calculating mean of valid properties
        allMeans[c] = np.mean(thisProp[validProp]) if np.any(validProp) else np.nan
        thisProp[~validProp] = np.nan

        # Updating vecLD with properties for this contour
        if property not in vecLD:
            vecLD[property] = []
        vecLD[property].append(thisProp)

        # Accumulating indices and properties
        allInd.extend(thisInd[0][validProp])
        allProp.extend(thisProp[validProp])

    # Assuming imsize is defined somewhere in your code, e.g., imsize = (height, width)
    # Assuming allInd, allMeans, and allProp are already defined from previous operations

    # Update vecLD with the means for each contour property
    vecLD[f'{property}Means'] = allMeans

    # Convert linear indices (allInd) to subscript indices
    Y, X = np.unravel_index(allInd, imsize)

    # Update vecLD with X, Y coordinates and all property scores
    vecLD[f'{property}_allX'] = X
    vecLD[f'{property}_allY'] = Y
    vecLD[f'{property}_allScores'] = allProp

    return vecLD