from pydantic import BaseModel
from typing import Any, List, Type


class Ctx(BaseModel):
    """Holds contextual information when comparing values.

    Attributes:
        partial: The type of comparison to perform
        recurse: The types of objects to recursively compare
    """

    partial: bool = True
    recurse: List[Type] = []

    def is_recurse(self, obj1: Any, obj2: Any) -> bool:
        """Returns whether or not the two objects should be recursed.

        Args:
            obj1: An object to check
            obj2: An object to check

        Returns:
            True if the objects should be recursed, False otherwise
        """
        return type(obj1) in self.recurse or type(obj2) in self.recurse


def compare(obj1: Any, obj2: Any, ctx: Ctx) -> None:
    """Compares two objects by asserting equality.

    The type of comparison performed is dependent on the types of the passed
    objects and information contained within the context. Objects that are
    recursible will have their attributes compared, dictionaries and lists will
    be iterated over to find recursible objects and keys/values will be
    asserted to be equal, all other types will be asserted to be equal to each
    other.

    Args:
        obj1: The first object to compare
        obj2: The second object to compare
        ctx: The comparison context

    Raises:
        AssertionError when an equality check fails
    """
    if ctx.is_recurse(obj1, obj2):
        compare_object(obj1, obj2, ctx)
    elif isinstance(obj1, dict) and isinstance(obj2, dict):
        compare_dict(obj1, obj2, ctx)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        compare_list(obj1, obj2, ctx)
    else:
        assert obj1 == obj2


def compare_dict(dict1, dict2, ctx: Ctx) -> None:
    """Compares two dictionaries, asserting they are equal.

    Args:
        dict1: The first dictionary to compare
        dict2: The second dictionary to compare
        ctx: The comparison context

    Raises:
        AssertionError when an equality check fails
    """
    assert not set(dict1.keys()).difference(set(dict2.keys()))
    for key in dict1:
        compare(dict1[key], dict2[key], ctx)


def compare_list(list1, list2, ctx: Ctx) -> None:
    """Compares two lists, asserting they are equal.

    Args:
        list1: The first list to compare
        list2: The second list to compare
        ctx: The comparison context

    Raises:
        AssertionError when an equality check fails
    """
    assert len(list1) == len(list2)
    for i in range(len(list1)):
        compare(list1[i], list2[i], ctx)


def compare_object(obj1: Any, obj2: Any, ctx: Ctx) -> None:
    """Compares two objects, asserting they are equal.

    Objects are compared by iterating over their attributes and asserting
    equality. If the context is set to partial, only attributes which the two
    objects share will be asserted equal. Attributes which are lists or
    dictionaries will be recursively checked. Nested objects are only recursed
    if their types are found in the recurse attribute of the given context.

    Args:
        obj1: The first object to compare
        obj2: The second object to compare
        ctx: The comparison context

    Raises:
        AssertionError when an equality check fails
    """

    def is_valid_attr(k: str, obj: Any) -> bool:
        if k.startswith("__"):
            return False
        elif callable(getattr(obj, k)):
            return False
        return True

    attr1 = set([attr for attr in dir(obj1) if is_valid_attr(attr, obj1)])
    attr2 = set([attr for attr in dir(obj2) if is_valid_attr(attr, obj2)])

    if not ctx.partial:
        assert not attr1.difference(
            attr2
        ), "Objects have dissimilar attributes"
        attrs = attr1
    else:
        attrs = attr1.intersection(attr2)

    for attr in attrs:
        val1 = getattr(obj1, attr)
        val2 = getattr(obj2, attr)

        compare(val1, val2, ctx)
