def getPrmDflt(prm, dfs, check_extra=0):
    """
    Merges user-specified parameters with default values, ensuring all required parameters are set.

    This function combines a set of user-specified parameters with default parameters, allowing 
    for flexible parameter management. It also includes optional checks to validate the user-specified 
    parameters against the defaults.

    Args:
        prm (list or dict): User-specified parameters. If a list is provided, it should be in the 
                            form of key-value pairs (e.g., `['param1', value1, 'param2', value2]`).
                            If a dictionary is provided, it should directly map parameter names to 
                            their values.
        dfs (list): Default parameters, provided as a list of key-value pairs. The length of `dfs` 
                    must be even.
        check_extra (int, optional): Determines how extra parameters are handled:
                                     - If `check_extra > 0`: Ensures no extra parameters are in `prm` 
                                       that are not in `dfs`. Raises an error if found.
                                     - If `check_extra < 0`: Adds any extra parameters in `prm` to the 
                                       output dictionary without raising an error.
                                     - If `check_extra == 0`: Only updates parameters present in both 
                                       `prm` and `dfs`.

    Returns:
        dict: A dictionary containing the merged parameters, with user-specified values overriding 
              the defaults where applicable.

    Raises:
        ValueError: If the length of `dfs` or `prm` (when provided as a list) is not even.
                    If a required parameter (denoted by 'REQ' in `dfs`) is missing in the final 
                    merged output.
        TypeError: If `prm` is neither a list nor a dictionary.

    Notes:
    - The function ensures that required parameters (those marked with 'REQ' in `dfs`) are specified 
      by the user. If not, it raises a `ValueError`.
    - The merging behavior can be customized via the `check_extra` argument, offering flexibility 
      in how strictly the parameters are managed.
      
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
    if len(dfs) % 2 != 0:
        raise ValueError('Odd number of default parameters')

    if isinstance(prm, list):
        if len(prm) % 2 != 0:
            raise ValueError('Odd number of parameters in prm')
        prm_dict = {prm[i]: prm[i + 1] for i in range(0, len(prm), 2)}
    elif isinstance(prm, dict):
        prm_dict = prm
    else:
        raise TypeError('prm must be a dict or a list')

    dfs_dict = {dfs[i]: dfs[i + 1] for i in range(0, len(dfs), 2)}

    if check_extra > 0:
        for key in prm_dict:
            if key not in dfs_dict:
                raise ValueError(f'Parameter {key} is not valid')
            dfs_dict[key] = prm_dict[key]
    elif check_extra < 0:
        for key in prm_dict:
            if key not in dfs_dict:
                dfs_dict[key] = prm_dict[key]
            else:
                dfs_dict[key] = prm_dict[key]
    else:
        for key in prm_dict:
            if key in dfs_dict:
                dfs_dict[key] = prm_dict[key]

    if 'REQ' in dfs_dict.values():
        missing = [k for k, v in dfs_dict.items() if v == 'REQ']
        raise ValueError(f"Required field '{missing[0]}' not specified.")

    return dfs_dict