import pytest

from beancount.core import data
from . import directives
from .file import BeancountFile, Directives, IDNotFoundError, Options
from hypothesis import given, strategies as s
from testing import common as t, generate as g
from ..types import OptionValues
from typing import Dict, List


def setup_module(_):
    g.register()


def reject(obj):
    if not isinstance(obj, list):
        return False
    elif obj:
        for v in obj:
            if isinstance(v, list):
                return False

    return True


@given(
    s.recursive(
        g.directive(data.Balance)
        | g.directive(data.Close)
        | g.directive(data.Commodity)
        | g.custom()
        | g.directive(data.Document)
        | g.directive(data.Event)
        | g.directive(data.Note)
        | g.directive(data.Open)
        | g.directive(data.Query)
        | g.directive(data.Pad)
        | g.directive(data.Price)
        | g.transaction(),
        s.lists,
        max_leaves=5,
    ).filter(reject)
)
def test_directives(d: List[data.Directive]):
    pd = Directives.parse(d)

    for i, en in enumerate(pd):
        t.compare_object(en, d[i], ctx=t.Ctx(recurse=g.recurse))


@given(
    g.directive(data.Open, account=g.account()),
    g.directive(data.Balance, account=g.account()),
    g.transaction(),
)
def test_directives_by_account(op, bal, txn):
    if len(set([op.account, bal.account, txn.postings[0].account])) != 3:
        return

    dirs = Directives.parse([op, bal, txn])
    pop = directives.Open.parse(op)
    pbal = directives.Balance.parse(bal)
    ptxn = directives.Transaction.parse(txn)

    assert dirs.by_account(pop.account) == Directives(__root__=[pop])
    assert dirs.by_account(pbal.account) == Directives(__root__=[pbal])
    assert dirs.by_account(ptxn.postings[0].account) == Directives(
        __root__=[ptxn]
    )


@given(g.directive(data.Open), g.directive(data.Balance), g.transaction())
def test_directives_by_id(op, bal, txn):
    dirs = Directives.parse([op, bal, txn])
    pop = directives.Open.parse(op)
    pbal = directives.Balance.parse(bal)
    ptxn = directives.Transaction.parse(txn)

    assert dirs.by_id(pop.id) == pop
    assert dirs.by_id(pbal.id) == pbal
    assert dirs.by_id(ptxn.id) == ptxn

    assert dirs.by_ids([pop.id, pbal.id, ptxn.id]) == [pop, pbal, ptxn]

    with pytest.raises(IDNotFoundError):
        dirs.by_id("a")


@given(g.directive(data.Open), g.directive(data.Balance), g.transaction())
def test_directives_by_type(op, bal, txn):
    dirs = Directives.parse([op, bal, txn])
    pop = directives.Open.parse(op)
    pbal = directives.Balance.parse(bal)
    ptxn = directives.Transaction.parse(txn)

    assert dirs.by_type(directives.Open) == Directives(__root__=[pop])
    assert dirs.by_type(directives.Balance) == Directives(__root__=[pbal])
    assert dirs.by_type(directives.Transaction) == Directives(__root__=[ptxn])


@given(
    s.dictionaries(
        s.text(),
        s.one_of(
            [
                s.booleans(),
                s.text(),
                s.integers(),
                s.decimals(allow_nan=False),
                s.sampled_from(data.Booking),
                s.lists(s.text()),
            ]
        ),
    )
)
def test_options(o: Dict[str, OptionValues]):
    po = Options.parse(o)
    t.compare_dict(o, po.__root__, t.Ctx())


@given(
    g.transaction(),
    s.dictionaries(
        s.text(),
        s.one_of(
            [
                s.booleans(),
                s.text(),
                s.integers(),
                s.decimals(allow_nan=False),
                s.sampled_from(data.Booking),
                s.lists(s.text()),
            ]
        ),
    ),
)
def test_file_compress(txn, opts):
    bf = BeancountFile.parse(([txn], [], opts))
    assert bf.decompress(bf.compress()) == bf
