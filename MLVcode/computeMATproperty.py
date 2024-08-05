import numpy as np
from traceSkeleton import traceSkeleton
from computeMATpropertyPerBranch import computeMATpropertyPerBranch

def computeMATproperty(MAT, prop, skeletalBranches=None, K=5):
    """
    Computes Medial Axis-based properties for an image.

    Parameters:
    - MAT: Medial axis transform object.
    - property (str): A string signaling the property that should be computed, one of: 'parallelism', 'separation', 'taper', 'mirror'.
    - skeletalBranches: The medial axis skeleton. If this argument is
                        omitted, skeletalBranches are computed using traceSkeleton.
                        Default is None.
    - K (int): The length of the window on the skeletal branch for computing
               the property. Default is 5.

    Returns:
    - skeletonImageWithRating: The image of the medial axis skeleton with
                               the ratings specified by property encoded in the image pixels.
    - skeletalBranches: The individual branches with their rating scores.

    Note:
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
    if skeletalBranches is None:
        skeletalBranches = traceSkeleton(MAT)

    skeletonImageWithRating = np.zeros(MAT['skeleton'].shape)

    for i in range(len(skeletalBranches)):
        scores = computeMATpropertyPerBranch(skeletalBranches[i], prop, K)
        skeletalBranches[i][prop] = scores
        
        # Convert branch coordinates (X, Y) to linear indices and update the image
        curBranchInds = np.ravel_multi_index((skeletalBranches['Y'], skeletalBranches['X']), MAT['skeleton'].shape) # Check this line
        skeletonImageWithRating[curBranchInds] = scores

    return skeletonImageWithRating, skeletalBranches