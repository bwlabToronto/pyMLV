import numpy as np
from skimage import measure, morphology

def get_con_seg(contour, min_length=10):
    """
    Removes small objects from a binary edge image and links edge points into segments.

    This function processes a binary image where edges are represented by non-zero pixels. 
    It first identifies connected components in the image, removes those that are smaller 
    than a specified minimum length, and then extracts the remaining edge segments as lists 
    of coordinates. This can be useful in image processing tasks where significant edge 
    structures need to be isolated and analyzed.

    Args:
        contour (ndarray): A binary image (NumPy array) where edge pixels are marked with 
                           non-zero values. Typically, this is an output from edge detection 
                           algorithms.
        min_length (int, optional): The minimum length of edge segments (in pixels) that 
                                    should be retained. Edge segments shorter than this 
                                    value will be removed. Default is 10 pixels.

    Returns:
        list: A list of edge segments, where each segment is represented as an array of 
              coordinates. Each array contains the (row, column) indices of the pixels 
              that make up the segment.

    Notes:
    - The function uses connected component labeling to identify individual edge segments 
      in the binary image.
    - Small segments are removed based on the `min_length` parameter, helping to clean up 
      noise and focus on more significant structures.
    - The output list of edge segments is useful for further analysis, such as measuring 
      edge lengths, shapes, or linking edges to other image features.


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
    # Label connected components
    labeled_edges, num_features = measure.label(contour, connectivity=2, return_num=True)
    
    # Remove small objects
    cleaned_edges = morphology.remove_small_objects(labeled_edges, min_size=min_length)
    
    # Extract edge segments
    seg_list = measure.regionprops(cleaned_edges)
    
    # Convert to list of coordinates
    edge_segments = []
    for region in seg_list:
        coords = region.coords  # Coordinates of the edge points
        edge_segments.append(coords)
    
    return edge_segments

