from __future__ import annotations

import datetime

from .base import Base
from beancount.core import (
    amount,
    inventory,
    position,
)
from decimal import Decimal
from typing import List, Literal, Optional
from .common import recursive_export, recursive_parse

Account = str
Currency = str
Flag = str


class Amount(Base):
    """A model representing a beancount.core.amount.Amount."""

    _sibling = amount.Amount
    ty: Literal["Amount"] = "Amount"
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
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> amount.Amount:
        """Exports this model into a beancount Amount

        Returns:
            A new instance of a beancount Amount
        """
        return self._sibling(**recursive_export(self))


class Cost(Base):
    """A model representing a beancount.core.position.Cost."""

    _sibling = position.Cost
    ty: Literal["Cost"] = "Cost"
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
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> position.Cost:
        """Exports this model into a beancount Cost

        Returns:
            A new instance of a beancount Cost
        """
        return self._sibling(**recursive_export(self))


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

    @classmethod
    def parse(cls, obj: position.CostSpec) -> CostSpec:
        """Parses a beancount CostSpec into this model

        Args:
            obj: The Beancount CostSpec to parse

        Returns:
            A new instance of this model
        """
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> position.CostSpec:
        """Exports this model into a beancount CostSpec

        Returns:
            A new instance of a beancount CostSpec
        """
        return self._sibling(**recursive_export(self))


class Inventory(Base):
    """A model representing a beancount.core.inventory.Inventory."""

    __root__: List[Position]

    @classmethod
    def parse(cls, obj: inventory.Inventory) -> Inventory:
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
            A new instance of a beancount Inventory
        """
        positions = [position.export() for position in self.__root__]
        return inventory.Inventory(positions=positions)


class Position(Base):
    """A model representing a beancount.core.position.Position."""

    _sibling = position.Position
    ty: Literal["Position"] = "Position"
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
        return cls.parse_obj(recursive_parse(obj))

    def export(self) -> position.Position:
        """Exports this model into a beancount Position

        Returns:
            A new instance of a beancount Position
        """
        return self._sibling(**recursive_export(self))


# Update forward references
Inventory.update_forward_refs()
