"""Provides the base models from which every other model inherits from.

Most models share common behavior, namely the ability to parse and export.
Models which are based from a beancount type which is a NamedTuple all share
the same parse/export code inherited from the [Base][bdantic.models.base.Base]
class. Models which need specialized code for parsing/exporting will override
these methods appropriately.

Additionally, models which wrap lists or dictionaries have a dedicated base
class for allowing filtering and providing the expected pythonic methods to
make them behave as lists/dictionaries.
"""

from __future__ import annotations

import datetime
import hashlib
import jmespath  # type: ignore
import orjson
import os

from beancount.core import data, number
from beancount.parser import printer  # type: ignore
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, Extra
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

S = TypeVar("S", bound="Base")
T = TypeVar("T")

_IGNORE_FIELDS = ["id", "ty"]
_DIRECTIVES = [
    data.Balance,
    data.Close,
    data.Commodity,
    data.Custom,
    data.Document,
    data.Event,
    data.Note,
    data.Open,
    data.Pad,
    data.Price,
    data.Query,
    data.Transaction,
]


def orjson_dumps(v, *, default):
    return orjson.dumps(
        v, default=default, option=orjson.OPT_NON_STR_KEYS
    ).decode()


class Base(BaseModel, Generic[T]):
    """The base model class used for most models in bdantic."""

    _sibling: Type[T]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    def json(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = True,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        return super().json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs,
        )

    @classmethod
    def parse(cls: Type[S], obj: T) -> S:
        """Parses a beancount type into this model

        Args:
            obj: The Beancount type to parse

        Returns:
            A new instance of this model
        """
        parsed = recursive_parse(obj)

        # It's possible for tolerances to have a number.MISSING key which will
        # fail validation
        try:
            parsed["meta"]["__tolerances__"] = {
                k: v
                for k, v in parsed["meta"]["__tolerances__"].items()
                if k is not number.MISSING
            }
        except (KeyError, TypeError):
            pass

        # Generate a unique ID for directives parsed from a file
        try:
            parsed["id"] = hashlib.md5(
                "".join(
                    [
                        os.path.basename(parsed["meta"]["filename"]),
                        str(parsed["meta"]["lineno"]),
                        str(parsed["date"]),
                    ]
                ).encode()
            ).hexdigest()
        except (KeyError, TypeError):
            pass

        return cls.parse_obj(parsed)

    def export(self: S) -> T:
        """Exports this model into it's associated beancount type

        Returns:
            A new instance of the beancount type
        """
        return self._sibling(**recursive_export(self, _IGNORE_FIELDS))

    def select(
        self, expr: str, model: Type[BaseModel] = None
    ) -> Optional[Any]:
        """Selects from this model using a jmespath expression.

        The model is converted to a dictionary and then the given jmespath
        expression is applied to the dictionary. The result of the selection
        process is dependent on the expression used and can be any combination
        of data contained within the model or its children. Note that this
        method automatically converts dates into ISO formatted strings and
        Decimals into floats in order to increase compatability with jmespath.

        The result can optionally be parsed into a model by passing the type of
        model. If the result is a list, all child elements will be converted
        into the given model.

        Args:
            expr: The jmespath expression

        Result:
            Result from applying the given expression
        """
        converted = self._mutate(_convert)
        if hasattr(self, "__root__"):
            result = jmespath.search(expr, converted["__root__"])
            obj = {"__root__": result}
        else:
            obj = jmespath.search(expr, converted)

        if obj:  # Sometimes jmespath returns False
            if model:
                if isinstance(obj, list):
                    return [model.parse_obj(o) for o in obj]
                else:
                    return model.parse_obj(obj)
            return obj
        else:
            return None

    def _mutate(self, fn: Callable) -> Any:
        """Mutates the model by converting it to a dict and calling fn().

        The given fn is recursively applied to the model fields and all child
        fields. The purpose of this method is to apply a transformation to
        potentially deeply nested child objects (i.e. convert all dates within
        a model and it's children to strings).

        Args:
            fn: The function to mutate with

        Returns:
            A mutated dictionary representation of the model and it's children.
        """
        return _map(self.dict(), fn)


class BaseDirective(Base):
    """A base class containing common fields for a Beancount directive.

    All directives in beancount share two common fields: a date they were
    recorded and optional metadata attached to them. This class provides fields
    for both of these attributes which directive models inherit from.

    Additionally, all directives can be represented as raw beancount syntax and
    this class provides a method for converting a directive model into its
    equivalent beancount syntax.

    Note: The ID of a directive will only be generated in the case where the
    directive contains the `filename` and `lineno` metadata fields. Per the
    beancount documentation, these fields are guaranteed to be present if the
    directive is coming from a parsed beancount ledger file. If a directive is
    dynamically created at runtime without these metadata fields the resulting
    model will not have an ID (it will be None).

    Attributes:
        id: An optional unique ID for this directive.
        date: The date for this directive.
        meta: An optional dictionary of metadata attached to the directive.
    """

    id: Optional[str] = None
    date: datetime.date
    meta: Optional[Meta] = None

    def syntax(self) -> str:
        """Converts this directive into it's equivalent beancount syntax."""
        return printer.format_entry(self.export())


