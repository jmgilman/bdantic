"""Provides models for representing the results of running a realization."""

from __future__ import annotations

from .base import Base, BaseList
from beancount.core import data, realization
from .data import Account as AccountName, Inventory
from datetime import date
from .directives import Balance, Close, Document, Note, Open, Pad, TxnPosting
from pydantic import BaseModel
from typing import Dict, List, Literal, Optional, Type, TypeVar, Union

T = TypeVar("T", bound="ModelTxnPosting")

ModelTxnPosting = Union[Balance, Close, Document, Note, Open, Pad, TxnPosting]
BeanTxnPosting = Union[
    data.Balance,
    data.Close,
    data.Document,
    data.Note,
    data.Open,
    data.Pad,
    data.TxnPosting,
]

_type_map: Dict[Type[BeanTxnPosting], Type[ModelTxnPosting]] = {
    data.Balance: Balance,
    data.Close: Close,
    data.Document: Document,
    data.Note: Note,
    data.Open: Open,
    data.Pad: Pad,
    data.TxnPosting: TxnPosting,
}


class Account(BaseModel):
    """A simplified view of an entire beancount account.

    The primary differenece between this and a `RealAccount` is that it strips
    out all children and directives associated with the account. Additionally,
    it added some useful data about an account like open/close date. The
    removal of the children and directives greatly reduces the size of this
    object, especially when serialized.

    Attributes:
        balance: A mapping of currencies to inventories.
        close: The (optional) date the account was closed.
        name: The account name.
        open: The date the account was opened.
    """

    balance: Dict[str, Inventory]
    close: Optional[date]
    name: str
    open: date

    @staticmethod
    def parse(obj: realization.RealAccount) -> Account:
        """Parses a beancount RealAccount into this model

        Args:
            obj: The Beancount RealAccount

        Returns:
            A new instance of this model
        """
        open_date = None
        close_date = None
        for dir in obj.txn_postings:
            if isinstance(dir, data.Open):
                open_date = dir.date
            elif isinstance(dir, data.Close):
                close_date = dir.date

        split = obj.balance.split()
        map = {}
        for k, v in split.items():
            map[k] = Inventory.parse(v)

        return Account(
            balance=map,
            close=close_date,
            open=open_date,
            name=obj.account,
        )

    @staticmethod
    def from_real(ra: RealAccount) -> Account:
        """Creates a new instance of `Account` using details from a
        [RealAccount][bdantic.models.realize.RealAccount].

        Args:
            ra: The RealAccount to use

        Returns:
            A new instance of Account
        """
        open = ra.txn_postings.by_type(Open)
        assert open is not None
        assert len(open) == 1

        close = ra.txn_postings.by_type(Close)
        if close:
            assert len(close) < 2
            close_date = close[0].date
        else:
            close_date = None

        return Account(
            balance=ra.cur_map,
            close=close_date,
            open=open[0].date,
            name=ra.account,
        )

    def export(self):
        raise NotImplementedError


class RealAccount(Base, smart_union=True):
    """A model representing a `beancount.core.realize.RealAccount`.

    A `RealAccount` is represented as a dictionary in beancount which contains
    additional attributes for describing details about the account. This model
    matches those details, however, the dictinary representation of a
    `RealAccount` is moved to the dedicated `children` field.

    Attributes:
        ty: A string literal identifying this model.
        account: The account name.
        balance: The balance of the account
        children: All children that belong to this account.
        cur_map: A map of currencies to their respective balances.
        txn_postings: A list of directives in which this account appears.
    """

    ty: Literal["RealAccount"] = "RealAccount"
    account: AccountName
    balance: Inventory
    children: Dict[str, RealAccount]
    cur_map: Dict[str, Inventory]
    txn_postings: TxnPostings

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
            txn_postings=TxnPostings.parse(obj.txn_postings),  # type: ignore
        )

    def export(self) -> realization.RealAccount:
        """Exports this model into a beancount RealAccount

        Returns:
            A new instance of a beancount RealAccount
        """
        ra = realization.RealAccount(self.account)
        for k, v in self.children.items():
            ra[k] = v.export()

        ra.txn_postings = self.txn_postings.export()  # type: ignore
        ra.balance = self.balance.export()

        return ra

    # def to_account(self) -> Account:
    #     """Converts this RealAccount into an Account instance.

    #     Returns:
    #         A new Account instance
    #     """
    #     return Account.from_real(self)


class TxnPostings(BaseList):
    """A model representing the txnpostings found within RealAccount's."""

    __root__: List[ModelTxnPosting]

    @classmethod
    def parse(
        cls,
        obj: List[BeanTxnPosting],
    ) -> TxnPostings:
        return TxnPostings(
            __root__=[_type_map[type(d)].parse(d) for d in obj]  # type: ignore
        )

    def export(self) -> List[BeanTxnPosting]:
        return [d.export() for d in self.__root__]

    def by_type(self, ty: Type[T]) -> TxnPostings:
        """Returns a new instance of `TxnPostings` filtered by the given type.

        Args:
            ty: The type to filter by.

        Returns:
            A new instance of `TxnPostings` with the filtered results.
        """
        return TxnPostings(__root__=super()._by_type(ty))


# Update forward references
Account.update_forward_refs()
RealAccount.update_forward_refs()
TxnPostings.update_forward_refs()
