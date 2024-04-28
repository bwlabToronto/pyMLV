import numpy as np
from traceSkeleton import traceSkeleton # Need to add
from computeMATproperty import computeMATproperty # Need to add
from mapMATtoContour import mapMATtoContour 

def computeAllMATproperties(MAT, imgLD, prop=None):
    """
    Computes all medial axis-based properties for a line drawing image
    given its medial axis representation.

    Parameters:
    - MAT: Medial axis transform of the line drawing.
    - imgLD: The line drawing image as an array.
    - properties (list of str, optional): The type of property that the user wants to look at.
      Options include:
      1. 'parallelism'
      2. 'separation'
      3. 'mirror'
      4. 'taper'
      If properties are given empty or None, the code produces three properties
      ('parallelism', 'separation', 'mirror') by default.

    Returns:
    - MATcontourImages: The contour images rated by the specific set of properties.
    - MATskeletonImages: The medial axis transform images rated by the specific set of properties.
    - skeletalBranches: The set of skeletal branches traced from the medial axis transform.

    Note:
    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """

    skeletalBranches = traceSkeleton(MAT)
    if prop is None:
        prop = ['parallelism', 'separation', 'mirror']

    for propertyInd in range(len(prop)):
        property = prop[propertyInd]
        skeletonImageWithRating, skeletalBranches = computeMATproperty(MAT, prop, skeletalBranches)
        contourImageWithRating = mapMATtoContour(skeletalBranches, imgLD, skeletonImageWithRating)
        MATskeletonImages = {}
        MATskeletonImages[prop] = skeletonImageWithRating
        MATcontourImages = {}
        MATcontourImages[prop] = contourImageWithRating
    
    return MATcontourImages, MATskeletonImages, skeletalBranches

