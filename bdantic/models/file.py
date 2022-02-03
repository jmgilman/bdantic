from __future__ import annotations

from .base import Base, BaseDict, BaseList
from beancount.core import data
from bdantic.types import ModelDirective, OptionValues, type_map
from typing import Any, Dict, List, Tuple


class Directives(BaseList, smart_union=True):
    """A model representing a list of directives."""

    __root__: List[ModelDirective]

    @classmethod
    def parse(cls, obj: List[data.Directive]) -> Directives:
        """Parses a list of beancount directives into this model

        Args:
            obj: The Beancount directives to parse

        Returns:
            A new instance of this model
        """
        dirs = []

        dirs = [type_map[type(d)].parse(d) for d in obj]  # type: ignore
        return Directives(__root__=dirs)

    def export(self) -> List[data.Directive]:
        """Exports this model into a list of beancount directives

        Returns:
            The list of beancount directives
        """
        dirs = [d.export() for d in self.__root__]
        return dirs


class Options(BaseDict, smart_union=True):
    """A model representing a dictionary of options."""

    __root__: Dict[str, OptionValues]

    @classmethod
    def parse(cls, obj: Dict[str, Any]) -> Options:
        """Parses a dictionary of beancount options into this model

        Args:
            obj: The Beancount options to parse

        Returns:
            A new instance of this model
        """
        d = {}
        for key, value in obj.items():
            if type(value) in type_map.keys():
                d[key] = type_map[type(value)].parse(value)
            else:
                d[key] = value

        return Options(__root__=d)

    def export(self) -> Dict[str, Any]:
        """Exports this model into a dictionary of beancount options

        Returns:
            The dictionary of beancount options
        """
        d = {}
        for key, value in self.__root__.items():
            if type(value) in type_map.values():
                d[key] = value.export()  # type: ignore
            else:
                d[key] = value

        return d


class BeancountFile(Base):
    """A model representing the contents of an entire beancount file."""

    entries: Directives
    options: Options
    errors: List[Any]

    @classmethod
    def parse(
        cls,
        obj: Tuple[List[data.Directive], List[Any], Dict[str, Any]],
    ) -> BeancountFile:
        """Parses the results of loading a beancount file into this model.

        Args:
            obj: The results from calling the beancount loader

        Returns:
            A new instance of this model
        """
        return BeancountFile(
            entries=Directives.parse(obj[0]),
            options=Options.parse(obj[2]),
            errors=obj[1],
        )

    def export(self) -> Tuple[List[data.Directive], List[Any], Dict[str, Any]]:
        """Exports this model into it's original counterpart

        Returns:
            The entries, errors, and options from the original loader
        """
        return (self.entries.export(), self.errors, self.options.export())
