import numpy as np


def computeJunctionAnglesTypes(junctions, vec_ld):
    """
    Computes the types and angles for the junctions and adds them to the junctions
    data structure.

    Parameters:
        junctions (list of dicts): The detected and cleaned up junctions.
        vecLD (dict): The line drawing data structure for looking up line orientations and lengths.

    Returns:
        list of dicts: The same junctions with fields for types, minAngle, and maxAngle added.
                       Junction type is based on maxAngle 'a', categorized as:
                        - 'T': T junction - three segments: 160 < a < 200
                        - 'Arrow': arrow junctions - three segments: a > 200
                        - 'Y': Y junctions - three segments: a < 160
                        - 'X': X junctions - four segments.
                        - 'Star': Star junctions - more than four segments

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
    thresh = 2
    thresh_squared = thresh ** 2
    remove_junctions = []

    for j in range(len(junctions)):
        junction = junctions[j]
        junction_oris = []
        p = np.array(junction['position'])

        for s in range(len(junction['segmentIDs'])):
            seg_id = junction['segmentIDs'][s]
            this_c = junction['contourIDs'][s]
            this_s = seg_id

            # Segment coordinates
            this_seg = np.array(vec_ld['contours'][0][this_c][this_s])
            dist1 = np.sum((p - this_seg[:2])**2)
            dist2 = np.sum((p - this_seg[2:])**2)

            # Check proximity to segment endpoints
            if dist1 < thresh_squared:
                junction_oris.append(vec_ld['orientations'][this_c][this_s] % 360)
                if this_s > 0:  # Check previous segment if exists
                    # Prevent double consideration of the segment if it was already processed
                    if not any((cid == this_c and sid == this_s - 1) for cid, sid in zip(junction['contourIDs'], junction['segmentIDs'])):
                        prev_orientation = (vec_ld['orientations'][this_c][this_s-1] + 180) % 360
                        junction_oris.append(prev_orientation)

            elif dist2 < thresh_squared:
                next_orientation = (vec_ld['orientations'][this_c][this_s] + 180) % 360
                junction_oris.append(next_orientation)
                if this_s + 1 < len(vec_ld['contours'][0][this_c]):  # Check next segment if exists
                    # Again, check if the segment has not been already considered
                    if not any((cid == this_c and sid == this_s + 1) for cid, sid in zip(junction['contourIDs'], junction['segmentIDs'])):
                        junction_oris.append(vec_ld['orientations'][this_c][this_s+1] % 360)

            else:
                orientation1 = np.degrees(np.arctan2(p[1] - this_seg[1], p[0] - this_seg[0])) % 360
                orientation2 = np.degrees(np.arctan2(p[1] - this_seg[3], p[0] - this_seg[2])) % 360
                junction_oris.append(orientation1)
                junction_oris.append(orientation2)

        # Calculate angles and sort orientations
        if junction_oris:
            junction_oris = np.sort(junction_oris)
            angles = np.mod(np.diff(junction_oris, append=[junction_oris[0] + 360]), 360)
            min_angle = np.min(angles)
            max_angle = np.max(angles)

            # Assign computed values back to junction
            junction['angles'] = angles
            junction['minAngle'] = min_angle
            junction['maxAngle'] = max_angle

            # Determine junction type based on angles and number of segments
            num_angles = len(angles)
            if num_angles == 2:
                remove_junctions.append(j)
            elif num_angles == 3:
                if max_angle < 160:
                    junction['type'] = 'Y'
                elif max_angle <= 200:
                    junction['type'] = 'T'
                else:
                    junction['type'] = 'Arrow'
            elif num_angles == 4:
                junction['type'] = 'X'
            elif num_angles > 4:
                junction['type'] = 'Star'
        else:
            remove_junctions.append(j)  # Optionally remove junctions with no orientations calculated

    # Remove junctions that should not be classified (e.g., simple bends)
    return [junction for i, junction in enumerate(junctions) if i not in remove_junctions]
