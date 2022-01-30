from bdantic import models
from typing import Any, Dict


def is_equal(obj1: Any, obj2: Any) -> bool:
    """Peforms a controlled deep comparison between two objects.

    Args:
        obj1: An object to compare against
        obj2: An object to compare against

    Returns:
        True if the objects are equal, False otherwise
    """
    return _to_dict(obj1) == _to_dict(obj2)


def _get_dict(obj: Any) -> Dict[Any, Any]:
    """Converts an object into a dictionary.

    This function is not gauranteed to run without errors. It assumes that the
    passed object will always have either an _asdict() method or a __dict__
    attribute. The test environment is controlled to ensure this is always the
    case.

    Args:
        obj: The object to convert to a dictionary

    Returns:
        A dictionary representation of the object
    """
    if "_asdict" in dir(obj) and callable(getattr(obj, "_asdict")):
        return obj._asdict()
    else:
        return obj.__dict__


def _is_recursable(obj: Any) -> bool:
    """Determines if an object should be recursed or not.

    This function is responsible for controlling the amount of recursion that
    occurs when comparing two objects. We're only interested in recursing
    through the controlled types within the test and not any other type.

    Args:
        obj: The object to check against

    Returns:
        Whether or not the object should be recursed or not
    """
    return (
        type(obj) in models.type_map.keys()
        or type(obj) in models.type_map.values()
    )


def _try_recurse(obj: Any) -> Any:
    """Recurses valid objects, otherwise returns the original object.

    Args:
        obj: The object to attempte recursion on

    Returns:
        A dictionary representation of the object if it's recursable, otherwise
        the original object is returned
    """
    return _to_dict(obj) if _is_recursable(obj) else obj


def _to_dict(obj: Any) -> Dict[Any, Any]:
    """Recursively converts an object into a dictionary representation.

    The conversion is controlled and not all children will be recursed. See
    notes for _is_recursable().

    Args:
        obj: The object to convert

    Returns:
        A dictionary representation of the object
    """
    new_dict: Dict[Any, Any] = {}
    if isinstance(obj, dict):
        d = obj
    else:
        d = _get_dict(obj)
    for key, value in d.items():
        if key == "ty":
            continue
        if isinstance(value, dict):
            new_dict[key] = {k: _try_recurse(v) for (k, v) in value.items()}
        elif isinstance(value, list):
            new_dict[key] = [_try_recurse(v) for v in value]
        elif _is_recursable(value):
            new_dict[key] = _to_dict(value)
        else:
            new_dict[key] = value

    return new_dict
