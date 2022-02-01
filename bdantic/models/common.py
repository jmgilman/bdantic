from .base import Base
from typing import Any, Dict


def filter_dict(meta: Dict[Any, Any]) -> Dict:
    """Recursively filters a dictionary to remove non-JSON serializable keys.

    Args:
        d: The dictionary to filter

    Returns:
        The filtered dictionary
    """
    new_meta: Dict = {}
    for key, value in meta.items():
        if type(key) not in [str, int, float, bool, None]:
            continue
        if isinstance(value, dict):
            new_meta[key] = filter_dict(value)
        elif isinstance(value, list):
            new_meta[key] = [
                filter_dict(v) for v in value if isinstance(v, dict)
            ]
        else:
            new_meta[key] = value

    return new_meta


def is_named_tuple(obj: Any) -> bool:
    """Attempts to determine if an object is a NamedTuple.

    The method is not fullproof and attempts to determine if the given object
    is a tuple which happens to have _asdict() and _fields() methods. It's
    possible to generate false positives but no such case exists within the
    beancount package.

    Args:
        obj: The object to check against

    Returns:
        True if the object is a NamedTuple, False otherwise
    """
    return (
        isinstance(obj, tuple)
        and hasattr(obj, "_asdict")
        and hasattr(obj, "_fields")
    )


def recursive_parse(b: Any) -> Dict[str, Any]:
    """Recursively parses a BeancountType into a nested dictionary of models.

    Since a NamedTuple can be represented as a dictionary using the bultin
    _asdict() method, this function attempts to recursively convert a
    BeancountTuple and any children types into a nested dictionary structure.

    Args:
        b: The BeancountType to recursively parse

    Returns:
        A nested dictionary with all parsed models.
    """
    result: Dict[str, Any] = {}
    for key, value in b._asdict().items():
        if is_named_tuple(value):
            result[key] = recursive_parse(value)
        elif isinstance(value, list) and value:
            if is_named_tuple(value[0]):
                result[key] = [recursive_parse(c) for c in value]
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = filter_dict(value)
        else:
            result[key] = value

    return result


def recursive_export(b: Any) -> Dict[str, Any]:
    """Recursively exports a ModelTuple into a nested dictionary

    Args:
        b: The ModelTuple to recursively export

    Returns:
        A nested dictionary with all exported Beancount types
    """
    result: Dict[str, Any] = {}
    for key, value in b.__dict__.items():
        if key == "ty":
            continue
        elif key == "meta":
            if not isinstance(value, dict) and value:
                result[key] = value.dict(
                    by_alias=True, exclude_none=True, exclude_unset=True
                )
            else:
                result[key] = value
            continue
        if isinstance(value, Base):
            result[key] = value._sibling(**recursive_export(value))
        elif isinstance(value, list) and value:
            if isinstance(value[0], Base):
                result[key] = [
                    c._sibling(**recursive_export(c)) for c in value
                ]
            else:
                result[key] = value
        else:
            result[key] = value

    return result
