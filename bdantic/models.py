from __future__ import annotations

import datetime

from beancount.core import amount, data, inventory, position
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
    _sibling: type


class BaseDirective(Base):
    """A base class containing common fields for a Beancount directive."""

    date: datetime.date
    meta: Optional[Dict[str, Any]]


class Amount(Base):
    """A model representing a beancount.core.amount.Amount."""

    _sibling = amount.Amount
    number: Optional[Decimal]
    currency: Optional[Currency]

    @classmethod
    def parse(cls, obj: amount.Amount) -> Amount:
        """Parses a beancount Amount into this model

        Args:
            obj: The Beancount Amount to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> amount.Amount:
        """Exports this model into a beancount Amount

        Returns:
            A new instance of a beancount Amount
        """
        return self._sibling(**_recursive_export(self))


class Balance(BaseDirective):
    """A model representing a beancount.core.data.Balance."""

    _sibling = data.Balance
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Balance:
        """Exports this model into a beancount Balance directive

        Returns:
            A new instance of a beancount Balance directive
        """
        return self._sibling(**_recursive_export(self))


class Close(BaseDirective):
    """A model representing a beancount.core.data.Close."""

    _sibling = data.Close
    account: Account

    @classmethod
    def parse(cls, obj: data.Close) -> Close:
        """Parses a beancount Close directive into this model

        Args:
            obj: The Beancount Close directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Close:
        """Exports this model into a beancount Close directive

        Returns:
            A new instance of a beancount Close directive
        """
        return self._sibling(**_recursive_export(self))


class Cost(Base):
    """A model representing a beancount.core.position.Cost."""

    _sibling = position.Cost
    number: Decimal
    currency: Currency
    date: datetime.date
    label: Optional[str]

    @classmethod
    def parse(cls, obj: position.Cost) -> Cost:
        """Parses a beancount Cost into this model

        Args:
            obj: The Beancount Cost to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> position.Cost:
        """Exports this model into a beancount Cost

        Returns:
            A new instance of a beancount Cost
        """
        return self._sibling(**_recursive_export(self))


class CostSpec(Base):
    """A model representing a beancount.core.position.CostSpec."""

    _sibling = position.CostSpec
    number_per: Optional[Decimal]
    number_total: Optional[Decimal]
    currency: Optional[Currency]
    date: Optional[datetime.date]
    label: Optional[str]
    merge: Optional[bool]

    @classmethod
    def parse(cls, obj: position.CostSpec) -> CostSpec:
        """Parses a beancount CostSpec into this model

        Args:
            obj: The Beancount CostSpec to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> position.CostSpec:
        """Exports this model into a beancount CostSpec

        Returns:
            A new instance of a beancount CostSpec
        """
        return self._sibling(**_recursive_export(self))


class Commodity(BaseDirective):
    """A model representing a beancount.core.data.Commodity."""

    _sibling = data.Commodity
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Commodity:
        """Exports this model into a beancount Commodity directive

        Returns:
            A new instance of a beancount Commodity directive
        """
        return self._sibling(**_recursive_export(self))


class Custom(BaseDirective):
    """A model representing a beancount.core.data.Custom."""

    _sibling = data.Custom
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Custom:
        """Exports this model into a beancount Custom directive

        Returns:
            A new instance of a beancount Custom directive
        """
        return self._sibling(**_recursive_export(self))


class Document(BaseDirective):
    """A model representing a beancount.core.data.Document."""

    _sibling = data.Document
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Document:
        """Exports this model into a beancount Document directive

        Returns:
            A new instance of a beancount Document directive
        """
        return self._sibling(**_recursive_export(self))


class Event(BaseDirective):
    """A model representing a beancount.core.data.Event."""

    _sibling = data.Event
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Event:
        """Exports this model into a beancount Event directive

        Returns:
            A new instance of a beancount Event directive
        """
        return self._sibling(**_recursive_export(self))


class Inventory(Base):
    """A model representing a beancount.core.inventory.Inventory."""

    __root__: List[Position]

    @classmethod
    def parse(cls: Type[Inventory], obj: inventory.Inventory) -> Inventory:
        """Parses a beancount Inventory into this model

        Args:
            obj: The Beancount Inventory to parse

        Returns:
            A new instance of this model
        """
        positions = [
            Position.parse(position) for position in obj.get_positions()
        ]
        return Inventory(__root__=positions)

    def export(self) -> inventory.Inventory:
        """Exports this model into a beancount Inventory

        Returns:
            A new instance of a beancount Inventory directive
        """
        positions = [position.export() for position in self.__root__]
        return inventory.Inventory(positions=positions)


class Note(BaseDirective):
    """A model representing a beancount.core.data.Note."""

    _sibling = data.Note
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Note:
        """Exports this model into a beancount Note directive

        Returns:
            A new instance of a beancount Note directive
        """
        return self._sibling(**_recursive_export(self))


class Open(BaseDirective):
    """A model representing a beancount.core.data.Open."""

    _sibling = data.Open
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Open:
        """Exports this model into a beancount Open directive

        Returns:
            A new instance of a beancount Open directive
        """
        return self._sibling(**_recursive_export(self))


class Pad(BaseDirective):
    """A model representing a beancount.core.data.Pad."""

    _sibling = data.Pad
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Pad:
        """Exports this model into a beancount Pad directive

        Returns:
            A new instance of a beancount Pad directive
        """
        return self._sibling(**_recursive_export(self))


