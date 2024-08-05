import numpy as np
from tqdm import tqdm


def computeAOF(D, IDX, sphere_points, epsilon):
    """
    This function computes the gradient vector field with regard to a distance function.

    Parameters:
    D (array_like): Distance map computed with respect to the binary image.
    IDX (array_like): The index of the closest point to the boundary.
    sphere_points (array_like): Points on a sphere, used in the computation.
    epsilon (float): A small value used to stabilize computations.

    Returns:
    array_like: Flux image, a 2D matrix with average outward flux values computed 
    from the gradient vector field of a binary image.

    -----------------------------------------------------
    Notes:
    This function is part of the skeletonization package based on earlier work by Morteza Rezanejad.
    Check the GitHub repository at https://github.com/mrezanejad/AOFSkeletons for more details.

    License:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

    Author:
    Aravind Narayanan
    University of Toronto, Toronto, ON, 2024
    Contact: aravind [dot] narayanan [at] utoronto [dot] ca
    -----------------------------------------------------
    """

    # Initialise Q
    (m, n) = D.shape
    nOfSamples = sphere_points.shape[0]

    # For each point on the sphere create the normal vector
    normals = np.zeros(sphere_points.shape)
    fluxImage = np.zeros((m, n))

    for t in range(nOfSamples):
        normals[t, 0] = sphere_points[t, 0]
        normals[t, 1] = sphere_points[t, 1]
    
    for i in tqdm(range(m)):
        for j in range(n):
            flux_value = 0
            if D[i, j] > -1.5:
                if i + 1 > epsilon and j + 1 > epsilon and i + 1 < m - epsilon and j + 1 < n - epsilon:
                    # sum over dot product of normal and the gradient vector field (q-dot)
                    for ind in range(nOfSamples):
                        # A point on the sphere
                        px = i + sphere_points[ind, 0] + 0.5
                        py = j + sphere_points[ind, 1] + 0.5
                        # the indices of the grid cell that sphere points fall into
                        cI = int(px - 1)
                        cJ = int(py - 1)

                        bx, by = np.unravel_index(IDX[cI, cJ], D.shape)
                        # The vector connect them
                        qq = np.array([bx - px, by - py])
                        d = np.linalg.norm(qq)
                        if d != 0:
                            qq /= d
                        else:
                            qq = 0
                        flux_value += np.dot(qq, normals[ind])

            fluxImage[i, j] = flux_value

    return fluxImage