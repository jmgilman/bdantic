from __future__ import annotations

import datetime

from .base import Base
from beancount.core import data
from .data import Account, Amount, Cost, CostSpec, Currency, Flag
from decimal import Decimal
from pydantic import BaseModel, Extra, Field
from typing import Any, Dict, List, Literal, Optional, Set, Union
from .common import recursive_export, recursive_parse


class BaseDirective(Base):
    """A base class containing common fields for a Beancount directive."""

    date: datetime.date
    meta: Optional[Meta]


class Meta(BaseModel):
    filename: Optional[str]
    lineno: Optional[int]
    tolerances: Optional[Dict[str, Decimal]] = Field(alias="__tolerances__")

    class Config:
        extra = Extra.allow


class Balance(BaseDirective):
    """A model representing a beancount.core.data.Balance."""

    _sibling = data.Balance
    ty: Literal["Balance"] = "Balance"
    account: Account
    amount: Amount
    tolerance: Optional[Decimal]
    diff_amount: Optional[Amount]

    @classmethod
    def parse(cls, obj: data.Balance) -> Balance:
        """Parses a beancount Balance directive into this model

        Args:
            obj: The Beancount Balance directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Balance:
        """Exports this model into a beancount Balance directive

        Returns:
            A new instance of a beancount Balance directive
        """
        return self._sibling(**recursive_export(self))


class Close(BaseDirective):
    """A model representing a beancount.core.data.Close."""

    _sibling = data.Close
    ty: Literal["Close"] = "Close"
    account: Account

    @classmethod
    def parse(cls, obj: data.Close) -> Close:
        """Parses a beancount Close directive into this model

        Args:
            obj: The Beancount Close directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Close:
        """Exports this model into a beancount Close directive

        Returns:
            A new instance of a beancount Close directive
        """
        return self._sibling(**recursive_export(self))


class Commodity(BaseDirective):
    """A model representing a beancount.core.data.Commodity."""

    _sibling = data.Commodity
    ty: Literal["Commodity"] = "Commodity"
    date: datetime.date
    currency: str

    @classmethod
    def parse(cls, obj: data.Commodity) -> Commodity:
        """Parses a beancount Commodity directive into this model

        Args:
            obj: The Beancount Commodity directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Commodity:
        """Exports this model into a beancount Commodity directive

        Returns:
            A new instance of a beancount Commodity directive
        """
        return self._sibling(**recursive_export(self))


class Custom(BaseDirective):
    """A model representing a beancount.core.data.Custom."""

    _sibling = data.Custom
    ty: Literal["Custom"] = "Custom"
    type: str
    values: List[Any]

    @classmethod
    def parse(cls, obj: data.Custom) -> Custom:
        """Parses a beancount Custom directive into this model

        Args:
            obj: The Beancount Custom directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Custom:
        """Exports this model into a beancount Custom directive

        Returns:
            A new instance of a beancount Custom directive
        """
        return self._sibling(**recursive_export(self))


class Document(BaseDirective):
    """A model representing a beancount.core.data.Document."""

    _sibling = data.Document
    ty: Literal["Document"] = "Document"
    account: Account
    filename: str
    tags: Optional[Set]
    links: Optional[Set]

    @classmethod
    def parse(cls, obj: data.Document) -> Document:
        """Parses a beancount Document directive into this model

        Args:
            obj: The Beancount Document directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Document:
        """Exports this model into a beancount Document directive

        Returns:
            A new instance of a beancount Document directive
        """
        return self._sibling(**recursive_export(self))


class Event(BaseDirective):
    """A model representing a beancount.core.data.Event."""

    _sibling = data.Event
    ty: Literal["Event"] = "Event"
    type: str
    description: str

    @classmethod
    def parse(cls, obj: data.Event) -> Event:
        """Parses a beancount Event directive into this model

        Args:
            obj: The Beancount Event directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Event:
        """Exports this model into a beancount Event directive

        Returns:
            A new instance of a beancount Event directive
        """
        return self._sibling(**recursive_export(self))


