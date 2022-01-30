from beancount.core.data import Directive
from bdantic import models
from typing import Any, Dict, List, Sequence


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


def parse_entries(entries: List[Directive]) -> models.Entries:
    """Parses a list of directives into a Directives model.

    Args:
        entries: The list of directives as returned by the parser

    Returns:
        A Directives instance
    """
    return models.Entries.parse(entries)


def parse_loader(
    entries: List[Directive], errors: List[Any], options: Dict[str, Any]
) -> models.BeancountFile:
    """Parses the result from calling the beancount loader to a BeancountFile.

    Args:
        entries: The entries return from the loader
        errors: The errors returned from a loader
        options: The options returned from a loder

    Returns:
        A BeancountFile model
    """
    return models.BeancountFile.parse(entries, errors, options)
