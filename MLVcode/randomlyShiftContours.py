import numpy as np

def randomlyShiftContours(vecLD, maxShift=None):
    """
    Randomly shifts the contours within a vectorized line drawing.

    This function applies a random shift to each contour within a vectorized line drawing. 
    The shift is bounded by a maximum shift value, which can be specified either as a scalar 
    (applied to both x and y directions) or as a two-element vector specifying separate 
    maximum shifts for the x and y directions.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing to be modified.
        maxShift (int or tuple of int): A scalar specifying the maximum number of pixels 
                                        used for the shift in both x and y directions, 
                                        or a two-element tuple specifying the maximum 
                                        shift in the x and y directions, respectively.

    Returns:
        LineDrawingStructure: A new vectorized line drawing with the shifted contours.

    Usage:
        shiftedLD = randomlyShiftContours(vecLD, maxShift)
        shiftedLD = randomlyShiftContours(vecLD, (maxShiftX, maxShiftY))

    References:
        - Walther, D. B., & Shen, D. (2014). Nonaccidental properties underlie 
          human categorization of complex natural scenes. Psychological Science, 
          25(4), 851-860. https://doi.org/10.1177/0956797613512662
        - Choo, H., & Walther, D. B. (2016). Contour junctions underlie neural 
          representations of scene categories in high-level human visual cortex. 
          Neuroimage, 135, 32-44. https://doi.org/10.1016/j.neuroimage.2016.04.021

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
    if maxShift is None:
        maxShift = vecLD['imsize'][0]

    if len(maxShift) == 1:
        maxShift = [maxShift, maxShift]

    shiftedLD = {}
    shiftedLD['originalImage'] = vecLD['originalImage']
    shiftedLD['imsize'] = vecLD['imsize']
    shiftedLD['lineMethod'] = vecLD['lineMethod']
    shiftedLD['numContours'] = vecLD['numContours']
    shiftedLD['contours'] = []

    for c in range(vecLD['numContours']):
        
        # X direction
        # Extracting all X coordinates (assuming first and third columns are X coordinates)
        # and finding the minimum and maximum X values for contour c.
        x_coords = np.concatenate((vecLD['contours'][c][:, 0], vecLD['contours'][c][:, 2]))
        minX = np.min(x_coords)
        maxX = np.max(x_coords)

        lowX = np.maximum(minX-1, maxShift[0])
        highX = np.minimum(vecLD['imsize'][0]-maxX, maxShift[0])
        shiftX = np.random.randint(-lowX, highX)

        # Y direction
        # Extracting all Y coordinates (assuming second and fourth columns are Y coordinates)
        # and finding the minimum and maximum Y values for contour c.
        y_coords = np.concatenate((vecLD['contours'][c][:, 1], vecLD['contours'][c][:, 3]))
        minY = np.min(y_coords)
        maxY = np.max(y_coords)

        lowY = np.maximum(minY-1, maxShift[1])
        highY = np.minimum(vecLD['imsize'][1]-maxY, maxShift[1])
        shiftY = np.random.randint(-lowY, highY)

        # Shift the coordinates
        shiftedContour = vecLD['contours'][c].copy()
        shiftedLD['contours'][c] = vecLD['contours'][c] + shiftedContour # FIX THIS LINE 

    return shiftedLD


    