class Position(Base):
    """A model representing a beancount.core.position.Position."""

    _sibling = position.Position
    units: Amount
    cost: Optional[Cost]

    @classmethod
    def parse(cls, obj: position.Position) -> Position:
        """Parses a beancount Position into this model

        Args:
            obj: The Beancount Position to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> position.Position:
        """Exports this model into a beancount Position

        Returns:
            A new instance of a beancount Position
        """
        return self._sibling(**_recursive_export(self))


class Posting(Base):
    """A model representing a beancount.core.data.Posting."""

    _sibling = data.Posting
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Posting:
        """Exports this model into a beancount Posting

        Returns:
            A new instance of a beancount Posting
        """
        return self._sibling(**_recursive_export(self))


class Price(BaseDirective):
    """A model representing a beancount.core.data.Price."""

    _sibling = data.Price
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Price:
        """Exports this model into a beancount Price directive

        Returns:
            A new instance of a beancount Price directive
        """
        return self._sibling(**_recursive_export(self))


class Query(BaseDirective):
    """A model representing a beancount.core.data.Query."""

    _sibling = data.Query
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Query:
        """Exports this model into a beancount Query directive

        Returns:
            A new instance of a beancount Query directive
        """
        return self._sibling(**_recursive_export(self))


class Transaction(BaseDirective):
    """A model representing a beancount.core.data.Transaction."""

    _sibling = data.Transaction
    flag: Flag
    payee: Optional[str]
    narration: str
    tags: Optional[Set]
    links: Optional[Set]
    postings: List[Posting]

    @classmethod
    def parse(cls, obj: data.Transaction) -> Transaction:
        """Parses a beancount Transaction directive into this model

        Args:
            obj: The Beancount Transaction directive to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.Transaction:
        """Exports this model into a beancount Transaction directive

        Returns:
            A new instance of a beancount Transaction directive
        """
        return self._sibling(**_recursive_export(self))


class TxnPosting(Base):
    """A model representing a beancount.core.data.TxnPosting."""

    _sibling = data.TxnPosting
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
        return cls.parse_obj(_recursive_parse(obj))

    def export(self) -> data.TxnPosting:
        """Exports this model into a beancount TxnPosting

        Returns:
            A new instance of a beancount TxnPosting
        """
        return self._sibling(**_recursive_export(self))


# A union for all models that are directives
ModelDirective = Union[
    Balance,
    Close,
    Open,
    Commodity,
    Custom,
    Document,
    Event,
    Note,
    Open,
    Pad,
    Price,
    Query,
    Transaction,
]

# A union for all models which have Beancount types that are NamedTuple's
ModelTuple = Union[
    ModelDirective,
    Amount,
    Base,
    Cost,
    CostSpec,
    Position,
    Posting,
    TxnPosting,
]

# A union for all models
Model = Union[ModelTuple, Inventory]

# A union for all Beancount types which are NamedTuple's
BeancountTuple = Union[
    amount.Amount,
    data.Balance,
    data.Close,
    data.Open,
    position.Cost,
    position.CostSpec,
    data.Commodity,
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

# A union for all Beancount types
BeancountType = Union[BeancountTuple, inventory.Inventory]

# A dictionary mapping Beancount types to their respective models
type_map: Dict[Type[BeancountType], Type[Model]] = {
    amount.Amount: Amount,
    data.Balance: Balance,
    data.Close: Close,
    data.Commodity: Commodity,
    position.Cost: Cost,
    position.CostSpec: CostSpec,
    data.Custom: Custom,
    data.Document: Document,
    data.Event: Event,
    data.Note: Note,
    data.Open: Open,
    data.Pad: Pad,
    position.Position: Position,
    data.Posting: Posting,
    data.Price: Price,
    data.Query: Query,
    data.Transaction: Transaction,
    data.TxnPosting: TxnPosting,
    inventory.Inventory: Inventory,
}


class Directives(BaseModel):
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
        dirs = [type_map[type(d)].parse(d) for d in obj]  # type: ignore
        return Directives(__root__=dirs)

    def export(self) -> List[data.Directive]:
        """Exports this model into a list of beancount directives

        Returns:
            The list of beancount directives
        """
        dirs = [d.export() for d in self.__root__]
        return dirs


# Update forward references
Directives.update_forward_refs()
Inventory.update_forward_refs()


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


def _recursive_parse(b: BeancountTuple) -> Dict[str, Any]:
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
        if _is_named_tuple(value):
            result[key] = _recursive_parse(value)
        elif isinstance(value, list) and value:
            if _is_named_tuple(value[0]):
                result[key] = [_recursive_parse(c) for c in value]
        else:
            result[key] = value

    return result


def _recursive_export(b: ModelTuple) -> Dict[str, Any]:
    """Recursively exports a ModelTuple into a nested dictionary

    Args:
        b: The ModelTuple to recursively export

    Returns:
        A nested dictionary with all exported Beancount types
    """
    result: Dict[str, Any] = {}
    for key, value in b.__dict__.items():
        if isinstance(value, Base):
            result[key] = value._sibling(**_recursive_export(value))
        elif isinstance(value, list) and value:
            if isinstance(value[0], Base):
                result[key] = [
                    c._sibling(**_recursive_export(c)) for c in value
                ]
        else:
            result[key] = value

    return result
