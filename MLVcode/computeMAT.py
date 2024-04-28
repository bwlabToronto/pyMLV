import numpy as np
from MLVcode.extract2DSkeletonFromBinaryImage import extract2DSkeletonFromBinaryImage
import scipy.io as sio

def computeMAT(imgLD,
               threshold_angle=28):
    """
    Extracts the Medial Axis Transform from a given line drawing image (imgLD) and returns its distance map,
    its average out flux (AOF) map, and the skeleton.

    Args:
        imgLD (ndarray): A line drawing image.
        threshold_angle (float, optional): Threshold on the object angle in degrees. Default is 28 degrees.

    Returns:
        dict: A dictionary with the following fields:
            - 'skeleton' (ndarray): A binary image the same size as imgLD. 1s represent where the skeleton appears.
            - 'distance_map' (ndarray): A distance-transformed image of the same size as imgLD.
            - 'AOF' (ndarray): Average outward flux image computed from the distance transform.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Morteza Rezanejad
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: Morteza.Rezanejad@gmail.com
    -----------------------------------------------------
    """
    binaryImage = imgLD
    # Define MAT which have three fields: skeleton, distance_map, AOF
    mat = {}
    # aof = 2/pi * sin(Object_Angle)
    if threshold_angle == 28:
        threshold = 0.3
    else:
        threshold = 2/np.pi * np.sin(np.deg2rad(threshold_angle))

    # In case thw input image has three channels
    # if len(binaryImage.shape) == 3:
    #     binaryImage = cv2.cvtColor(binaryImage, cv2.COLOR_BGR2GRAY)
    binaryImage = binaryImage[:,:,0]
    fluxImage, skeletonImage, distImage, _ = extract2DSkeletonFromBinaryImage(binaryImage,threshold)
    # extract2DSkeletonFromBinaryImage(binaryImage,threshold)
    # # Skeleton
    mat['skeleton'] = skeletonImage

    # # Distance map
    mat['distance_map'] = distImage

    # # Average outward flux map
    mat['AOF'] = fluxImage
    # Save MAT as .mat file
    sio.savemat('MAT.mat', mat)
    # Save AOFSkeleton as .mat file
    return mat, fluxImage, skeletonImage, distImage