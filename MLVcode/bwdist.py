import numpy as np
from scipy.ndimage import distance_transform_edt


# BWDist
def bwdist(mat):
    """
    Computes the Euclidean distance transform of a binary image and returns the distances 
    and the indices of the nearest non-zero pixels.

    This function calculates the distance of each pixel in a binary matrix `mat` from the nearest 
    non-zero pixel. It also provides the indices of these nearest non-zero pixels in a flattened format.

    Args:
        mat (ndarray): A 2D binary matrix (NumPy array) where non-zero elements represent foreground pixels 
                       and zeros represent background pixels.

    Returns:
        tuple:
            - d (ndarray): A 2D array of the same shape as `mat`, where each element contains the Euclidean 
                           distance to the nearest non-zero pixel in `mat`.
            - idx (ndarray): A 2D array of the same shape as `mat`, where each element contains the flattened 
                             index of the nearest non-zero pixel in the input matrix `mat`.

    Notes:
    - The function uses the Euclidean distance transform provided by `scipy.ndimage.distance_transform_edt`.
    - The `idx` array is calculated by combining the row and column indices of the nearest non-zero pixels into 
      a single flattened index using row-major order.
    - This function is useful in image processing tasks where understanding the proximity of features within 
      a binary image is necessary.

    Raises:
        None: This function assumes that `mat` is a valid binary matrix.
        
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
    d, labels =distance_transform_edt(
        mat==0, return_distances=True, return_indices=True)
    # print("d: \n", d)
    # print("labels: \n", labels)
    idx = np.zeros(mat.shape, dtype=np.intp)
    for row in range(mat.shape[0]):
        for col in range(mat.shape[1]):
            idx[row, col] = labels[0][row, col] * mat.shape[1] + labels[1][row, col]
    # print("IDX: \n", idx)
    return d, idx