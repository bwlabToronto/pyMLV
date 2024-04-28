from skimage.morphology import medial_axis, skeletonize
import numpy as np
from renderLineDrawing import renderLineDrawing
from computeMAT import computeMAT
from computeAllMATproperties import computeAllMATproperties
from mapMATtoContour import mapMATtoContour
from MATpropertiesToContours import MATpropertiesToContours
from getMATpropertyStats import getMATpropertyStats



def computeAllMATfromVecLD(vecLD):
    """
    Computes the medial axis properties for a line drawing structure.

    Parameters:
    - vecLD: The vectorized line drawing structure or a list of such structures.
             This drawing will be rendered into an image to compute the medial axis properties.

    Returns:
    - vecLD: The line drawing structure(s) with the medial axis properties added.
    - MAT: The medial axis. In case of multiple vecLD as input, this will be a list of MATs.
    - MATskel: The MAT skeleton image(s) with ratings.

    Note:
    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """

    if len(vecLD) > 1:
        resLD = []
        MAT = []
        for l in range(len(vecLD)):
            print(f"Processing {vecLD[l]['originalImage']} ({l} of {len(vecLD)})...")
            thisLD, thisMAT = computeAllMATfromVecLD(vecLD[l])
            resLD.append(thisLD)
            MAT.append(thisMAT)
        
        vecLD = resLD
        print("Done.")
        return vecLD, MAT, MATskel # Need to fix this
    
    # This is the actual process for a single vecLD
    img = renderLineDrawing(vecLD)
    MAT = computeMAT(img)
    MATimg, MATskel, branches = computeAllMATproperties(MAT, img)
    prop = MATimg.keys()

    for p in range(len(prop)):
        thisPropImg = mapMATtoContour(branches, img, MATskel[prop[p]])
        vecLD = MATpropertiesToContours(vecLD, thisPropImg, prop[p])
        vecLD = getMATpropertyStats(vecLD, prop[p]) 

    return vecLD, MAT, MATskel
    
