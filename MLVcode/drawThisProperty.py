import warnings
from MLVcode.drawLinedrawing import drawLinedrawing
from MLVcode.drawLinedrawingProperty import drawLinedrawingProperty
from MLVcode.drawMATproperty import drawMATproperty

def drawThisProperty(vecLD, property):
    """
    Draws specific properties of a vectorized line drawing based on the specified property.

    This function allows for the visualization of various properties of a line drawing. 
    It supports basic drawing of the original line drawing as well as specific properties 
    like length, orientation, curvature, junctions, parallelism, separation, and mirror symmetry.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing data structure.
        property (str): The specific property to visualize. Supported properties include 
        'original', 'length', 'orientation', 'curvature', 'junctions', 'parallelism', 
        'separation', and 'mirror'. The function is case-insensitive.

    Returns:
        None: The function does not return a value but visualizes the specified property 
        of the line drawing.

    Raises:
        Warning: If an unknown property is specified, a warning is issued.

    Notes:
    - The function modifies the 'property' parameter by converting it to lowercase for 
      case-insensitive comparison.
    - Visualization is handled by different functions based on the property. 
      For 'original', it calls 'drawLinedrawing', for properties like 'length', 
      'orientation', 'curvature', and 'junctions', it calls 'drawLinedrawingProperty', 
      and for 'parallelism', 'separation', and 'mirror', it calls 'drawMATproperty'.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    property = property.lower()
    if property == 'original':
        drawLinedrawing(vecLD)
    elif property in ['length', 'orientation', 'curvature', 'junctions']:
        drawLinedrawingProperty(vecLD, property)
    elif property in ['parallelism', 'separation', 'mirror']:
        drawMATproperty(vecLD, property)
    else:
        warnings.warn('Unknown property: ' + property)
        return
    return