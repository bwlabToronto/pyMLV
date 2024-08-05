import numpy as np
from scipy.ndimage import distance_transform_edt
from MLVcode.is_outer_border_point import is_outer_border_point


def getOuterBoundary(binaryImage, background):
    """
    Extracts the outer boundary coordinates from a binary image.

    This function traverses a binary image and identifies the outer boundary points 
    using an 8-neighborhood approach. It checks if each pixel is an outer border point 
    relative to the specified background value.

    Args:
        binaryImage (numpy.ndarray): A binary image where the objects are marked 
        with 1's (or any non-background value) and the background is marked with 
        the specified background value.
        background (int or float): The value representing the background in the binary image.

    Returns:
        tuple: A tuple (result, result2) where:
            result (numpy.ndarray): An array of shape (number of boundary points, 2), 
            containing the coordinates of the boundary points.
            result2 (numpy.ndarray): A binary image of the same size as binaryImage, 
            with 1's marking the boundary points and 0's elsewhere.

    Notes:
    - The function uses an 8-neighborhood approach to identify boundary points.
    - The outer boundary is defined as the set of non-background pixels that have at least 
      one background pixel in their 8-neighborhood.
    - 'result' contains the coordinates of the boundary points, while 'result2' is a binary 
      image marking these points.
    - Debug information such as the size of 'result' and the counter of boundary points 
      is printed during execution.

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
    m_Neighbors8 = np.array([[-1, -1], [-1, 0], [-1, 1],
                             [0, -1], [0, 1],
                             [1, -1], [1, 0], [1, 1]])
    result2 = np.zeros(shape=binaryImage.shape)
    m, n = binaryImage.shape
    result = np.zeros(shape=(m * n, 2))
    print("Result Size: ", result.shape)
    counter = 0
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            if is_outer_border_point(binaryImage, i, j, m_Neighbors8, background):
                result[counter][0] = i
                result[counter][1] = j
                result2[i][j] = 1
                counter += 1
    print("Counter: ", counter)
    # result = result(1:counter-1,:); to python
    result = result[:counter, :]
    return result, result2