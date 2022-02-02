from __future__ import annotations

from .base import Base
from beancount.core import realization
from .data import Account as AccountName, Inventory
from datetime import date
from .directives import Close, Open, TxnPosting
from pydantic import BaseModel
from ..types import ModelDirective, type_map
from typing import cast, Dict, List, Literal, Optional, Union


class Account(BaseModel):
    """A simplified view of an entire beancount account.

    Attributes:
        balance: A mapping of currencies to inventories
        close: The (optional) date the account was closed
        directives: All directives associated with this account
        open: The date the account was opened
        name: The account name
    """

    balance: Dict[str, Inventory]
    close: Optional[date]
    directives: List[Union[ModelDirective, TxnPosting]]
    open: date
    name: str

    @staticmethod
    def from_real(ra: RealAccount) -> Account:
        """Creates a new instance of Account using details from a RealAccount.

        Args:
            ra: The RealAccount to use

        Returns:
            A new instance of Account
        """
        open = cast(
            List[Open],
            list(
                filter(lambda d: isinstance(d, Open), ra.txn_postings),
            ),
        )
        assert len(open) == 1

        close = cast(
            List[Close],
            list(
                filter(lambda d: isinstance(d, Close), ra.txn_postings),
            ),
        )
        assert len(close) < 2
        if close:
            close_date = close[0].date
        else:
            close_date = None

        return Account(
            balance=ra.cur_map,
            close=close_date,
            directives=ra.txn_postings,
            open=open[0].date,
            name=ra.account,
        )


class RealAccount(Base, smart_union=True):
    """A model representing a beancount.core.realize.RealAccount."""

    ty: Literal["RealAccount"] = "RealAccount"
    account: AccountName
    balance: Inventory
    children: Dict[str, RealAccount]
    cur_map: Dict[str, Inventory]
    txn_postings: List[Union[ModelDirective, TxnPosting]]

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

        split = obj.balance.split()
        map = {}
        for k, v in split.items():
            map[k] = Inventory.parse(v)

        return RealAccount(
            account=obj.account,
            balance=Inventory.parse(obj.balance),
            children=children,
            cur_map=map,
            txn_postings=[
                type_map[type(d)].parse(d)  # type: ignore
                for d in obj.txn_postings
            ],
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

    def to_account(self) -> Account:
        """Converts this RealAccount into an Account instance.

        Returns:
            A new Account instance
        """
        return Account.from_real(self)
