import numpy as np
import math

def averageProperty(vecLD,property):
    """
    Computes the average value of a specified property over an entire vectorized line drawing.

    This function calculates the mean of a specified property across all contours or 
    segments in a vectorized line drawing. The property to be averaged can be one of 
    several types, such as orientation, length, curvature, junctions, mirror, parallelism, 
    or separation.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        property (str): A string indicating the property to be computed. Valid options include:
            - 'orientation': Concatenate all straight line segments and return the orientation 
              of the resulting vector in degrees.
            - 'length': Average of the lengths of the individual contours in pixels.
            - 'curvature': Mean curvature over all line segments, weighted by the number of 
              pixels in the segments, in degrees per pixel.
            - 'junctions': Number of junctions per 10,000 pixels, computed as the sum over 
              normJunctionTypeHistogram.
            - 'mirror', 'parallelism', 'separation': Average value over all contour pixels, 
              a number between 0 and 1.

    Returns:
        float: The mean value of the specified property according to the descriptions above.

    Notes:
    - The computation of the average property varies based on the type of property specified.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2023

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """

    # Giving different results from MATLAB version
    if property.lower() == 'orientation': 
        # For orientation, all line segments get concatenated
        totalVec = np.array([0.0, 0.0])
        for c in range(vecLD['numContours'][0][0]):
            theseVec = vecLD['contours'][0][c][:, 3:4] - vecLD['contours'][0][c][:, 1:2]

            # For orientation we need to count line segments irrespective
            # of the direciton in which they were drawn. So all line
            # segments with an orientation angle between 180 and 360
            # degrees get reversed before they are added to the total
            # vector for the entire drawing.
            # If we didn't do this, an alongated closed rectangle would
            # have a totalVec of [0,0] - that's not what we mena by 
            # "average angle".
            reverseIdx = vecLD['orientations'][0][c] > 180
            reverseIdx = reverseIdx.flatten()
            theseVec[reverseIdx, :] = -theseVec[reverseIdx, :]
            totalVec += np.sum(theseVec, axis=0).flatten()
        meanProperty = math.degrees(math.atan2(-totalVec[1], totalVec[0])) % 180

        # overlaying mean orientation for debugging
        #hold on;
        #totalVec = totalVec/max(totalVec) * 200;
        #plot(400+[0,totalVec(1)],300+[0,totalVec(2)],'r-','LineWidth',3);

    # Matches MATLAB version
    elif property.lower() == 'length':
        meanProperty = np.mean(vecLD['contourLengths'])
    # Giving different results from MATLAB version
    elif property.lower() == 'curvature':
        meanProperty = 0
        for c in range(vecLD['numContours'][0][0]):
            meanProperty = meanProperty + sum(vecLD['curvatures'][0][c] * vecLD['lengths'][c])
        meanProperty = meanProperty / sum(vecLD['contourLengths'])
    # Matches MATLAB version
    elif property.lower() == 'junctions':
        meanProperty = sum(vecLD['normJunctionTypeHistogram'])
    # Matches MATLAB version
    elif property.lower() == 'mirror':
        meanProperty = np.mean(vecLD['mirror_allScores'])
    # Matches MATLAB version
    elif property.lower() == 'parallelism':
        meanProperty = np.mean(vecLD['parallelism_allScores'])
    # Matches MATLAB version
    elif property.lower() == 'separation':
        meanProperty = np.mean(vecLD['separation_allScores'])
    # Matches MATLAB version
    else:
        raise ValueError('Unknown property string: ' + property)
    

    return meanProperty