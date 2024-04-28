import numpy as np
import matplotlib.pyplot as plt
from MLVcode.drawLinedrawing import drawLinedrawing
import warnings


def drawJunctions(Junctions,
                  types = ['T', 'Y', 'X', 'Arrow', 'Star'],
                  MarkerSize = 10,
                  colors = None):
    """
    Draws the junctions into the current figure.

    Args:
        Junctions (array or LineDrawingStructure): The junctions to be drawn. E.g., from vecLD.junctions.
            Alternatively, you can provide the entire vectorized line drawing with the junctions included (LineDrawingStructure).

        types (list of str, optional): A list of junction types to be drawn in order. You can use any combination of 'T', 'Y', 'X', 'Arrow', 'Star'.
            Default is an empty list, which means all junctions are drawn.

        MarkerSize (int, optional): The size of the marker for the junctions. Default is 5.

        colors (array-like, optional): An Nx3 array of RGB values to be used as colors for the markers.
            Default is to use the default color map specified by Matplotlib for line plots.

    Returns:
        None

    See also:
        drawLinedrawing
        drawLinedrawingProperty

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright (c) 2022 Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Need to edit and verify this function
    if not isinstance(types, (list, tuple)):
        types = [types]
    
    # Special case of a vectorized line drawing
    if 'contours' in Junctions.dtype.names:
        drawLinedrawing(Junctions)
        Junctions = Junctions['junctions']
    
    if len(Junctions[0]) == 0:
        warnings.warn('No junctions to plot.')

    junctionTypes = [j['type'] for j in Junctions]

    types = np.unique(junctionTypes)

    if colors is None:
        default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        colors = [default_colors[i % len(default_colors)] for i in range(len(types))]

    
    positions = np.array([j['position'] for j in Junctions[0]]).reshape(-1,2)
    h = []
    for t in range(len(types)):
        typeIdx = [types[t] == junction_type for junction_type in junctionTypes]
        trueIdx = np.where(typeIdx)
        Idx = positions[trueIdx[1]]
       
        color_Idx = np.repeat([colors[t]], len(Idx), axis=0)
        plot = plt.scatter(Idx[:,0], Idx[:,1],
                            c=color_Idx,  # Repeat the color for each matching position
                            s=MarkerSize*2,
                            marker='o',
                            edgecolors=colors[t],
                            alpha=1.0)
        h.append(plot)

    # Put a legend to the right of the current axis
    plt.legend(h,types,loc='center left', bbox_to_anchor=(1, 1))
    plt.title('Junctions')


    # plt.legend(h, types)
    plt.gca().get_legend().set_visible(True)

    plt.show()