import numpy as np
import matplotlib.pyplot as plt
from MLVcode.drawLinedrawing import drawLinedrawing
from MLVcode.drawJunctions import drawJunctions
from MLVcode.computeColorIndex import computeColorIndex
import warnings

def drawLinedrawingProperty(vecLD,
                            property,
                            lineWidth=1):
    """
    Draws a colored line drawing with line color determined by a specified property
    from a data structure into a figure.

    Args:
        vecLD (LineDrawingStructure): A line drawing structure.
        property (str): The property to determine line color, which can be one of 'orientation', 'length', 'curvature', 'junctions'.
        lineWidth (int, optional): The width of the contour lines in pixels. Default is 1.

    Returns:
        None

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
    property = property.lower()
    # Junctions are treated differently
    if property in ['junctions']:
        drawLinedrawing(vecLD, lineWidth, [0, 0, 0])
        drawJunctions(vecLD['junctions'])
        return 
    
    # Get the color index
    colorIdx, cmap = computeColorIndex(vecLD, property)
    for i in range(len(colorIdx)):
        colorIdx[i] = colorIdx[i].astype(np.int64)
    # Draw the line segments one at a time
    fig, ax = plt.subplots()
    for i in range(vecLD['numContours'][0][0]):
        thisC = vecLD['contours'][0][i]
        for s in range(len(thisC)):
            X = [thisC[s,0], thisC[s,2]]
            Y = [thisC[s,1], thisC[s,3]]
            ax.plot(X, Y,'-' , color=cmap(colorIdx[i][s]), linewidth=lineWidth)

    ax.tick_params(axis='both', which='both', length=0)
    sm = plt.cm.ScalarMappable(cmap=cmap)  # Create the ScalarMappable object
    cbar = plt.colorbar(sm, ax=ax)  # Assign the colorbar to the same axes


    if property == 'length':
        cbar.set_ticks([0,1])
        cbar.set_ticklabels(['short','long'])
    elif property == 'curvature':
        cbar.set_ticks([0,1])
        cbar.set_ticklabels(['straight','angular'])
    elif property == 'orientation':
        cbar.set_ticks([0, 0.5, 1])
        cbar.set_ticklabels(['horizontal', 'vertical', 'horizontal'])
    else:
        warnings.warn('Unknown Property: ' + property)
        return
    # ax.invert_xaxis()
    # Set axis limits
    ax.set_xlim([0, vecLD['imsize'][0][0]])
    ax.set_ylim([0, vecLD['imsize'][0][1]])
    ax.invert_yaxis()
    # Title 
    ax.set_title(property)
    # return fig, ax
    plt.show()