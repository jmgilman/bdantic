import pytest
import beancount_hypothesis as h
from beancount_hypothesis.directive import query
from beancount.core import data
from bdantic import types
from bdantic.models import directives, file
from hypothesis import given, strategies as s
from typing import Dict, List
from unittest import mock
from conftest import Ctx


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
        h.balance()
        | h.close()
        | h.commodity()
        | h.custom()
        | h.document()
        | h.event()
        | h.note()
        | h.open()
        | query()
        | h.pad()
        | h.price()
        | h.transaction(),
        s.lists,
        max_leaves=5,
    ).filter(reject)
)
def test_directives(ctx: Ctx, d: List[data.Directive]):
    pd = file.Directives.parse(d)

    for i, en in enumerate(pd):
        ctx.compare_object(en, d[i])


@given(
    h.open(),
    h.balance(),
    h.transaction(),
)
def test_directives_by_account(op, bal, txn):
    if len(set([op.account, bal.account, txn.postings[0].account])) != 3:
        return

    dirs = file.Directives.parse([op, bal, txn])
    pop = directives.Open.parse(op)
    pbal = directives.Balance.parse(bal)
    ptxn = directives.Transaction.parse(txn)

    assert dirs.by_account(pop.account) == file.Directives(__root__=[pop])
    assert dirs.by_account(pbal.account) == file.Directives(__root__=[pbal])
    assert dirs.by_account(ptxn.postings[0].account) == file.Directives(
        __root__=[ptxn]
    )


@given(h.open(), h.balance(), h.transaction())
def test_directives_by_id(op, bal, txn):
    dirs = file.Directives.parse([op, bal, txn])
    pop = directives.Open.parse(op)
    pbal = directives.Balance.parse(bal)
    ptxn = directives.Transaction.parse(txn)

    assert dirs.by_id(pop.id) == pop
    assert dirs.by_id(pbal.id) == pbal
    assert dirs.by_id(ptxn.id) == ptxn

    assert dirs.by_ids([pop.id, pbal.id, ptxn.id]) == [pop, pbal, ptxn]

    with pytest.raises(file.IDNotFoundError):
        dirs.by_id("a")


@given(h.open(), h.balance(), h.transaction())
def test_directives_by_type(op, bal, txn):
    dirs = file.Directives.parse([op, bal, txn])
    pop = directives.Open.parse(op)
    pbal = directives.Balance.parse(bal)
    ptxn = directives.Transaction.parse(txn)

    assert dirs.by_type(directives.Open) == file.Directives(__root__=[pop])
    assert dirs.by_type(directives.Balance) == file.Directives(__root__=[pbal])
    assert dirs.by_type(directives.Transaction) == file.Directives(
        __root__=[ptxn]
    )


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
def test_options(ctx: Ctx, o: Dict[str, types.OptionValues]):
    po = file.Options.parse(o)
    ctx.compare_dict(o, po.__dict__)


@given(
    h.transaction(),
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
    bf = file.BeancountFile.parse(([txn], [], opts))
    assert bf.decompress(bf.compress()) == bf


@mock.patch("beancount.loader.compute_input_hash")
def test_file_hash(loader):
    opts = file.Options(filename="test.beancount")
    dirs = file.Directives(__root__=[])
    bf = file.BeancountFile(entries=dirs, options=opts, errors=[], accounts={})
    loader.return_value = "hash"

    result = bf.hash()
    loader.assert_called_with(["test.beancount"])
    assert result == "hash"

    opts = file.Options(include=["test.beancount", "test1.beancount"])
    bf = file.BeancountFile(entries=dirs, options=opts, errors=[], accounts={})

    bf.hash()
    loader.assert_called_with(["test.beancount", "test1.beancount"])


@mock.patch("bdantic.models.query.QueryResult.parse")
@mock.patch("beancount.query.query.run_query")
def test_file_query(query, response):
    bf = file.BeancountFile(entries=[], options={}, errors=[], accounts=[])
    query.return_value = "query"
    response.return_value = "response"
    result = bf.query("test")

    query.assert_called_once_with([], bf.options, "test")
    response.assert_called_once_with("query")

    assert result == "response"


@mock.patch("bdantic.models.realize.RealAccount.parse")
@mock.patch("beancount.core.realization.realize")
def test_file_realize(realize, acct):
    bf = file.BeancountFile(entries=[], options={}, errors=[], accounts=[])
    realize.return_value = "realize"
    acct.return_value = "response"
    result = bf.realize()

    realize.assert_called_once_with([])
    acct.assert_called_once_with("realize")

    assert result == "response"
