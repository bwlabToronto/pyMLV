import pandas as pd
import numpy as np


def histogramToTable(histogram,shortName,bins=[]):
    """
    Converts a histogram into a table with variable names constructed from 
    a short name and, optionally, bin names.

    This function takes a histogram array and converts it into a structured table (DataFrame in Python). 
    The column names of the table are constructed using a provided short name and, if provided, the 
    names of the histogram bins.

    Args:
        histogram (numpy.ndarray): An N x M array containing N histograms with M bins each.
        shortName (str): A string with a short name that is used to create variable names for the table. 
                         E.g., 'ori' for orientation.
        bins (list or numpy.ndarray, optional): The names of the histogram bins. Can be a numerical array 
                                                or a list/array of strings. If bins is provided, the 
                                                variable names are constructed as shortName_bin. If bins 
                                                is omitted or empty, variable names are constructed as 
                                                shortName_1, shortName_2, etc.

    Returns:
        pandas.DataFrame: The histogram converted into a table (DataFrame) of size N x M.

    Notes:
    - The function is useful for converting raw histogram data into a more readable and structured table format.
    - The function assumes that the histogram array and bins (if provided) are aligned correctly in terms of dimensions.

    -----------------------------------------------------
    This function is part of the Mid Level Vision Toolbox:
    http://www.mlvtoolbox.org

    Copyright Dirk Bernhardt-Walther
    University of Toronto, Toronto, Ontario, Canada, 2022

    Contact: dirk.walther@gmail.com
    -----------------------------------------------------
    """
    numVar = histogram.shape[1]
    varNames = []
    for v in range(numVar):
        if len(bins) == 0:
            varNames.append(f'{shortName}_{v+1}')
        else:
            if isinstance(bins, list) or isinstance(bins, tuple):
                if isinstance(bins[v], (int, float)):
                    varNames.append(f'{shortName}_{bins[v]}')
                elif isinstance(bins[v], str):
                    varNames.append(f'{shortName}_{bins[v]}')
                else:
                    raise ValueError(f"Don't know how to handle bin names of type: {type(bins[v])}")
            else:
                raise ValueError(f"Don't know how to handle bins of type: {type(bins)}")
            
    return pd.DataFrame(histogram,columns=varNames)