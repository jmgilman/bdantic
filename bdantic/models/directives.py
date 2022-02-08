"""Provides models for all beancount directives."""

from __future__ import annotations

from .base import Base, BaseDirective, Meta  # noqa: F401
from beancount.core import data
from .data import Account, Amount, Cost, CostSpec, Currency, Flag
from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional, Set, Union


class Balance(BaseDirective):
    """A model representing a `beancount.core.data.Balance`.

    Attributes:
        ty: A string literal identifying this model.
        account: The account whose balance to check at the given date.
        amount: The number of expected units for the account at the given date.
        diff_amount: The difference between the expected and actual amounts.
        tolerance: The amount of tolerance to use in the verification.
    """

    _sibling = data.Balance

    ty: Literal["Balance"] = "Balance"
    account: Account
    amount: Amount
    tolerance: Optional[Decimal]
    diff_amount: Optional[Amount]


class Close(BaseDirective):
    """A model representing a `beancount.core.data.Close`.
    Attributes:
        ty: A string literal identifying this model.
        account: The name of the account being closed.
    """

    _sibling = data.Close

    ty: Literal["Close"] = "Close"
    account: Account


class Commodity(BaseDirective):
    """A model representing a `beancount.core.data.Commodity`.

    Attributes:
        ty: A string literal identifying this model.
        currency: The commodity under consideration.
    """

    _sibling = data.Commodity

    ty: Literal["Commodity"] = "Commodity"
    currency: str


class Custom(BaseDirective):
    """A model representing a `beancount.core.data.Custom`.

    Attributes:
        ty: A string literal identifying this model.
        type: The type of this custom directive.
        values: A list of values of simple types supported by the grammar.
    """

    _sibling = data.Custom

    ty: Literal["Custom"] = "Custom"
    type: str
    values: List[Any]


class Document(BaseDirective):
    """A model representing a `beancount.core.data.Document`.

    Attributes:
        ty: A string literal identifying this model.
        account: The account the document is associated with.
        filename: The absolute filename of the document.
        tags: A set of tag strings.
        links: A set of link strings.
    """

    _sibling = data.Document

    ty: Literal["Document"] = "Document"
    account: Account
    filename: str
    tags: Optional[Set]
    links: Optional[Set]


class Event(BaseDirective):
    """A model representing a `beancount.core.data.Event`.

    Attributes:
        ty: A string literal identifying this model.
        type: A unique string identifying this event.
        description: The value of the above type at the given date.
    """

    _sibling = data.Event

    ty: Literal["Event"] = "Event"
    type: str
    description: str


class Note(BaseDirective):
    """A model representing a `beancount.core.data.Note`.

    Attributes:
        ty: A string literal identifying this model.
        account: The account this note is attached to.
        comment: The string contents of the note.
    """

    _sibling = data.Note

    ty: Literal["Note"] = "Note"
    account: Account
    comment: str


class Open(BaseDirective):
    """A model representing a `beancount.core.data.Open`.

    Attributes:
        ty: A string literal identifying this model.
        account: The name of the account being opened.
        currencies: Currencies that are allowed in this account.
        booking: Booking method used to disambiguate postings to this account.
    """

    _sibling = data.Open

    ty: Literal["Open"] = "Open"
    account: Account
    currencies: Optional[List[Currency]]
    booking: Optional[data.Booking]


class Pad(BaseDirective):
    """A model representing a `beancount.core.data.Pad`.

    Attributes:
        ty: A string literal identifying this model.
        account: The name of the account which needs to be filled.
        source_account: The name of the account used for debiting.
    """

    _sibling = data.Pad

    ty: Literal["Pad"] = "Pad"
    account: Account
    source_account: Account


class Posting(Base):
    """A model representing a `beancount.core.data.Posting`.

    Attributes:
        ty: A string literal identifying this model.
        account: The account that is modified by this posting.
        units: The units of the position.
        cost: The cost of the position.
        price: The optional price at which the position took place.
        flag: An optional flag to associate with the posting.
        meta: Optional metadata attached to the posting.
    """

    _sibling = data.Posting

    ty: Literal["Posting"] = "Posting"
    account: Account
    units: Optional[Amount]
    cost: Optional[Union[Cost, CostSpec]]
    price: Optional[Amount]
    flag: Optional[str]
    meta: Optional[Dict[str, Any]]


class Price(BaseDirective):
    """A model representing a `beancount.core.data.Price`.

    Attributes:
        ty: A string literal identifying this model.
        currency: The currency that is being priced.
        amount: The value of the currency.
    """

    _sibling = data.Price

    ty: Literal["Price"] = "Price"
    currency: Currency
    amount: Amount


class Query(BaseDirective):
    """A model representing a `beancount.core.data.Query`.

    Attributes:
        ty: A string literal identifying this model.
        name: The unique identifier for the query.
        query_string: The SQL query string to run or be made available.
    """

    _sibling = data.Query

    ty: Literal["Query"] = "Query"
    name: str
    query_string: str


class Transaction(BaseDirective):
    """A model representing a `beancount.core.data.Transaction`.

    Attributes:
        ty: A string literal identifying this model.
        flag: A flag denoting the state of the transaction.
        payee: The payee of the transaction.
        narration: A description of the transaction.
        tags: A set of tag strings.
        links: A set of link strings.
        postings: A list of postings attached to this transaction.
    """

    _sibling = data.Transaction

    ty: Literal["Transaction"] = "Transaction"
    flag: Flag
    payee: Optional[str]
    narration: str
    tags: Optional[Set[str]]
    links: Optional[Set[str]]
    postings: List[Posting]


class TxnPosting(Base):
    """A model representing a `beancount.core.data.TxnPosting`.

    Attributes:
        ty: A string literal identifying this model.
        txn: The parent transaction instance.
        posting: The posting instance.
    """

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
