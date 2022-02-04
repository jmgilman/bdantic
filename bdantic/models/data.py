"""Provides models for the core beancount data types."""

from __future__ import annotations

import datetime

from .base import Base, BaseList
from beancount.core import (
    amount,
    inventory,
    position,
)
from decimal import Decimal
from typing import List, Literal, Optional

Account = str
Currency = str
Flag = str


class Amount(Base):
    """A model representing a `beancount.core.amount.Amount`.

    Attributes:
        ty: A string literal identifying this model.
        number: The value of the amount.
        currency: The amount currency.
    """

    _sibling = amount.Amount

    ty: Literal["Amount"] = "Amount"
    number: Optional[Decimal]
    currency: Optional[Currency]


class Cost(Base):
    """A model representing a `beancount.core.position.Cost`.

    Attributes:
        ty: A string literal identifying this model.
        number: The per-unit cost.
        currency: The cost currency.
        date: A date that the lot was created at.
        label: An optional label for the lot.
    """

    _sibling = position.Cost

    ty: Literal["Cost"] = "Cost"
    number: Decimal
    currency: Currency
    date: datetime.date
    label: Optional[str]


class CostSpec(Base):
    """A model representing a `beancount.core.position.CostSpec`.

    Attributes:
        ty: A string literal identifying this model.
        number_per: The cost/price per unit.
        number_total: The total cost/price, or None if unspecified.
        currency: The commodity of the amount.
        date: A date for the lot.
        label: An optional label for the lot.
        merge: True if this specification calls for averaging the units of this
            lot's currency, or False if unspecified.
    """

    _sibling = position.CostSpec

    ty: Literal["CostSpec"] = "CostSpec"
    number_per: Optional[Decimal]
    number_total: Optional[Decimal]
    currency: Optional[Currency]
    date: Optional[datetime.date]
    label: Optional[str]
    merge: Optional[bool]


class Inventory(BaseList):
    """A model representing a `beancount.core.inventory.Inventory`.

    A beancount inventory mimics a dictionary, but ultimately the data
    underlying it is a list of Positions. This model represents this fact by
    wrapping a list of [Position][bdantic.models.data.Position] models. It
    inherits basic list functionality and can be indexed/iterated over."""

    __root__: List[Position]

    @classmethod
    def parse(cls, obj: inventory.Inventory) -> Inventory:
        positions = [
            Position.parse(position) for position in obj.get_positions()
        ]
        return Inventory(__root__=positions)

    def export(self) -> inventory.Inventory:
        positions = [position.export() for position in self.__root__]
        return inventory.Inventory(positions=positions)


class Position(Base):
    """A model representing a `beancount.core.position.Position`.

    Attributes:
        ty: A string literal identifying this model.
        units: The number of units and its currency.
        cost: A Cost that represents the lot.
    """

    _sibling = position.Position

    ty: Literal["Position"] = "Position"
    units: Amount
    cost: Optional[Cost]


# Update forward references
Inventory.update_forward_refs()
