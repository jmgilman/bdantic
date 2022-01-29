from __future__ import annotations

import datetime

from beancount.core import amount, data, position
from decimal import Decimal
from pydantic import BaseModel
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Type,
    Union,
)

Account = str
Currency = str
Flag = str


class Base(BaseModel):
    """Base class for representing models of Beancount types.

    This class provides standard methods for converting between a Beancount
    type and a Pydantic model.
    """

    _sibling: Type[BeancountType]

    @classmethod
    def parse(cls: Type[Model], obj: BeancountType) -> Model:
        """Attempts to parse a Beancount type into this class.

        Args:
            obj: The Beancount type to parse

        Returns:
            A new instance of this class
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> BeancountType:
        """Attempts to export this class into it's respective Beancount type.

        Returns:
            A new instance of the respective Beancount type for this class.
        """
        return _recursive_export(self)


class BaseDirective(Base):
    """A base class containing common fields for a Beancount directive."""

    date: datetime.date
    meta: Optional[Dict[str, Any]]


class Amount(Base):
    """A model representing a beancount.core.amount.Amount."""

    _sibling = amount.Amount
    number: Optional[Decimal]
    currency: Optional[Currency]


class Balance(BaseDirective):
    """A model representing a beancount.core.data.Balance."""

    _sibling = data.Balance
    account: Account
    amount: Amount
    tolerance: Optional[Decimal]
    diff_amount: Optional[Amount]


class Close(BaseDirective):
    """A model representing a beancount.core.data.Close."""

    _sibling = data.Close
    account: Account


class Commodity(BaseDirective):
    """A model representing a beancount.core.data.Commodity."""

    _sibling = data.Commodity
    currency: Currency


class Cost(Base):
    """A model representing a beancount.core.position.Cost."""

    _sibling = position.Cost
    number: Decimal
    currency: Currency
    date: datetime.date
    label: Optional[str]


class CostSpec(Base):
    """A model representing a beancount.core.position.CostSpec."""

    _sibling = position.CostSpec
    number_per: Optional[Decimal]
    number_total: Optional[Decimal]
    currency: Optional[Currency]
    date: Optional[datetime.date]
    label: Optional[str]
    merge: Optional[bool]


class Custom(BaseDirective):
    """A model representing a beancount.core.data.Custom."""

    _sibling = data.Custom
    type: str
    values: List[Any]


class Document(BaseDirective):
    """A model representing a beancount.core.data.Document."""

    _sibling = data.Document
    account: Account
    filename: str
    tags: Optional[Set]
    links: Optional[Set]


class Event(BaseDirective):
    """A model representing a beancount.core.data.Event."""

    _sibling = data.Event
    type: str
    description: str


class Note(BaseDirective):
    """A model representing a beancount.core.data.Note."""

    _sibling = data.Note
    account: Account
    comment: str


class Open(BaseDirective):
    """A model representing a beancount.core.data.Open."""

    _sibling = data.Open
    account: Account
    currencies: Optional[List[Currency]]
    booking: Optional[data.Booking]


class Pad(BaseDirective):
    """A model representing a beancount.core.data.Pad."""

    _sibling = data.Pad
    account: Account
    source_account: Account


class Position(Base):
    """A model representing a beancount.core.position.Position."""

    _sibling = position.Position
    units: Amount
    cost: Optional[Cost]


class Posting(Base):
    """A model representing a beancount.core.data.Posting."""

    _sibling = data.Posting
    account: Account
    units: Optional[Amount]
    cost: Optional[Union[Cost, CostSpec]]
    price: Optional[Amount]
    flag: Optional[str]
    meta: Optional[Dict[str, Any]]


class Price(BaseDirective):
    """A model representing a beancount.core.data.Price."""

    _sibling = data.Price
    currency: Currency
    amount: Amount


class Query(BaseDirective):
    """A model representing a beancount.core.data.Query."""

    _sibling = data.Query
    name: str
    query_string: str


class Transaction(BaseDirective):
    """A model representing a beancount.core.data.Transaction."""

    _sibling = data.Transaction
    flag: Flag
    payee: Optional[str]
    narration: str
    tags: Optional[Set]
    links: Optional[Set]
    postings: List[Posting]


class TxnPosting(Base):
    """A model representing a beancount.core.data.TxnPosting."""

    _sibling = data.TxnPosting
    txn: Transaction
    posting: Posting


# A union type for all valid models
Model = Union[
    Amount,
    Balance,
    Base,
    Close,
    Commodity,
    Cost,
    CostSpec,
    Custom,
    Document,
    Event,
    Note,
    Open,
    Pad,
    Position,
    Posting,
    Price,
    Query,
    Transaction,
    TxnPosting,
]

# A union type for all valid Beancount types
BeancountType = Union[
    amount.Amount,
    data.Balance,
    data.Close,
    data.Commodity,
    position.Cost,
    position.CostSpec,
    data.Custom,
    data.Document,
    data.Event,
    data.Note,
    data.Open,
    data.Pad,
    position.Position,
    data.Posting,
    data.Price,
    data.Query,
    data.Transaction,
    data.TxnPosting,
]


def _is_named_tuple(obj: Any) -> bool:
    """Attempts to determine if an object is a NamedTuple.

    The method is not fullproof and attempts to determine if the given object
    is a tuple which happens to have _asdict() and _fields() methods. It's
    possible to generate false positives but no such case exists within the
    beancount package.

    Args:
        obj: The object to check against

    Returns:
        True if the object is a NamedTuple, False otherwise
    """
    return (
        isinstance(obj, tuple)
        and hasattr(obj, "_asdict")
        and hasattr(obj, "_fields")
    )


def _recursive_parse(b: BeancountType) -> Dict[str, Any]:
    """Recursively parses a BeancountType into a nested dictionary.

    Since a NamedTuple can be represented as a dictionary using the bultin
    _asdict() method, this function attempts to recursively convert a
    BeancountType and any children types into a nested dictionary structure.

    Args:
        b: The BeancountType to recursively parse

    Returns:
        A nested dictionary with all parsed BeancountType contents.
    """
    result: Dict[str, Any] = {}
    for key, value in b._asdict().items():
        if _is_named_tuple(value):
            result[key] = _recursive_parse(value)
        elif isinstance(value, list) and value:
            if _is_named_tuple(value[0]):
                result[key] = [_recursive_parse(c) for c in value]
        else:
            result[key] = value

    return result


def _recursive_export(b: Base) -> BeancountType:
    """Recursively exports a Base model into its resepective BeancountType.

    Args:
        b: The Base model to recursively export

    Returns:
        The respective BeancountType
    """
    result: Dict[str, Any] = {}
    for key, value in b.__dict__.items():
        if isinstance(value, Base):
            result[key] = _recursive_export(value)
        elif isinstance(value, list) and value:
            if isinstance(value[0], Base):
                result[key] = [_recursive_export(c) for c in value]
        else:
            result[key] = value

    return b._sibling(**result)
