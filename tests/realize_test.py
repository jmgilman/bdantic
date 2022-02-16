from typing import Any

import beancount_hypothesis as h
from beancount.core import data, realization
from conftest import Ctx
from hypothesis import given
from hypothesis import strategies as s

from bdantic.models import realize


@given(
    s.lists(h.txnposting(), max_size=2),
    h.account_name(),
    h.inventory(),
    h.open(),
)
def test_account(ctx: Ctx, txns, acct, inv, open):
    ra = realization.RealAccount(acct)
    ra.txn_postings = [open] + txns
    ra.balance = inv

    a = realize.Account.parse(ra)

    balance = {}
    for k, v in ra.balance.split().items():
        balance[k] = v.get_positions()
    ctx.compare_dict(a.balance, balance)
    assert a.close is None
    assert a.name == ra.account
    assert a.open == open.date


@given(h.transactions())
def test_realaccount(txns):
    ra = realization.realize(txns)
    pra = realize.RealAccount.parse(ra)
    era = pra.export()

    assert era == ra


def test_realize(beanfile: tuple[list[data.Directive], list, dict[str, Any]]):
    entries, _, _ = beanfile
    ra = realization.realize(entries)
    pra = realize.RealAccount.parse(ra)
    era = pra.export()

    assert era == ra
