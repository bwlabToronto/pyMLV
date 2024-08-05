import scipy.io as sio

def load_mat(filename):
    """
    Loads a MATLAB file (.mat) and returns its contents.

    This function reads a specified .mat file and returns its contents as a dictionary. 
    The keys in the dictionary correspond to variable names stored in the .mat file.

    Args:
        filename (str): The path and name of the .mat file to be loaded.

    Returns:
        dict: A dictionary containing variables loaded from the .mat file.

    Notes:
    - This function uses SciPy's `loadmat` method from the `io` module.
    - The .mat file should be in MATLAB format (version 5 and above).

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
    mat = sio.loadmat(filename)
    return mat