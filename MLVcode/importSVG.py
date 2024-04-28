import numpy as np
import cv2
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import math

# Local recursive function that traverses the SVG tree and fills in the vecLD data structure along the way
def parseChildNodes(theNode,vecLD,groupTransform):
    name = theNode['getNodeName'] # Check
    if name is not None:
        thisContour = []
        contourBreaks = 1
        if name == 'g':
            thisTransform = theNode['getAttribute']('transform') # Check
            if thisTransform is None:
                groupTransform = thisTransform
            else:
                groupTransform = groupTransform + ' ' + thisTransform

        elif name == 'svg':
            viewBox = theNode['getValue']('viewBox') # Check
            if viewBox is not None:
                vecLD['imsize'] = viewBox[2:3]

        elif name == 'line':
            thisContour = [0, 0, 0, 0]
            thisContour[0] = theNode['getValue']('x1')
            thisContour[1] = theNode['getValue']('y1')
            thisContour[2] = theNode['getValue']('x2')
            thisContour[3] = theNode['getValue']('y2')

        elif name == 'polygon' or name == 'polyline':
            points = theNode['getValue']('points') # Check
            x = points[0:1:-1]  # Check
            y = points[1:1:]  # Check

            # If polygon isn't closed, close it
            if name == 'polygon' and (x[-1] != x[0] or y[-1] != y[0]):
                x = np.append(x, x[0])
                y = np.append(y, y[0])
            thisContour = [(start_x, start_y, end_x, end_y) for (start_x, start_y), (end_x, end_y) in zip(zip(x[:-1], y[:-1]), zip(x[1:], y[1:]))]
            # If you prefer thisContour to be a numpy array instead of a list of tuples:
            thisContour = np.array(thisContour)

        elif name == 'rect':
            x = theNode['getValue']('x')
            y = theNode['getValue']('y')
            w = theNode['getValue']('width')
            h = theNode['getValue']('height')
            thisContour = [(x, y, x+w, y), (x+w, y, x+w, y+h), (x+w, y+h, x, y+h), (x, y+h, x, y)]

        elif name in ['circle','ellipse']:
            cs = theNode['getValue']('cx')
            cy = theNode['getValue']('cy')
            if name == 'circle':
                rx = theNode['getValue']('r')
                ry = rx
            else:
                rx = abs(theNode['getValue']('rx'))
                ry = abs(theNode['getValue']('ry'))
            numSeg = max(8, round(2 * math.pi * max(rx, ry)/5.0))
            dAng = 360 / numSeg
            angles = np.arange(0, 360, dAng)
            x = cs + rx * np.cos(angles)
            y = cy + ry * np.sin(angles)
            thisContour = [(start_x, start_y, end_x, end_y) for (start_x, start_y), (end_x, end_y) in zip(zip(x[:-1], y[:-1]), zip(x[1:], y[1:]))]

        elif name == 'path':
            commands = theNode['getValue']('d') # Check
            commands[commands == ','] = ' '
            idx = 1 # Maybe 0
            prevPos = []
            pathStartPos = []
            prevContr = []
            prevCom = ''
            nextCom = ''
            contourBreaks = []
            while (idx < len(commands) or nextCom is not None):
                if nextCom is not None:
                    # Read the command and coordinates from the command string
                    thisCom = commands[idx]
                    # [coords,~,~,nextidx] = sscanf(commands(idx+1:end),'%f');
                    idx = nextidx + idx
                else:
                    thisCom = nextCom
                    nextCom = ''
                if thisCom.lower() in ['M','m']:
                    x = coords[0:1:-1]
                    y = coords[1:1:]
                    contourBreaks = np.append(contourBreaks, len(thisContour)+1)
                    # Relative coords? cumulative addition of points
                    if thisCom.lower() == 'm':
                        if len(prevPos) > 0:
                            x[0] = prevPos[0] + x[0]
                            y[0] = prevPos[1] + y[0]
                        x = cumsum[x]
                        y = cumsum[y]
                    
                    # Add straight line segments if we have more than one point
                    if len(x) > 1:
                        new_segments = np.column_stack((x[:-1], y[:-1], x[1:], y[1:]))
                        # Append new segments to thisContour
                        thisContour = np.vstack((thisContour, new_segments))
                    prevPos = [x[-1], y[-1]]
                    pathStartPos = [x[0], y[0]]

                # Draw sequence of line segments
                elif thisCom.lower() in ['L','l']:
                    x = coords[0:1:-1]
                    y = coords[1:1:]
                    # Connect to previous point
                    x = [prevPos[0], x]
                    y = [prevPos[1], y]
                    # Relative coords? cumulative addition of points
                    if thisCom.lower() == 'l':
                        x = cumsum[x]
                        y = cumsum[y]

                    # Add straight line segments
                    new_segments = np.column_stack((x[:-1], y[:-1], x[1:], y[1:]))
                    thisContour = np.vstack((thisContour, new_segments))
                    prevPos = [x[-1], y[-1]]
                
                # Draw horizontal line(s)
                elif thisCom.lower() in ['H','h']:
                    x = [prevPos[0], coords]
                    x = x.flatten()
                    y = [prevPos[1]+np.zeros(len(x))]
                    # Flatten y
                    y = y.flatten()
                    if thisCom.lower() == 'h':
                        x = cumsum[x]
                    thisContour = np.vstack((thisContour, np.column_stack((x[:-1], y[:-1], x[1:], y[1:]))))
                    prevPos = [x[-1], y[-1]]

                # Draw vertical line(s)
                elif thisCom.lower() in ['V','v']:
                    y = [prevPos[1], coords]
                    y = y.flatten()
                    x = [prevPos[0]+np.zeros(len(y))]
                    x = x.flatten()
                    if thisCom.lower() == 'v':
                        y = cumsum[y]
                    thisContour = np.vstack((thisContour, np.column_stack((x[:-1], y[:-1], x[1:], y[1:]))))
                    prevPos = [x[-1], y[-1]]

                # Quadratic Bezier curves

                         



