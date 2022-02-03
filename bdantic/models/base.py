from __future__ import annotations

import jmespath  # type: ignore
import orjson

from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


S = TypeVar("S", bound="Base")


class Base(BaseModel):
    """The base model class used for most models in bdantic."""

    _sibling: type

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
