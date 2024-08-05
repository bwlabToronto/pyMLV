import numpy as np

def InitializeNeighborhoods():
    """
    Initializes an array representing the 8-neighborhoods of a pixel in a 2D grid.

    This function creates and returns an array that represents the relative coordinates 
    of the 8 neighbors surrounding a central pixel in a 2D grid. This is commonly used in 
    image processing tasks where neighborhood information of pixels is required.

    Returns:
        numpy.ndarray: An array of shape (8, 2) where each row represents the relative 
        (row, column) offsets of one of the 8 neighboring pixels.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Python Implementation: Aravind Narayanan
    Original MATLAB Implementation: Dirk Bernhardt-Walther
    Copyright: Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2024

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    Skeletonization package from earlier work of Morteza Rezanejad
    Check the https://github.com/mrezanejad/AOFSkeletons
    """

    m_Neighbors8 = np.array([[-1,-1], 
                             [-1,0], 
                             [-1,1], 
                             [0,-1], 
                             [0,1], 
                             [1,-1], 
                             [1,0], 
                             [1,1]])
    return m_Neighbors8