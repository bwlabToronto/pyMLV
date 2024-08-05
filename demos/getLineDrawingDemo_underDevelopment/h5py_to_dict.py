import h5py

def h5py_to_dict(group):
    """
    Recursively converts an h5py group into a nested dictionary.

    This function traverses an HDF5 group and its subgroups, converting the structure into a 
    nested dictionary. Datasets within the HDF5 file are read into NumPy arrays, while groups 
    are recursively converted into dictionaries.

    Args:
        group (h5py.Group): The h5py group to convert. This could be the root group of an 
                            HDF5 file or any subgroup within it.

    Returns:
        dict: A nested dictionary where each key corresponds to an HDF5 dataset or subgroup. 
              Datasets are converted into NumPy arrays, and groups are represented as nested 
              dictionaries.

    Notes:
    - This function is useful for accessing and manipulating the contents of an HDF5 file 
      in a Python-native format, facilitating easy access to data without requiring direct 
      interaction with the HDF5 format.
    - Be mindful of memory usage when reading large datasets, as they are fully loaded into 
      memory as NumPy arrays.

    Raises:
        TypeError: If the input `group` is not an instance of `h5py.Group` or `h5py.File`.
        
        
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
    result = {}
    for key, item in group.items():
        if isinstance(item, h5py.Dataset):
            result[key] = item[()]  # Read dataset
        elif isinstance(item, h5py.Group):
            result[key] = h5py_to_dict(item)  # Recursively read group
    return result