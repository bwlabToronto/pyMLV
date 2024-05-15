import numpy as np


def recursive_classes(j, merge_matrix, is_junction_available):
    if not is_junction_available[j]:
        return [], merge_matrix, is_junction_available

    is_junction_available[j] = False
    all_js = [j]
    new_js = np.where(merge_matrix[j, :])[0]

    merge_matrix[j, :] = False
    merge_matrix[:, j] = False

    for nj in new_js:
        additional_js, merge_matrix, is_junction_available = recursive_classes(nj, merge_matrix, is_junction_available)
        all_js.extend(additional_js)

    return all_js, merge_matrix, is_junction_available

def cleanupJunctions(junctions, thresh=2):
    """
    Cleans up junctions by merging junctions that are within `thresh` pixels of each other.

    Parameters:
        junctions (list of dicts): Junctions as computed by detectJunctions, where each junction is a dictionary
                                   containing at least the 'position' key with [x, y] coordinates.
        thresh (float): The threshold for merging junctions, in pixels. Default value is 2.

    Returns:
        list of dicts: Cleaned up and merged junctions.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    thresh_squared = thresh ** 2
    num_junctions = len(junctions)
    merge_matrix = np.zeros((num_junctions, num_junctions), dtype=bool)

    # Calculate which junctions need to be merged
    for j1 in range(num_junctions):
        for j2 in range(j1 + 1, num_junctions):
            if np.sum((np.array(junctions[j1]['position']) - np.array(junctions[j2]['position']))**2) <= thresh_squared:
                merge_matrix[j1, j2] = True

    # Determine equivalence classes
    equivalence_classes = []
    is_junction_available = np.ones(num_junctions, dtype=bool)

    while np.any(merge_matrix):
        j1 = np.where(merge_matrix)[0][0]
        new_class, merge_matrix, is_junction_available = recursive_classes(j1, merge_matrix, is_junction_available)
        equivalence_classes.append(new_class)

    # Initialize the resulting junctions with all junctions that do not have neighbors
    cleaned_junctions = [junctions[i] for i in range(num_junctions) if is_junction_available[i]]

    # Merge junctions that are in equivalence classes
    for this_class in equivalence_classes:
        all_positions = np.array([junctions[j]['position'] for j in this_class])
        this_junct = {
            'position': np.mean(all_positions, axis=0).tolist(),
            'contourIDs': [],
            'segmentIDs': []
        }

        # Combine contour segments
        contour_segment_set = set()
        for j in this_class:
            for contour_id, segment_id in zip(junctions[j]['contourIDs'], junctions[j]['segmentIDs']):
                if (contour_id, segment_id) not in contour_segment_set:
                    contour_segment_set.add((contour_id, segment_id))
                    this_junct['contourIDs'].append(contour_id)
                    this_junct['segmentIDs'].append(segment_id)

        cleaned_junctions.append(this_junct)

    return cleaned_junctions
