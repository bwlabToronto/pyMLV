import numpy as np
import matplotlib.pyplot as plt


def drawLinedrawing(vecLD,
                    lineWidth=1,
                    color = [0,0,0]):
    """
    Draws a line drawing from a data structure into a figure.

    Args:
        vecLD (LineDrawingStructure): A line drawing structure.
        linewidth (int, optional): The width of the contour lines in pixels. Default is 1.
        color (list of int, optional): The RGB color for drawing the contours. Default is [0, 0, 0] (black).

    Returns:
        None

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright (c) 2022 Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    fig, ax = plt.subplots()
    for i in range(vecLD['numContours'][0][0]):
        thisC = vecLD['contours'][0][i]
        X_1 = thisC[:,0]
        Y_1 = thisC[:,1]
        X_2 = thisC[-1:,2]
        Y_2 = thisC[-1:,3]
        X = np.concatenate((X_1, X_2))
        Y = np.concatenate((Y_1, Y_2))
        ax.plot(X, Y,'-' , color=color, linewidth=lineWidth)

    ax.set_aspect('equal')
    ax.set_xlim([0, vecLD['imsize'][0][0]])
    ax.set_ylim([0, vecLD['imsize'][0][1]])
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')  
    plt.title('Original - '+vecLD['originalImage'][0])