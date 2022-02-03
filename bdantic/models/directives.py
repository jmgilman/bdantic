from __future__ import annotations

import datetime

from .base import Base
from beancount.core import data
from .data import Account, Amount, Cost, CostSpec, Currency, Flag
from decimal import Decimal
from pydantic import BaseModel, Extra, Field
from typing import Any, Dict, List, Literal, Optional, Set, Union


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


class Close(BaseDirective):
    """A model representing a beancount.core.data.Close."""

    _sibling = data.Close

    ty: Literal["Close"] = "Close"
    account: Account


class Commodity(BaseDirective):
    """A model representing a beancount.core.data.Commodity."""

    _sibling = data.Commodity

    ty: Literal["Commodity"] = "Commodity"
    date: datetime.date
    currency: str


class Custom(BaseDirective):
    """A model representing a beancount.core.data.Custom."""

    _sibling = data.Custom

    ty: Literal["Custom"] = "Custom"
    type: str
    values: List[Any]


class Document(BaseDirective):
    """A model representing a beancount.core.data.Document."""

    _sibling = data.Document

    ty: Literal["Document"] = "Document"
    account: Account
    filename: str
    tags: Optional[Set]
    links: Optional[Set]


class Event(BaseDirective):
    """A model representing a beancount.core.data.Event."""

    _sibling = data.Event

    ty: Literal["Event"] = "Event"
    type: str
    description: str


class Note(BaseDirective):
    """A model representing a beancount.core.data.Note."""

    _sibling = data.Note

    ty: Literal["Note"] = "Note"
    account: Account
    comment: str


class Open(BaseDirective):
    """A model representing a beancount.core.data.Open."""

    _sibling = data.Open

    ty: Literal["Open"] = "Open"
    account: Account
    currencies: Optional[List[Currency]]
    booking: Optional[data.Booking]


class Pad(BaseDirective):
    """A model representing a beancount.core.data.Pad."""

    _sibling = data.Pad

    ty: Literal["Pad"] = "Pad"
    account: Account
    source_account: Account


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


class Price(BaseDirective):
    """A model representing a beancount.core.data.Price."""

    _sibling = data.Price

    ty: Literal["Price"] = "Price"
    currency: Currency
    amount: Amount


class Query(BaseDirective):
    """A model representing a beancount.core.data.Query."""

    _sibling = data.Query

    ty: Literal["Query"] = "Query"
    name: str
    query_string: str


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


class TxnPosting(Base):
    """A model representing a beancount.core.data.TxnPosting."""

    _sibling = data.TxnPosting

    ty: Literal["TxnPosting"] = "TxnPosting"
    txn: Transaction
    posting: Posting


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
