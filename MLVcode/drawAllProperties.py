import math
import warnings
import matplotlib.pyplot as plt
from MLVcode.drawThisProperty import drawThisProperty


def drawAllProperties(vecLD, mode='subplot', properties=['Original','Length',
                                               'Orientation','Curvature',
                                               'Junctions','Mirror',
                                               'Parallelism','Separation']):
    """
    Draws the original line drawing and all of its properties.

    Input:
        vecLD - the vectorized line drawing to be drawn
        mode - one of: 'subplot' - draw properties into one figure using subplot (default)
                       'separate' - draw properties into separate figures
        properties - a cell array of text labels of the properties to be drawn
                     default: ['Original', 'Length', 'Orientation', 'Curvature', 'Junctions', 'mirror', 'parallelism', 'separation']

    Return:
        figIDs - a vector of the figure IDs of the individual figures.
                 just one ID for mode = 'subplots'

    See also drawLinedrawing, drawLinedrawingProperty

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
    if not isinstance(properties, list):
        properties = [properties]
    numProps = len(properties)

    # Switch statement for the mode
    if mode == 'subplot':
        # ceil(sqrt(numProps))
        m = math.ceil(math.sqrt(numProps))
        n = math.ceil(numProps / m)
        # Define a figure
        # figIDs, ax = plt.subplots(m, n)
        for p in range(numProps):
            # plt.subplot(m, n, p+1)
            drawThisProperty(vecLD, properties[p])
    elif mode == 'separate':
        figIDs = []
        for p in range(numProps):
            figIDs.append(plt.figure())
            drawThisProperty(vecLD, properties[p])
    else:
        warnings.warn('Unknown mode: ' + mode)