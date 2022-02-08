"""Provides models for representing the contents of a parsed beancount file."""

from __future__ import annotations

from .base import Base, BaseDict, BaseList
from beancount.core import data
from bdantic.types import ModelDirective, OptionValues, type_map
from typing import Any, Dict, List, Tuple


class Directives(BaseList, smart_union=True):
    """A model representing a list of directives.

    This models wraps the entries response often returned when loading the
    content of a beancount file. It holds a list of various valid directive
    models.
    """

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

    def get(self, id: str) -> ModelDirective:
        """Returns the directive with the given ID.

        Args:
            id: The directive ID.

        Raises:
            IDNotFoundError: If the given ID was not found.

        Returns:
            The directive.
        """
        id_map = {d.id: d for d in self}
        if id not in id_map:
            raise IDNotFoundError(f"Failed to find directive with ID: {id}")

        return id_map[id]

    def get_all(self, ids: List[str]) -> List[ModelDirective]:
        """Returns a list of directives matching the given ID's.

        Args:
            ids: A list of ID's to get.

        Raises:
            IDNotFoundError: If any of the given ID's were not found.

        Returns:
            A list of the directives.
        """
        result = []
        for id in ids:
            result.append(self.get(id))

        return result


class Options(BaseDict, smart_union=True):
    """A model representing a dictionary of options.

    This model wraps the options often returned when loading the content of a
    beancount file. Options which contain raw beancount types are automatically
    parsed into their respective model.
    """

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
    """A model representing the contents of an entire beancount file.

    This model provides an interface for accessing the result returned when
    loading the contents of a beancount file. It's constructor can be fed the
    (entries, errors, options) tuple often returned from loader functions.

    Attributes:
        entries: The directives parsed from the beancount file.
        options: The options parsed from the beancount file.
        errors: Any errors generated during parsing.
    """

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


class IDNotFoundError(Exception):
    """Thrown when a `Directives` instance doesn't contain the given id."""

    pass
