import numpy as np

def edges(E, S, h, w, A):
    """
    Determines edge strengths for an image based on superpixels and an affinity matrix.

    This function updates an edge strength matrix `E` by analyzing the relationships between 
    neighboring superpixels within an image. The function uses a superpixel label matrix `S` 
    and an affinity matrix `A` to calculate edge strengths. The edge strength at each pixel 
    location is determined based on the affinity values between neighboring superpixels.

    Args:
        E (ndarray): A 2D array representing the edge strength matrix to be updated. 
                     The matrix should have the same dimensions as the image.
        S (ndarray): A 2D array representing the superpixel label matrix, where each 
                     pixel is labeled with an integer corresponding to its superpixel.
        h (int): The height of the image in pixels.
        w (int): The width of the image in pixels.
        A (ndarray): A 2D square affinity matrix where the element at (i, j) represents 
                     the affinity between superpixel i and superpixel j. The affinity values 
                     range from 0 (no affinity) to 1 (high affinity).

    Returns:
        ndarray: The updated edge strength matrix `E` with the same dimensions as the input 
                 image, where each pixel's edge strength has been recalculated based on 
                 the surrounding superpixel affinities.

    Notes:
    - The function iterates over each pixel in the image and considers its 8-neighborhood 
      (including diagonal neighbors) to determine the edge strength.
    - If a pixel is already associated with a superpixel (i.e., `S[y, x]` is non-zero), it is 
      skipped, and its edge strength is not recalculated.
    - The edge strength for a pixel is set to a default minimum value of 0.01 if no neighboring 
      superpixels are found.
    - When multiple unique superpixels are present in a pixel's neighborhood, the function calculates 
      the edge strength based on the affinities between all pairs of these superpixels.
    - The function assumes that superpixel labels in `S` are 1-based (starting from 1).


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
    # Determine the maximum superpixel label
    m = S.max()
    
    # Iterate over each pixel
    for x in range(w):
        for y in range(h):
            # Skip if the pixel is already processed or non-zero in S
            if S[y, x] != 0:
                continue
            
            # Initialize edge strength
            E[y, x] = 0.01
            
            # Collect neighborhood indices
            x_indices = [x-1, x, x+1]
            y_indices = [y-1, y, y+1]
            
            # Ensure the indices are within image boundaries
            x_indices = [xi for xi in x_indices if 0 <= xi < w]
            y_indices = [yi for yi in y_indices if 0 <= yi < h]
            
            # Extract the neighborhood
            neighborhood = S[np.ix_(y_indices, x_indices)]
            
            # Collect unique superpixels, excluding zero
            unique_superpixels = np.unique(neighborhood[neighborhood > 0]) - 1 # Adjust for zero-based indexing
            
            # Calculate edge strength using the affinity matrix
            if len(unique_superpixels) > 1:
                # Generate all pairs of unique superpixels
                n_unique = len(unique_superpixels)
                pairs = np.array(np.triu_indices(n_unique, 1)).T
                pairs = np.column_stack((unique_superpixels[pairs[:, 0]] + 1, unique_superpixels[pairs[:, 1]] + 1)) # Adjust back to 1-based indexing
                
                # Compute the linear indices for the affinity matrix
                linear_indices = np.ravel_multi_index((pairs[:, 0]-1, pairs[:, 1]-1), (m, m))
                
                # Update edge strength
                for k in range(len(linear_indices)):
                    E[y, x] = max(1 - A.flat[linear_indices[k]], E[y, x])
    
    return E