class Note(BaseDirective):
    """A model representing a beancount.core.data.Note."""

    _sibling = data.Note
    ty: Literal["Note"] = "Note"
    account: Account
    comment: str

    @classmethod
    def parse(cls, obj: data.Note) -> Note:
        """Parses a beancount Note directive into this model

        Args:
            obj: The Beancount Note directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Note:
        """Exports this model into a beancount Note directive

        Returns:
            A new instance of a beancount Note directive
        """
        return self._sibling(**recursive_export(self))


class Open(BaseDirective):
    """A model representing a beancount.core.data.Open."""

    _sibling = data.Open
    ty: Literal["Open"] = "Open"
    account: Account
    currencies: Optional[List[Currency]]
    booking: Optional[data.Booking]

    @classmethod
    def parse(cls, obj: data.Open) -> Open:
        """Parses a beancount Open directive into this model

        Args:
            obj: The Beancount Open directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Open:
        """Exports this model into a beancount Open directive

        Returns:
            A new instance of a beancount Open directive
        """
        return self._sibling(**recursive_export(self))


class Pad(BaseDirective):
    """A model representing a beancount.core.data.Pad."""

    _sibling = data.Pad
    ty: Literal["Pad"] = "Pad"
    account: Account
    source_account: Account

    @classmethod
    def parse(cls, obj: data.Pad) -> Pad:
        """Parses a beancount Pad directive into this model

        Args:
            obj: The Beancount Pad directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Pad:
        """Exports this model into a beancount Pad directive

        Returns:
            A new instance of a beancount Pad directive
        """
        return self._sibling(**recursive_export(self))


class Posting(Base):
    """A model representing a beancount.core.data.Posting."""

    _sibling = data.Posting
    ty: Literal["Posting"] = "Posting"
    account: Account
    units: Optional[Amount]
    cost: Optional[Union[Cost, CostSpec]]
    price: Optional[Amount]
    flag: Optional[str]
    meta: Optional[Dict[str, Any]]

    @classmethod
    def parse(cls, obj: data.Posting) -> Posting:
        """Parses a beancount Posting into this model

        Args:
            obj: The Beancount Posting to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Posting:
        """Exports this model into a beancount Posting

        Returns:
            A new instance of a beancount Posting
        """
        return self._sibling(**recursive_export(self))


class Price(BaseDirective):
    """A model representing a beancount.core.data.Price."""

    _sibling = data.Price
    ty: Literal["Price"] = "Price"
    currency: Currency
    amount: Amount

    @classmethod
    def parse(cls, obj: data.Price) -> Price:
        """Parses a beancount Price directive into this model

        Args:
            obj: The Beancount Price directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Price:
        """Exports this model into a beancount Price directive

        Returns:
            A new instance of a beancount Price directive
        """
        return self._sibling(**recursive_export(self))


class Query(BaseDirective):
    """A model representing a beancount.core.data.Query."""

    _sibling = data.Query
    ty: Literal["Query"] = "Query"
    name: str
    query_string: str

    @classmethod
    def parse(cls, obj: data.Query) -> Query:
        """Parses a beancount Query directive into this model

        Args:
            obj: The Beancount Query directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Query:
        """Exports this model into a beancount Query directive

        Returns:
            A new instance of a beancount Query directive
        """
        return self._sibling(**recursive_export(self))


class Transaction(BaseDirective):
    """A model representing a beancount.core.data.Transaction."""

    _sibling = data.Transaction
    ty: Literal["Transaction"] = "Transaction"
    flag: Flag
    payee: Optional[str]
    narration: str
    tags: Optional[Set[str]]
    links: Optional[Set[str]]
    postings: List[Posting]

    @classmethod
    def parse(cls, obj: data.Transaction) -> Transaction:
        """Parses a beancount Transaction directive into this model

        Args:
            obj: The Beancount Transaction directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.Transaction:
        """Exports this model into a beancount Transaction directive

        Returns:
            A new instance of a beancount Transaction directive
        """
        return self._sibling(**recursive_export(self))


class TxnPosting(Base):
    """A model representing a beancount.core.data.TxnPosting."""

    _sibling = data.TxnPosting
    ty: Literal["TxnPosting"] = "TxnPosting"
    txn: Transaction
    posting: Posting

    @classmethod
    def parse(cls, obj: data.TxnPosting) -> TxnPosting:
        """Parses a beancount TxnPosting into this model

        Args:
            obj: The Beancount TxnPosting to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> data.TxnPosting:
        """Exports this model into a beancount TxnPosting

        Returns:
            A new instance of a beancount TxnPosting
        """
        return self._sibling(**recursive_export(self))


# Update forward references
Balance.update_forward_refs()
Close.update_forward_refs()
Commodity.update_forward_refs()
Custom.update_forward_refs()
Document.update_forward_refs()
Event.update_forward_refs()
Note.update_forward_refs()
Open.update_forward_refs()
Pad.update_forward_refs()
Price.update_forward_refs()
Query.update_forward_refs()
Transaction.update_forward_refs()