class BaseFiltered(Base):
    """A base model which can be filtered."""

    def filter(self: S, expr: str) -> Optional[S]:
        """Filters this model using the given jmespath expression.

        Note that the given expression must return a result that can be parsed
        back into this model. If the expression mutates the object in an
        incompatible way then it's likely to raise an exception when Pydantic
        attempts to parse the result back into the model."""
        obj = self.select(expr)
        if obj:
            return self.parse_obj(obj)
        else:
            return None


class BaseList(BaseFiltered, Generic[S]):
    """A base model that wraps a list of objects."""

    __root__: List[S]

    def _by_type(self, ty: Type[T]) -> List[T]:
        result = []
        for model in self:
            if isinstance(model, ty):
                result.append(model)

        return result

    def __len__(self) -> int:
        return len(self.__root__)

    def __getitem__(self, i: int):
        return self.__root__[i]

    def __delitem__(self, i: int):
        del self.__root__[i]

    def __setitem__(self, i: int, v: S):
        self.__root__[i] = v

    def __iter__(self):
        for v in self.__root__:
            yield v


class BaseDict(Base, Generic[S]):
    """A base model that wraps a dictionary."""

    __root__: Dict[str, S]

    def __len__(self) -> int:
        return len(self.__root__)

    def __getitem__(self, key: str):
        return self.__root__[key]

    def __delitem__(self, key: str):
        del self.__root__[key]

    def __setitem__(self, key: str, v: Any):
        self.__root__[key] = v

    def __iter__(self):
        for k in self.__root__.keys():
            yield k

    def items(self):
        return self.__root__.items()

    def keys(self):
        return self.__root__.keys()

    def values(self):
        return self.__root__.values()


class Meta(BaseModel):
    """Represents the metadata attached to a directive.

    Most directives share common metadata fields, namely the filename and line
    number in which they occur. This model provides access to those common
    fields but is also configured to accept any other variable number of fields
    that may be attached to a directive.

    Attributes:
        filename: The name of the file the direcive is located in
        lineno: The line number the directive is located on
        tolerances: A lookup dictionary for fetching currency tolerances.
    """

    filename: Optional[str]
    lineno: Optional[int]
    tolerances: Optional[Dict[str, Decimal]] = Field(alias="__tolerances__")

    class Config:
        extra = Extra.allow


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
        if hasattr(value, "_asdict"):
            result[key] = recursive_parse(value)
        elif isinstance(value, list) and value:
            if hasattr(value[0], "_asdict"):
                result[key] = [recursive_parse(c) for c in value]
            else:
                result[key] = value
        else:
            result[key] = value

    return result


def recursive_export(b: Any, skip_fields: List[str] = []) -> Dict[str, Any]:
    """Recursively exports a ModelTuple into a nested dictionary

    Args:
        b: The ModelTuple to recursively export
        skip_fields: A list of fields to skip when exporting

    Returns:
        A nested dictionary with all exported Beancount types
    """
    result: Dict[str, Any] = {}
    for key, value in b.__dict__.items():
        if key in skip_fields:
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
            result[key] = value._sibling(
                **recursive_export(value, skip_fields)
            )
        elif isinstance(value, list) and value:
            if isinstance(value[0], Base):
                result[key] = [
                    c._sibling(**recursive_export(c, skip_fields))
                    for c in value
                ]
            else:
                result[key] = value
        else:
            result[key] = value

    return result


def _map(obj: Any, fn: Callable) -> Any:
    """Recursively maps a function to a nested object.

    If the passed object is a list, dictionary, set, or tuple, then all child
    elements are recursively mapped.

    Args:
        obj: The object to map against
        fn: The function to map

    Returns:
        The mutated object
    """
    if isinstance(obj, dict):
        return {k: _map(v, fn) for k, v in obj.items()}
    elif (
        isinstance(obj, list) or isinstance(obj, set) or isinstance(obj, tuple)
    ):
        return [_map(v, fn) for v in obj]
    else:
        return fn(obj)


def _convert(obj: Any) -> Any:
    """Converts decimals to floats and dates to ISO formatted date strings.

    Args:
        obj: The object to convert

    Returns:
        A float, ISO formatted date string, or the original object.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, date):
        return obj.isoformat()
    else:
        return obj
