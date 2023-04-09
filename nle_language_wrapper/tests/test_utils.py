import numpy as np


def str_to_1d(string):
    """Convert a string to equivalent numpy array
    Args:
        string(str): string to be converted
    Returns:
        (numpy.ndarray): 1-D uint8 values for unicode string input.
    """
    output = np.array(bytearray(string.encode("utf-8")))
    return output


def strs_to_2d(strings, fill_value=0):
    """Convert a list of strings to equivalent 2d numpy array
    Args:
        strings(List[str]): string to be converted
    Returns:
        (numpy.ndarray): 2-D uint8 values for unicode strings input.
    """
    arrays = []
    max_len = 0
    for string in strings:
        arrays.append(str_to_1d(string))
        if len(string) > max_len:
            max_len = len(string)
    output = np.full((len(arrays), max_len), fill_value=fill_value, dtype=np.uint8)
    for i, array in enumerate(arrays):
        output[i, : len(array)] = array
    return output