def importSVG(svgFilename, imsize=None):
    """
    Imports an SVG image into a vecLD structure.

    Parameters:
    - svgFilename (str): File name for an SVG file.
    - imsize (tuple, optional): The image size as (width, height). If not provided,
                                the image size will be determined from the SVG file.

    Returns:
    - vecLD (dict): A dictionary representing the vecLD data structure with the contours
                    from the SVG file. This structure typically includes keys for contours,
                    image size, and other relevant information extracted from the SVG.

    Note:
    This function is experimental and does not implement all aspects of the SVG standard.
    In particular, it does not translate any text, embedded images, shape fill, or gradients.
    Some aspects of this function are untested because suitable SVG files containing the
    relevant features were not available. If you encounter any errors, please email the SVG
    file you were trying to load to dirk.walther@gmail.com, and I will try my best to
    address the issue.

    This function is part of the Mid Level Vision Toolbox: http://www.mlvtoolbox.org

    Copyright:
    Dirk Bernhardt-Walther, University of Toronto, Toronto, Ontario, Canada, 2023.

    Contact:
    dirk.walther@gmail.com
    """

    # Prepare vecLD data structure
    vecLD = {}
    vecLD['originalImage'] = svgFilename
    vecLD['imsize'] = []
    vecLD['lineMethod'] = mFilename # Need to convert still from matlab
    vecLD['contours'] = []

    # Recursively parse the elements in the SVG file
    tree = ET.parse(svgFilename)
    # vecLD = parseChildNodes(tree,vecLD,''); # Need to convert still from matlab

    # If we have no valid image size, use the bounding box around all contours
    if imsize is not None:
        vecLD['imsize'] = imsize
    
    if len(vecLD['imsize']) == 0:
        maxX = -np.inf
        maxY = -np.inf
        for c in range(vecLD['numContours'][0][0]):
            thisCont = vecLD['contours'][c]
            maxX = max(maxX, max([thisCont[:,0], thisCont[:,2]]))
            maxY = max(maxY, max([thisCont[:,1], thisCont[:,3]]))
        vecLD['imsize'] = math.ceil([maxX, maxY])

    return vecLD

