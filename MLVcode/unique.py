import numpy as np



# Find number of distinc values in the 3D array and their counts
def unique3D(data):
    """
    Finds the number of distinct values in a 3D array and their counts.

    This function flattens a 3D array into a 1D array and then finds the unique values 
    in this array along with their counts.

    Args:
        data (numpy.ndarray): A 3D numpy array.

    Returns:
        tuple: A tuple (unique, counts) where:
            unique (numpy.ndarray): A 1D array of unique values found in the input data.
            counts (numpy.ndarray): The corresponding counts of each unique value.

    Notes:
    - The function first converts the 3D array to a 2D array and then to a 1D array before 
      finding the unique values.
    - It prints the shape of the flattened array for debugging purposes.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    # Flatten the 3D array to 1D
    data = data.reshape(-1, data.shape[-1])
    # Data is now 2D, make it 1D
    data = data.reshape(-1)
    print(data.shape)
    # Find unique values and their counts
    unique, counts = np.unique(data, axis=0, return_counts=True)
    return unique, counts

# Find number of distinc values in the 2D array and their counts
def unique2D(data):
    """
    Finds the number of distinct values in a 2D array and their counts.

    This function flattens a 2D array into a 1D array and then finds the unique values 
    in this array along with their counts.

    Args:
        data (numpy.ndarray): A 2D numpy array.

    Returns:
        tuple: A tuple (unique, counts) where:
            unique (numpy.ndarray): A 1D array of unique values found in the input data.
            counts (numpy.ndarray): The corresponding counts of each unique value.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    unique, counts = np.unique(data.reshape(-1, data.shape[-1]), axis=0, return_counts=True)
    return unique, counts

# Find number of distinc values in the 1D array and their counts
def unique1D(data):
    """
    Finds the number of distinct values in a 1D array and their counts.

    This function finds the unique values in a 1D array and their corresponding counts.

    Args:
        data (numpy.ndarray): A 1D numpy array.

    Returns:
        tuple: A tuple (unique, counts) where:
            unique (numpy.ndarray): A 1D array of unique values found in the input data.
            counts (numpy.ndarray): The corresponding counts of each unique value.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    unique, counts = np.unique(data, return_counts=True)
    return unique, counts