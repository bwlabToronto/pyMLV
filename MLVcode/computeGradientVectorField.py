import numpy as np
from scipy.ndimage import distance_transform_edt
from MLVcode.is_outer_border_point import is_outer_border_point
from MLVcode.getOuterBoundary import getOuterBoundary
from MLVcode.bwdist import bwdist
import matplotlib.pyplot as plt
from MLVcode.load_mat import load_mat



def computeGradientVectorField(binaryImage):
    """
    Computes the gradient vector field of a binary image.

    This function transforms a binary image, identifies the outer boundary, 
    and calculates two distance transforms, IDX1 and IDX2, from the binary image 
    and its complement, respectively. It then computes a histogram of the distance 
    transforms and combines them to form the gradient vector field.

    Args:
        binaryImage (numpy.ndarray): A binary image where the objects are marked with 1's and 
        the background is marked with 0's.

    Returns:
        tuple: A tuple (D, IDX) where:
            D (numpy.ndarray): The difference between the distance transforms from the 
            binary image and its complement.
            IDX (numpy.ndarray): The combined distance transform.

    Notes:
    - The function modifies the input binary image by converting 1s to 255s and vice versa.
    - It loads an external file 'outerBoundaryOriginal.mat' for the outer boundary calculation.
    - It plots histograms of the distance transforms.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Convert 1s to 255s
    binaryImage[binaryImage == 1] = 255
    newBinaryImage = binaryImage.copy()
    newBinaryImage[newBinaryImage == 255] = 1

    outerBoundary, _ = getOuterBoundary(binaryImage, 0)
    # Load outerBoundaryOriginal.mat

    #######################################################
    outerBoundary = load_mat('outerBoundaryOriginal.mat')
    outerBoundary = outerBoundary['outerBoundary']
    outerBoundary = outerBoundary - 1
    #######################################################

    for i in range(len(outerBoundary)):
        newBinaryImage[int(outerBoundary[i, 0])][int(outerBoundary[i, 1])] = 1
    D2, IDX2 = bwdist(newBinaryImage)
    D1, IDX1 = bwdist(~binaryImage)

    plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.hist(IDX1.ravel(), bins=96, range=(0.0, 480000), fc='k', ec='k',color='blue')
    plt.title("IDX1")
    plt.subplot(2, 2, 2)
    plt.hist(D2.ravel(), bins=2, range=(0.0, 2.0), fc='k', ec='k',color='blue')
    plt.title("D2")
    plt.subplot(2, 2, 3)
    plt.hist(D1.ravel(), bins=86, range=(0.0, 256), fc='k', ec='k',color='blue')
    plt.title("D1")
    plt.subplot(2, 2, 4)
    plt.hist(IDX2.ravel(), bins=96, range=(0.0, 480000), fc='k', ec='k',color='blue')
    plt.title("IDX2")
    plt.show()

    IDX1[D1 == 0] = 0
    IDX2[D2 == 0] = 0
    
    IDX = IDX1 + IDX2

    for i in range(len(outerBoundary)):
        linear_index = np.ravel_multi_index((int(outerBoundary[i, 0]), int(outerBoundary[i, 1])), IDX.shape)
        IDX[int(outerBoundary[i, 0])][int(outerBoundary[i, 1])] = linear_index

    D = D1 - D2
    return D, IDX