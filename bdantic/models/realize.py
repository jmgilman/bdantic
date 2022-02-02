from __future__ import annotations

from .base import Base
from .data import Account, Inventory
from .directives import TxnPosting
from beancount.core import realization
from ..types import ModelDirective, type_map
from typing import Dict, List, Literal, Union


class RealAccount(Base, smart_union=True):
    """A model representing a beancount.core.realize.RealAccount."""

    ty: Literal["RealAccount"] = "RealAccount"
    account: Account
    txn_postings: List[Union[ModelDirective, TxnPosting]]
    balance: Inventory
    children: Dict[str, RealAccount]

    @classmethod
    def parse(cls, obj: realization.RealAccount) -> RealAccount:
        """Parses a beancount RealAccount into this model

        Args:
            obj: The Beancount RealAccount

        Returns:
            A new instance of this model
        """
        children = {}
        for k, v in obj.items():
            children[k] = RealAccount.parse(v)

        return RealAccount(
            account=obj.account,
            txn_postings=[
                type_map[type(d)].parse(d)  # type: ignore
                for d in obj.txn_postings
            ],
            balance=Inventory.parse(obj.balance),
            children=children,
        )

    def export(self) -> realization.RealAccount:
        """Exports this model into a beancount RealAccount

        Returns:
            A new instance of a beancount RealAccount
        """
        ra = realization.RealAccount(self.account)
        for k, v in self.children.items():
            ra[k] = v.export()

        ra.txn_postings = [
            p.export() for p in self.txn_postings  # type: ignore
        ]
        ra.balance = self.balance.export()

        return ra
