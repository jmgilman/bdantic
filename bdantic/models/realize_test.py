from beancount import loader
from beancount.core import data, realization
from hypothesis import given, strategies as s
from .realize import Account, RealAccount
from testing import common as t, generate as g


def setup_module(_):
    g.register()


@given(
    s.lists(g.txnposting(), max_size=2),
    g.account(),
    g.inventory(),
    g.directive(data.Open),
)
def test_account(txns, acct, inv, open):
    ra = realization.RealAccount(acct)
    ra.txn_postings = [open] + txns
    ra.balance = inv

    a = Account.parse(ra)

    balance = {}
    for k, v in ra.balance.split().items():
        balance[k] = v.get_positions()
    t.compare_dict(a.balance, balance, t.Ctx(recurse=g.recurse))
    t.compare_list(a.directives, ra.txn_postings, t.Ctx(recurse=g.recurse))
    assert a.close is None
    assert a.name == ra.account
    assert a.open == open.date


@given(g.transactions())
def test_realaccount(txns):
    ra = realization.realize(txns)
    pra = RealAccount.parse(ra)
    era = pra.export()

    assert era == ra


def test_realize():
    entries, _, options = loader.load_file("testing/static.beancount")
    ra = realization.realize(entries)
    pra = RealAccount.parse(ra)
    era = pra.export()

    assert era == ra
