import numpy as np

def relabel(S, h, w):
    """
    Relabel the regions in an image based on connectivity, ensuring unique labels for connected regions.

    This function processes a labeled image and reassigns labels to ensure that each connected region 
    within the image has a unique label. The relabeling is based on connectivity, taking into account 
    both horizontal and vertical connections, and resolving label conflicts that arise from diagonal 
    connectivity.

    Args:
        S (ndarray): Input label matrix of size (h, w), where each element represents a labeled region.
        h (int): Height of the image.
        w (int): Width of the image.

    Returns:
        ndarray: The input label matrix `S`, with regions relabeled to ensure unique labels for each 
                 connected component.

    Notes:
    - The function starts by assigning initial labels based on vertical connectivity for the first column 
      and then proceeds to label the entire image while handling horizontal and vertical connections.
    - It resolves conflicts in labeling that may occur due to diagonal connectivity between neighboring 
      regions by using a temporary mapping array.
    - After resolving conflicts, the function flattens the mapping to ensure each region has a unique and 
      consecutive label, and then applies this mapping to the entire image.

    Raises:
        None: This function assumes that `S` is a valid labeled matrix and that `h` and `w` correspond 
              to the dimensions of `S`.
              
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
    T = np.zeros((h, w), dtype=np.uint32)  # Temporary array for new labels
    map = np.zeros(h * w // 2, dtype=np.uint32)

    m = np.uint32(1)  # Initial label
    T[0, 0] = m  # Assign the first element
    m += 1

    # Relabel based on vertical connectivity for the first column
    for y in range(1, h):
        if S[y, 0] == S[y - 1, 0]:
            T[y, 0] = T[y - 1, 0]
        else:
            T[y, 0] = m
            m += 1

    # Relabel based on horizontal and vertical connectivity for each column
    for x in range(1, w):
        z = x * h
        T[0, x] = T[0, x - 1] if S[0, x] == S[0, x - 1] else m
        if S[0, x] != S[0, x - 1]:
            m += 1

        for y in range(1, h):
            z = y + x * h
            if S[y, x] == S[y, x - 1]:
                T[y, x] = T[y, x - 1]
            elif S[y, x] == S[y - 1, x]:
                T[y, x] = T[y - 1, x]
            else:
                T[y, x] = m
                m += 1

            # Handle the diagonal connectivity and resolve conflicts
            if T[y, x - 1] != T[y - 1, x] and S[y, x - 1] == S[y, x] and S[y - 1, x] == S[y, x]:
                t1 = T[y, x - 1]
                while map[t1] != 0:
                    t1 = map[t1]
                t2 = T[y - 1, x]
                while map[t2] != 0:
                    t2 = map[t2]
                if t1 != t2:
                    if t1 < t2:
                        map[t2] = t1
                        T[y, x] = t1
                    else:
                        map[t1] = t2
                        T[y, x] = t2

    # Flatten the mapping to ensure direct mapping to final labels
    m1 = np.uint32(0)
    for t in range(1, m):
        if map[t] != 0:
            map[t] = map[map[t]]
        else:
            map[t] = m1
            m1 += 1

    # Apply the final mapping to S
    for x in range(w):
        for y in range(h):
            S[y, x] = map[T[y, x]]

    return S