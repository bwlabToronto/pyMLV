from MLVcode.computeOrientation import computeOrientation
from MLVcode.computeLength import computeLength
from MLVcode.computeCurvature import computeCurvature
from MLVcode.computeJunctions_FIX import computeJunctions
# from computeOrientation import computeOrientation
# from computeLength import computeLength
# from computeCurvature import computeCurvature


def computeContourProperties(vecLD, 
                             whichProps=['orientation', 'length', 
                                         'curvature', 'junctions']):
    """
    Computes contour properties for the vectorized line drawing.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        whichProps (str or list, optional): String or list of strings defining which properties to compute.
            Options are: 'orientation', 'length', 'curvature', 'junctions'.
            Default is ['orientation', 'length', 'curvature', 'junctions'].

    Returns:
        LineDrawingStructure: A vector LD of structs with the requested contour properties added.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
        
    if not isinstance(whichProps, (list, tuple)):
        whichProps = [whichProps]
    for prop in range(len(whichProps)):
        thisProp = whichProps[prop].lower()
        if thisProp == 'orientation':
            vecLD = computeOrientation(vecLD)
        elif thisProp == 'length':
            vecLD = computeLength(vecLD) 
        elif thisProp == 'curvature':
            vecLD = computeCurvature(vecLD) 
        elif thisProp == 'junctions':
            vecLD = computeJunctions(vecLD) # Need to write code for this
        else:
            raise ValueError('Unknown property: ' + thisProp)
    return vecLD