import numpy as np
import cv2

def generateFeatureDensityMap(vecLD, property, smoothingSigma=0, junctionTypes=None):
    """
    Generates a feature density map (FDM) for a specified contour property in a vectorized line drawing.
    Optionally applies Gaussian smoothing to the density map.

    This function creates a density map based on the specified contour property present in the vectorized
    line drawing. If smoothing is requested, it applies a 2D Gaussian smoothing operation with the specified
    standard deviation.

    Args:
        vecLD (dict): The vectorized line drawing data structure with the contour property already computed.
        property (str): The name of the contour property for which the FDM is generated. Valid options include
                        'length', 'curvature', 'orientation', 'junctions', 'mirror', 'parallelism', 'separation'.
        smoothingSigma (float, optional): The standard deviation of the 2D Gaussian smoothing kernel, in pixels.
                                          Default is 0, indicating no smoothing.
        junctionTypes (list of str, optional): Only relevant when `property` is 'junctions'. Specifies the types
                                               of junctions to consider. Default is None, which considers all junctions.

    Returns:
        numpy.ndarray: The feature density map (FDM) with the same size as the original image. The FDM is generated
                       using raw feature values without any normalization applied.

    Notes:
    - For properties like 'junctions', 'mirror', 'parallelism', 'separation', additional considerations might
      be necessary to accurately generate the density map.
    - The user may want to normalize the resulting FDM to sum to 1 (as a probability distribution) or to have
      0 mean and unit standard deviation for further analysis.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Function implementation goes here

    FDM = np.zeros((vecLD['height'], vecLD['width']), dtype=np.float32)

    # Switch case for different properties
    if property == 'orientation':
        xMap = np.zeros((vecLD['height'], vecLD['width']), dtype=np.float32)
        yMap = np.zeros((vecLD['height'], vecLD['width']), dtype=np.float32)

        for c in range(vecLD['numContours']):
            oris = np.mod(vecLD['orientations'][c], 180)
            sinAngle = np.sin(np.radians(oris))
            cosAngle = np.cos(np.radians(oris))

            for s in range(len(vecLD['contours'][c])): # VERIFY THIS
                thisMap = np.zeros((vecLD['imsize'][1], vecLD['imsize'][0], 3), dtype=np.uint8)
                # Draw the line
                pt1 = (int(vecLD['contours'][c][s][0]), int(vecLD['contours'][c][s][1]))
                pt2 = (int(vecLD['contours'][c][s][2]), int(vecLD['contours'][c][s][3]))
                cv2.line(thisMap, pt1, pt2, (255, 0, 0), 1)
                thisMap = thisMap[:, :, 0]  # Extract the red channel where the line was drawn
                thisIdx = (thisMap > 0)

                # Update xMap and yMap where thisMap is non-zero
                xMap[thisIdx] = sinAngle[s]
                yMap[thisIdx] = cosAngle[s]

        if smoothingSigma > 0: # 
            xMap = cv2.GaussianBlur(xMap, (0, 0), smoothingSigma)
            yMap = cv2.GaussianBlur(yMap, (0, 0), smoothingSigma)
        
        FDM = np.degrees(np.arctan2(yMap, xMap))

    elif property == 'length':
        for c in range(vecLD['numContours']):
            thisMap = np.zeros((vecLD['imsize'][1], vecLD['imsize'][0], 3), dtype=np.uint8)
            for s in range(len(vecLD['contours'][c])):
                # Draw the line
                pt1 = (int(vecLD['contours'][c][s][0]), int(vecLD['contours'][c][s][1]))
                pt2 = (int(vecLD['contours'][c][s][2]), int(vecLD['contours'][c][s][3]))
                cv2.line(thisMap, pt1, pt2, (255, 0, 0), 1)
            thisMap = thisMap[:, :, 0]
            FDM[thisMap > 0] = vecLD['contourLengths'][c]

        if smoothingSigma > 0:
            FDM = cv2.GaussianBlur(FDM, (0, 0), smoothingSigma)

    elif property == 'curvature':
        for c in range(vecLD['numContours']):
            for s in range(len(vecLD['contours'][c])):
                thisMap = np.zeros((vecLD['imsize'][1], vecLD['imsize'][0], 3), dtype=np.uint8)
                # Draw the line
                pt1 = (int(vecLD['contours'][c][s][0]), int(vecLD['contours'][c][s][1]))
                pt2 = (int(vecLD['contours'][c][s][2]), int(vecLD['contours'][c][s][3]))
                cv2.line(thisMap, pt1, pt2, (255, 0, 0), 1)
                thisMap = thisMap[:, :, 0]
                FDM[thisMap > 0] = vecLD['curvatures'][c][s]
        
        if smoothingSigma > 0:
            FDM = cv2.GaussianBlur(FDM, (0, 0), smoothingSigma)
        
    elif property == 'junctions':
        if junctionTypes is None:
            junctionTypes = {}
        junctionTypes = {vecLD['junctions']['type']} # FIX THIS BASED ON STRUCTURE OF ARGUEMENTS

        for j in range(len(vecLD['junctions'])):
            if vecLD['junctions']['type'][j] in junctionTypes:
                pos = np.round(vecLD['junctions']['position'][j])
                # Make sure we're in bounds
                if pos[0] < 1:
                    pos[0] = 1
                if pos[0] > vecLD['imsize'][0]:
                    pos[0] = vecLD['imsize'][0]
                if pos[1] < 1:
                    pos[1] = 1
                if pos[1] > vecLD['imsize'][1]:
                    pos[1] = vecLD['imsize'][1]

                # Set the point in the map
                FDM[int(pos[1]), int(pos[0])] = 1
        
        if smoothingSigma > 0:
            FDM = cv2.GaussianBlur(FDM, (0, 0), smoothingSigma)

    elif property == 'mirror':
        for p in range(len(vecLD['mirror_allScores'])):
            FDM[vecLD['mirror_allY'][p], vecLD['mirror_allX'][p]] = vecLD['mirror_allScores'][p]
        
        if smoothingSigma > 0:
            FDM = cv2.GaussianBlur(FDM, (0, 0), smoothingSigma)

    elif property == 'parallelism':
        for p in range(len(vecLD['parallelism_allScores'])):
            FDM[vecLD['parallelism_allY'][p], vecLD['parallelism_allX'][p]] = vecLD['parallelism_allScores'][p]
        
        if smoothingSigma > 0:
            FDM = cv2.GaussianBlur(FDM, (0, 0), smoothingSigma)

    elif property == 'separation':
        for p in range(len(vecLD['separation_allScores'])):
            FDM[vecLD['separation_allY'][p], vecLD['separation_allX'][p]] = vecLD['separation_allScores'][p]
        
        if smoothingSigma > 0:
            FDM = cv2.GaussianBlur(FDM, (0, 0), smoothingSigma)

    else:
        raise ValueError(f'Invalid property [{property}] specified. Valid options include: length, curvature, orientation, junctions, mirror, parallelism, separation.')
    return FDM


                         