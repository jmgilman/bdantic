import pytest

from beancount.core import data
from . import directives
from .file import BeancountFile, Directives, IDNotFoundError, Options
from hypothesis import given, strategies as s
from testing import common as t, generate as g
from ..types import OptionValues
from typing import Dict, List
from unittest import mock


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
    t.compare_dict(o, po.__dict__, t.Ctx())


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


@mock.patch("beancount.loader.compute_input_hash")
def test_file_hash(loader):
    opts = Options(filename="test.beancount")
    dirs = Directives(__root__=[])
    bf = BeancountFile(entries=dirs, options=opts, errors=[], accounts={})
    loader.return_value = "hash"

    result = bf.hash()
    loader.assert_called_with(["test.beancount"])
    assert result == "hash"

    opts = Options(include=["test.beancount", "test1.beancount"])
    bf = BeancountFile(entries=dirs, options=opts, errors=[], accounts={})

    bf.hash()
    loader.assert_called_with(["test.beancount", "test1.beancount"])


@mock.patch("bdantic.models.query.QueryResult.parse")
@mock.patch("beancount.query.query.run_query")
def test_file_query(query, response):
    bf = BeancountFile(entries=[], options={}, errors=[], accounts=[])
    query.return_value = "query"
    response.return_value = "response"
    result = bf.query("test")

    query.assert_called_once_with([], bf.options, "test")
    response.assert_called_once_with("query")

    assert result == "response"


@mock.patch("bdantic.models.realize.RealAccount.parse")
@mock.patch("beancount.core.realization.realize")
def test_file_realize(realize, acct):
    bf = BeancountFile(entries=[], options={}, errors=[], accounts=[])
    realize.return_value = "realize"
    acct.return_value = "response"
    result = bf.realize()

    realize.assert_called_once_with([])
    acct.assert_called_once_with("realize")

    assert result == "response"
