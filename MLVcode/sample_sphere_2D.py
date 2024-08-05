import math
import numpy as np

def sample_sphere_2D(number_of_samples):
    """
    Generates evenly distributed points on the circumference of a unit circle (2D sphere).

    This function creates a set of points evenly distributed along the circumference of a unit circle.
    It uses a uniform angular distribution to place each point on the circle.

    Args:
        number_of_samples (int): The number of points to be generated on the circle.

    Returns:
        numpy.ndarray: A 2D array of shape (number_of_samples, 2) where each row 
        represents the (x, y) coordinates of a point on the unit circle.

    Notes:
    - The function calculates the angular step based on the number of samples and 
      uses trigonometric functions (sine and cosine) to compute the coordinates.
    - The circle is centered at the origin (0,0) with a radius of 1.

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
    sphere_points = np.zeros((number_of_samples, 2))
    alpha = 2 * math.pi / number_of_samples
    for i in range(number_of_samples):
        sphere_points[i, 0] = math.cos(i * alpha)
        sphere_points[i, 1] = math.sin(i * alpha)
    return sphere_points