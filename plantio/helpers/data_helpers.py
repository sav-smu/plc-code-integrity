import json


def convert_key_value(inputDict, special_keys=[]):
    """
    Converts dictionary from PlantViz to key/value pair

    Parameters
    ----------
    inputDict : dict
        Dictionary containing all key, value and type for detector
        settings.
    special_keys : list, optional
        List containing keys to skip when encountered in `inputDict`.

    Returns
    -------
    dict
        Contains key/value pair.
    """
    returnDict = {}
    for key in inputDict:
        if key not in special_keys:
            returnDict[key] = inputDict[key]["value"]
    return returnDict


def json_deserializer(key, value, flags):
    """
    Deserializes JSON data

    Parameters
    ----------
    key : str
        Not used directly, but by pymemcache deserializer. This is the
        key that is used to store the value.
    value : any
        Value stored in memcached.
    flags : int
        Indicates the type of data.

    Raises
    ------
    Exception
        If no flags match, then error is raised.
    """
    if flags == 1 or flags == 0:
        return value.decode("utf-8")
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")


def json_serializer(key, value):
    """
    Serializes JSON data.

    Parameters
    ----------
    key : str
        Not used directly, but by pymemcache deserializer. This is the
        key that is used to store the value.
    value : any
        Value to be stored in memcached.

    Returns
    -------
    str
        String when type of value is string or will convert any data into
        string using json module.
    """
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2


def round_floats(obj):
    """
    Rounds all floats to 2 decimal places.

    Parameters
    ----------
    obj : any
        Object to be converted to 2 decimal places.

    Returns
    -------
    any
        Returns the input data but converted to 2 decimal places where
        possible.
    """
    if isinstance(obj, float):
        return round(obj, 2)
    if isinstance(obj, dict):
        return {k: round_floats(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [round_floats(x) for x in obj]
    return obj
