from __future__ import annotations

from .base import Base
from .data import Account, Inventory
from .directives import TxnPosting
from beancount.core import realization
from ..parse import export_all, parse_all
from ..types import ModelDirective
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
            txn_postings=parse_all(obj.txn_postings),
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

        ra.txn_postings = export_all(self.txn_postings)  # type: ignore
        ra.balance = self.balance.export()

        return ra
