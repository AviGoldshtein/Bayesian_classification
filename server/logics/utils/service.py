import numpy as np

def convert_numpy_types(obj):
    """
    Converts a nested dictionary/list structure that may contain NumPy types
    (like numpy floats, ints, arrays) to pure Python types.

    :param obj: A Python object (dict, list, np.integer, np.floating, np.ndarray)
    :return: Same structure with NumPy types converted to native Python types.
    """
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    elif isinstance(obj, np.ndarray):
        return convert_numpy_types(obj.tolist())
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    else:
        return obj
