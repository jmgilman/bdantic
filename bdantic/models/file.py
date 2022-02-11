"""Provides models for representing the contents of a parsed beancount file."""

from __future__ import annotations
from decimal import Decimal

import lzma
import pickle

from .base import Base, BaseList
from beancount.core import data, realization
from beancount.query import query
from bdantic import models
from bdantic.types import ModelDirective, type_map
from pydantic import Extra
from .query import QueryResult
from .realize import Account, RealAccount
from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar

T = TypeVar("T", bound="ModelDirective")


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

    def by_account(self, account: str) -> Directives:
        """Returns a new instance of `Directives` filtered by the given account.

        Args:
            account: The account to filter by.

        Returns:
            A new instance of `Directives` with the filtered results.
        """
        result: List[ModelDirective] = []
        simple = (
            models.Open,
            models.Close,
            models.Balance,
            models.Note,
            models.Document,
        )
        for dir in self:
            if isinstance(dir, models.Transaction):
                if account in [p.account for p in dir.postings]:
                    result.append(dir)
            elif isinstance(dir, simple):
                if dir.account == account:
                    result.append(dir)
            elif isinstance(dir, models.Pad):
                if dir.account == account or dir.source_account == account:
                    result.append(dir)
            elif isinstance(dir, models.Custom):
                for v in dir.values:
                    if isinstance(v, str):
                        if v == account:
                            result.append(dir)

        return Directives(__root__=result)

    def by_id(self, id: str) -> ModelDirective:
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

    def by_ids(self, ids: List[str]) -> List[ModelDirective]:
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
            result.append(self.by_id(id))

        return result

    def by_type(self, ty: Type[T]) -> Directives:
        """Returns a new instance of `Directives` filtered by the given type.

        Args:
            ty: The type to filter by.

        Returns:
            A new instance of `Directives` with the filtered results.
        """
        return Directives(__root__=super()._by_type(ty))


class Options(Base):
    """A model representing ledger options.

    This model wraps the options contained within a ledger. Options which
    contain raw beancount types are automatically parsed into their respective
    model.

    See the docs for more details about each field:
    https://beancount.github.io/docs/beancount_options_reference.html
    """

    account_current_conversions: Optional[str] = None
    account_current_earnings: Optional[str] = None
    account_previous_balances: Optional[str] = None
    account_previous_conversions: Optional[str] = None
    account_previous_earnings: Optional[str] = None
    account_rounding: Optional[str] = None
    allow_deprecated_none_for_tags_and_links: Optional[bool] = None
    allow_pipe_separator: Optional[bool] = None
    booking_method: Optional[data.Booking] = None
    commodities: Optional[Set[str]] = None
    conversion_currency: Optional[str] = None
    dcontext: Optional[models.DisplayContext] = None
    documents: Optional[List[str]] = None
    experiment_explicit_tolerances: Optional[bool] = None
    infer_tolerance_from_cost: Optional[bool] = None
    inferred_tolerance_default: Optional[Dict[str, Decimal]]
    inferred_tolerance_multiplier: Optional[Decimal] = None
    input_hash: Optional[str] = None
    insert_pythonpath: Optional[bool] = None
    long_string_maxlines: Optional[int] = None
    name_assets: Optional[str] = None
    name_equity: Optional[str] = None
    name_expenses: Optional[str] = None
    name_income: Optional[str] = None
    name_liabilities: Optional[str] = None
    operating_currency: Optional[List[str]] = None
    plugin: Optional[List[str]] = None
    plugin_processing_mode: Optional[str] = None
    render_commas: Optional[bool] = None
    tolerance: Optional[Decimal] = None
    title: Optional[str] = None
    use_legacy_fixed_tolerances: Optional[bool] = None

    class Config:
        extra = Extra.allow

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

        return Options(**d)

    def export(self) -> Dict[str, Any]:
        """Exports this model into a dictionary of beancount options

        Returns:
            The dictionary of beancount options
        """
        d = {}
        for key, value in self.__dict__.items():
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
        accounts: A dictionary of account names to `Account` instances
    """

    entries: Directives
    options: Options
    errors: List[Any]
    accounts: Dict[str, Account]

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
        entries = Directives.parse(obj[0])
        errors = obj[1]
        options = Options.parse(obj[2])

        real = realization.realize(obj[0])
        names = [o.account for o in entries.by_type(models.Open)]

        accounts = {}
        for name in names:
            accounts[name] = Account.parse(realization.get(real, name))

        return BeancountFile(
            entries=entries,
            options=options,
            errors=errors,
            accounts=accounts,
        )

    @staticmethod
    def decompress(data: bytes) -> BeancountFile:
        """Decompresses the given data into a `BeancountFile` instance.

        Args:
            data: The bytes from an LZMA compressed pickled `BeancountFile`.

        Returns:
            The decompressed, unpickled `BeancountFile` instance.
        """
        return pickle.loads(lzma.decompress(data))

    def export(self) -> Tuple[List[data.Directive], List[Any], Dict[str, Any]]:
        """Exports this model into it's original counterpart

        Returns:
            The entries, errors, and options from the original loader
        """
        return (self.entries.export(), self.errors, self.options.export())

    def compress(self) -> bytes:
        """Compresses this instance into a byte stream.

        Returns:
            An LZMA compressed pickle instance of this instance.
        """
        return lzma.compress(pickle.dumps(self))

    def query(self, query_str: str) -> QueryResult:
        """Executes the given BQL query against the entries in this file.

        Args:
            query_str: The BQL query to execute.

        Returns:
            A `QueryResult` containing the results of the query.
        """
        result = query.run_query(
            self.entries.export(), self.options.export(), query_str
        )

        return QueryResult.parse(result)

    def realize(self) -> RealAccount:
        """Realizes the entries in this file.

        Returns:
            The root `RealAccount` from the realization.
        """
        root = realization.realize(self.entries.export())
        return RealAccount.parse(root)


class IDNotFoundError(Exception):
    """Thrown when a `Directives` instance doesn't contain the given id."""

    pass
