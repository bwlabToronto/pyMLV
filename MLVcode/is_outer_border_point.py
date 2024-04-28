import numpy as np

# Def is_outer_border_point
def is_outer_border_point(binaryImage, ii, jj, m_Neighbors8, background):
    """
    Determines if a given pixel in a binary image is an outer border point.

    This function checks whether a specified pixel in a binary image is an outer border point. 
    A pixel is considered an outer border point if it is a background pixel and has at least 
    one foreground and one background pixel in its 8-neighborhood.

    Args:
        binaryImage (numpy.ndarray): A binary image where the objects are marked 
        with non-background values and the background is marked with the specified background value.
        ii (int): The row index of the pixel to check.
        jj (int): The column index of the pixel to check.
        m_Neighbors8 (numpy.ndarray): An array of 8 neighbor offsets to consider around the pixel.
        background (int or float): The value representing the background in the binary image.

    Returns:
        int: Returns 1 if the pixel is an outer border point, otherwise 0.

    Notes:
    - The function iterates through the 8-neighborhood of the specified pixel.
    - It counts the number of foreground and background pixels in the neighborhood.
    - A pixel is classified as an outer border point if it is a background pixel and has 
      at least one foreground and one background neighbor.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    if binaryImage[ii, jj] == background:
        result2 = 0
        nOfBackgroundPoints = 0
        nOfForegoundPoints = 0
        iterator = 0
        while (nOfBackgroundPoints == 0 or nOfForegoundPoints == 0) and iterator <= 7:
            if binaryImage[ii + m_Neighbors8[iterator][0], jj + m_Neighbors8[iterator][1]] > background:
                nOfForegoundPoints += 1
            elif binaryImage[ii + m_Neighbors8[iterator][0], jj + m_Neighbors8[iterator][1]] <= background:
                nOfBackgroundPoints += 1
            iterator += 1
        if nOfBackgroundPoints > 0 and nOfForegoundPoints > 0:
            result2 = 1
        else:
            result2 = 0
        return result2
    else:
        return 0