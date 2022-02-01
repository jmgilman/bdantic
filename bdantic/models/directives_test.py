from beancount.core import data
from .data import Amount, Cost, CostSpec
from decimal import Decimal
from .directives import (
    Balance,
    Close,
    Commodity,
    Custom,
    Document,
    Event,
    Meta,
    Note,
    Open,
    Pad,
    Posting,
    Price,
    Query,
    Transaction,
    TxnPosting,
)
from hypothesis import given, strategies as s
from testing import common as t

r = [Amount, Cost, CostSpec, Meta, Posting, Transaction]


def setup_module(_):
    s.register_type_strategy(Decimal, s.decimals(allow_nan=False))


def build_meta():
    return s.dictionaries(s.text(), s.text())


@given(
    s.builds(
        data.Balance,
        meta=build_meta(),
    )
)
def test_balance(b: data.Balance):
    pb = Balance.parse(b)
    t.compare_object(pb, b, t.Ctx(recurse=r))
    t.compare_object(pb.export(), b, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Close,
        meta=build_meta(),
    )
)
def test_close(c: data.Close):
    pc = Close.parse(c)
    t.compare_object(pc, c, t.Ctx(recurse=r))
    t.compare_object(pc.export(), c, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Commodity,
        meta=build_meta(),
    )
)
def test_commodity(c: data.Commodity):
    pc = Commodity.parse(c)
    t.compare_object(pc, c, t.Ctx(recurse=r))
    t.compare_object(pc.export(), c, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Custom,
        meta=build_meta(),
    )
)
def test_custom(c: data.Custom):
    try:
        pc = Custom.parse(c)
    except AssertionError:
        return

    t.compare_object(pc, c, t.Ctx(recurse=r))
    t.compare_object(pc.export(), c, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Document,
        meta=build_meta(),
    )
)
def test_document(d: data.Document):
    pd = Document.parse(d)
    t.compare_object(pd, d, t.Ctx(recurse=r))
    t.compare_object(pd.export(), d, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Event,
        meta=build_meta(),
    )
)
def test_event(e: data.Event):
    pe = Event.parse(e)
    t.compare_object(pe, e, t.Ctx(recurse=r))
    t.compare_object(pe.export(), e, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Note,
        meta=build_meta(),
    )
)
def test_note(n: data.Note):
    pn = Note.parse(n)
    t.compare_object(pn, n, t.Ctx(recurse=r))
    t.compare_object(pn.export(), n, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Open,
        meta=build_meta(),
    )
)
def test_open(o: data.Open):
    po = Open.parse(o)
    t.compare_object(po, o, t.Ctx(recurse=r))
    t.compare_object(po.export(), o, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Pad,
        meta=build_meta(),
    )
)
def test_pad(p: data.Pad):
    pp = Pad.parse(p)
    t.compare_object(pp, p, t.Ctx(recurse=r))
    t.compare_object(pp.export(), p, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Posting,
        meta=build_meta(),
    )
)
def test_posting(p: data.Posting):
    pp = Posting.parse(p)
    t.compare_object(pp, p, t.Ctx(recurse=r))
    t.compare_object(pp.export(), p, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Price,
        meta=build_meta(),
    )
)
def test_price(p: data.Price):
    pp = Price.parse(p)
    t.compare_object(pp, p, t.Ctx(recurse=r))
    t.compare_object(pp.export(), p, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Query,
        meta=build_meta(),
    )
)
def test_query(q: data.Query):
    pq = Query.parse(q)
    t.compare_object(pq, q, t.Ctx(recurse=r))
    t.compare_object(pq.export(), q, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.Transaction,
        meta=build_meta(),
        tags=s.sets(s.text()),
        links=s.sets(s.text()),
        postings=s.lists(
            s.builds(
                data.Posting,
                meta=build_meta(),
            )
        ),
    )
)
def test_transaction(tr: data.Transaction):
    ptr = Transaction.parse(tr)
    t.compare_object(ptr, tr, t.Ctx(recurse=r))
    t.compare_object(ptr.export(), tr, t.Ctx(partial=False, recurse=r))


@given(
    s.builds(
        data.TxnPosting,
        txn=s.builds(
            data.Transaction,
            meta=build_meta(),
            tags=s.sets(s.text()),
            links=s.sets(s.text()),
            postings=s.lists(
                s.builds(
                    data.Posting,
                    meta=build_meta(),
                )
            ),
        ),
        posting=s.builds(
            data.Posting,
            meta=build_meta(),
        ),
    )
)
def test_txnposting(tr: data.TxnPosting):
    ptr = TxnPosting.parse(tr)
    t.compare_object(ptr, tr, t.Ctx(recurse=r))
    t.compare_object(ptr.export(), tr, t.Ctx(partial=False, recurse=r))
