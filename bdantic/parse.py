from beancount.core.data import Directive
from bdantic import models
from typing import List, Sequence


def parse(obj: models.BeancountType) -> models.Model:
    """Parses a Beancount type into it's respective Pydantic models.

    Args:
        obj: A valid BeancountType

    Returns:
        The associated model for the given BeancountType
    """
    return models.type_map[type(obj)].parse(obj)  # type: ignore


def parse_all(objs: Sequence[models.BeancountType]) -> List[models.Model]:
    """Parses a list of Beancount types into a list of their respective
    Pydantic models.

    Args:
        objs: A list of valid BeancountType's

    Returns:
        A list of associated models for each BeancountType
    """
    return [parse(obj) for obj in objs]


def parse_entries(entries: List[Directive]) -> models.Directives:
    """Parses a list of directives into a Directives model.

    Args:
        entries: The list of directives as returned by the parser

    Returns:
        A Directives instance
    """
    return models.Directives.parse(entries)
