import numpy as np
import math
import cv2
from scipy import ndimage
from skimage import io
from skimage import morphology
from skimage.morphology import skeletonize
from MLVcode.computeGradientVectorField import computeGradientVectorField
from MLVcode.sample_sphere_2D import sample_sphere_2D
from MLVcode.computeAOF import computeAOF



def extract2DSkeletonFromBinaryImage(binaryImage,threshold):
    """
    Extracts a 2D skeleton from a binary image.

    This function performs skeletonization on a binary image, yielding the average 
    outward flux image, the skeleton image, a distance-transformed image, and a thinned 
    binary image. The skeletonization process is influenced by the specified threshold.

    Args:
        binaryImage (numpy.ndarray): A binary image where the objects are marked with 1's and 
        the background is marked with 0's.
        threshold (float): A threshold value used in the skeletonization process.

    Returns:
        tuple: A tuple (fluxImage, skeletonImage, distImage, thin_boundary) where:
            fluxImage (numpy.ndarray): Average outward flux image computed from the distance transform.
            skeletonImage (numpy.ndarray): A binary image of the same size as binaryImage, 
            with 1's representing the skeleton.
            distImage (numpy.ndarray): A distance-transformed image of the same size as binaryImage.
            thin_boundary (numpy.ndarray): A thinned version of the binary image.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Python Implementation: Aravind Narayanan
    Original MATLAB Implementation: Dirk Bernhardt-Walther
    Copyright: Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2024

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Skeletonization package from earlier work of Morteza Rezanejad
    Check the https://github.com/mrezanejad/AOFSkeletons
    """
    inverted_binary = ~binaryImage.astype(bool)
    skeleton = skeletonize(inverted_binary, method='lee').astype(np.uint8)
    thin_boundary = cv2.bitwise_not(skeleton)
    print("Plotting the skeleton ...")
    io.imshow_collection([thin_boundary], cmap='gray')
    io.show()
    print("Skeleton is plotted.")
    number_of_samples = 60
    epsilon = 1
    fraction = 0.025
    area_threshold = max(math.floor(fraction * max(binaryImage.shape[0], binaryImage.shape[1])), 1)
    print("Area threshold is: ", area_threshold)
    # Computing Gradient Vector Field
    print('Distance function and gradient vector field is being computed ...\n')
    distImage, IDX = computeGradientVectorField(thin_boundary)
    ###############################################
    # Consider a sphere with radius 1 with some sample points on that
    sphere_points = sample_sphere_2D(number_of_samples)
    # Computing Average outward flux
    # Print "DONE"
    print('Average outward flux is being computed ...\n')
    fluxImage = computeAOF(distImage, IDX, sphere_points, epsilon)
    print('Average outward flux is computed.\n')
    # Print first 2 rows of fluxImage
    print("Flux Image: \n", fluxImage[:2])
    skeletonImage = fluxImage
    skeletonImage[skeletonImage < threshold*number_of_samples] = 0
    skeletonImage[skeletonImage >= threshold*number_of_samples] = 1
    # Skeletonize the image
    thin_boundary = morphology.skeletonize(skeletonImage)
    # Convert to uint8
    thin_boundary = thin_boundary.astype(np.uint8) * 255
    # PLot the skeleton
    io.imshow_collection([thin_boundary], cmap='gray')
    io.show()
    # Refine the skeleton
    # Convrt to bool
    skeletonImage = (skeletonImage > 0).astype(bool)
    area_threshold = 100  # Adjust this value according to your needs (NEED TO FIX THIS)
    skeletonImage = morphology.remove_small_objects(skeletonImage, min_size=area_threshold) 
    return fluxImage,skeletonImage,distImage,thin_boundary