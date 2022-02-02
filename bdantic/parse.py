from beancount.core import data, realization
from bdantic.models.file import Entries, BeancountFile
from bdantic.models.realize import RealAccount
from bdantic.types import type_map
from bdantic.types import BeancountType, Model
from typing import Any, Dict, List, Sequence


def export(model: Model) -> BeancountType:
    """Exports a Model to its respective BeancountType.

    Args:
        model: A valid Model

    Returns:
        The associated BeancountType for this Model
    """
    return model.export()


def export_all(models: Sequence[Model]) -> List[BeancountType]:
    """Exports a list of Models into a list of their respective BeancountType.

    Args:
        models: A list of Models

    Returns:
        A list of associated BeancountType's for each model
    """
    return [export(model) for model in models]


def parse(obj: BeancountType) -> Model:
    """Parses a BeancountType into it's respective Model.

    Args:
        obj: A valid BeancountType

    Returns:
        The associated Model for the given BeancountType
    """
    return type_map[type(obj)].parse(obj)  # type: ignore


def parse_all(
    objs: Sequence[BeancountType],
) -> List[Model]:
    """Parses a list of BeancountTypes's into a list of their respective
    Models.

    Args:
        objs: A list of valid BeancountType's

    Returns:
        A list of associated Models for each BeancountType
    """
    return [parse(obj) for obj in objs]


def parse_entries(entries: List[data.Directive]) -> Entries:
    """Parses a list of directives into a Directives model.

    Args:
        entries: The list of directives as returned by the parser

    Returns:
        A Directives instance
    """
    return Entries.parse(entries)


def parse_loader(
    entries: List[data.Directive], errors: List[Any], options: Dict[str, Any]
) -> BeancountFile:
    """Parses the result from calling the beancount loader to a BeancountFile.

    Args:
        entries: The entries return from the loader
        errors: The errors returned from a loader
        options: The options returned from a loder

    Returns:
        A BeancountFile model
    """
    return BeancountFile.parse(entries, errors, options)


def parse_realize(real_acct: realization.RealAccount) -> RealAccount:
    """Parses the response from running realize() on a list of entries.

    Args:
        real_acct: The realization.RealAccount to parse

    Returns:
        A RealAccount model
    """
    return RealAccount.parse(real_acct)
