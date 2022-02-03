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
    """A model representing a beancount.core.amount.Amount."""

    _sibling = amount.Amount

    ty: Literal["Amount"] = "Amount"
    number: Optional[Decimal]
    currency: Optional[Currency]


class Cost(Base):
    """A model representing a beancount.core.position.Cost."""

    _sibling = position.Cost

    ty: Literal["Cost"] = "Cost"
    number: Decimal
    currency: Currency
    date: datetime.date
    label: Optional[str]


class CostSpec(Base):
    """A model representing a beancount.core.position.CostSpec."""

    _sibling = position.CostSpec

    ty: Literal["CostSpec"] = "CostSpec"
    number_per: Optional[Decimal]
    number_total: Optional[Decimal]
    currency: Optional[Currency]
    date: Optional[datetime.date]
    label: Optional[str]
    merge: Optional[bool]


class Inventory(BaseList):
    """A model representing a beancount.core.inventory.Inventory."""

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
    """A model representing a beancount.core.position.Position."""

    _sibling = position.Position

    ty: Literal["Position"] = "Position"
    units: Amount
    cost: Optional[Cost]


# Update forward references
Inventory.update_forward_refs()
