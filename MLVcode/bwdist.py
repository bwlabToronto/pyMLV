import numpy as np
from scipy.ndimage import distance_transform_edt


# BWDist
def bwdist(mat):
    d, labels =distance_transform_edt(
        mat==0, return_distances=True, return_indices=True)
    # print("d: \n", d)
    # print("labels: \n", labels)
    idx = np.zeros(mat.shape, dtype=np.intp)
    for row in range(mat.shape[0]):
        for col in range(mat.shape[1]):
            idx[row, col] = labels[0][row, col] * mat.shape[1] + labels[1][row, col]
    # print("IDX: \n", idx)
    return d, idx