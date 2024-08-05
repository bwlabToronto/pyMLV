import numpy as np
import matplotlib.pyplot as plt

def drawMATproperty(vecLD,
                    property,
                    markerSize=1):
    """
    Draws a colored line drawing with line color determined by the MAT property
    indicated by 'property'.

    Args:
        vecLD (LineDrawingStructure): The vectorized line drawing.
        property (str): A string indicating the MAT property, which can be one of: 'mirror', 'parallelism', 'separation'.
        markerSize (int, optional): The size of the '.' marker used for drawing the property onto the contours. Default is 1.

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
    print(property)

    figureSize = [12, 12]
    fig, ax = plt.subplots(figsize=figureSize)
    ax.scatter(vecLD[property + '_allX'], vecLD[property + '_allY'], 
                s=markerSize, c=vecLD[property + '_allScores'], 
                cmap='jet')
    

    # Set axis properties
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap='jet')  # Create the ScalarMappable object
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_ticks([0, 0.5, 1])
    cbar.set_ticklabels(['lowest', 'intermediate', 'highest'])
    plt.title(property)

    plt.show()