import numpy as np
from scipy.ndimage import label, generate_binary_structure
from skimage.measure import regionprops

def bwareaopen(bw, p, conn=None):
    """
    Removes small objects from a binary image.

    This function processes a binary image by identifying and removing objects (connected components) that contain 
    fewer than a specified number of pixels. It is useful for cleaning up noise in binary images by discarding small 
    objects that may not be of interest.

    Args:
        bw (ndarray): A binary image (NumPy array) where objects are represented by non-zero pixels.
        p (int): The minimum number of pixels an object must have to be retained in the output image. 
                 Objects with fewer pixels will be removed.
        conn (int or ndarray, optional): Specifies the desired connectivity for determining which pixels 
                                         are considered connected. If not provided, the function uses the 
                                         maximal connectivity based on the dimensions of the image. 
                                         This can be an integer (1 for minimal connectivity, up to the number 
                                         of dimensions of the image) or a structuring element defining connectivity.

    Returns:
        ndarray: A binary image with the same dimensions as the input `bw`, but with all small objects removed. 
                 The output image will only include objects that have at least `p` pixels.

    Notes:
    - The function works by first labeling all connected components in the image using the specified connectivity.
    - It then filters out components that do not meet the minimum pixel count criterion.
    - This function is commonly used in image processing workflows to remove noise or irrelevant small features from binary images.

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
    if not np.issubdtype(bw.dtype, np.bool_):
        bw = bw != 0
    
    if conn is None:
        conn = generate_binary_structure(bw.ndim, bw.ndim)
    elif isinstance(conn, int):
        conn = generate_binary_structure(bw.ndim, conn)

    labeled_array, num_features = label(bw, structure=conn)
    props = regionprops(labeled_array)
    
    bw2 = np.zeros_like(bw, dtype=np.bool_)
    for prop in props:
        if prop.area >= p:
            bw2[labeled_array == prop.label] = True
    
    return bw2