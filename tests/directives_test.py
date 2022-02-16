import beancount_hypothesis as h
from beancount_hypothesis.directive import query
from beancount.core import data
from beancount.parser import parser  # type: ignore
from bdantic.models import directives
from hypothesis import given
from conftest import Ctx


def test_syntax(syntax):
    def strip(s: str) -> str:
        return s.strip().replace(" ", "").replace("\n", "")

    for test in syntax:
        d = parser.parse_string(test[0])[0][0]
        pd = test[1].parse(d)
        syn = pd.syntax()

        assert strip(test[0]) == strip(syn)


@given(h.balance())
def test_balance(ctx: Ctx, b: data.Balance):
    pb = directives.Balance.parse(b)
    ctx.compare_object(pb, b)
    ctx.compare_object(pb.export(), b, False)


@given(h.close())
def test_close(ctx: Ctx, c: data.Close):
    pc = directives.Close.parse(c)
    ctx.compare_object(pc, c)
    ctx.compare_object(pc.export(), c, False)


@given(h.commodity())
def test_commodity(ctx: Ctx, c: data.Commodity):
    pc = directives.Commodity.parse(c)
    ctx.compare_object(pc, c)
    ctx.compare_object(pc.export(), c, False)


@given(h.custom())
def test_custom(ctx: Ctx, c: data.Custom):
    pc = directives.Custom.parse(c)
    ctx.compare_object(pc, c)
    ctx.compare_object(pc.export(), c, False)


@given(h.document())
def test_document(ctx: Ctx, d: data.Document):
    pd = directives.Document.parse(d)
    ctx.compare_object(pd, d)
    ctx.compare_object(pd.export(), d, False)


@given(h.event())
def test_event(ctx: Ctx, e: data.Event):
    pe = directives.Event.parse(e)
    ctx.compare_object(pe, e)
    ctx.compare_object(pe.export(), e, False)


@given(h.note())
def test_note(ctx: Ctx, n: data.Note):
    pn = directives.Note.parse(n)
    ctx.compare_object(pn, n)
    ctx.compare_object(pn.export(), n, False)


@given(h.open())
def test_open(ctx: Ctx, o: data.Open):
    po = directives.Open.parse(o)
    ctx.compare_object(po, o)
    ctx.compare_object(po.export(), o, False)


@given(h.pad())
def test_pad(ctx: Ctx, p: data.Pad):
    pp = directives.Pad.parse(p)
    ctx.compare_object(pp, p)
    ctx.compare_object(pp.export(), p, False)


@given(h.posting())
def test_posting(ctx: Ctx, p: data.Posting):
    pp = directives.Posting.parse(p)
    ctx.compare_object(pp, p)
    ctx.compare_object(pp.export(), p, False)


@given(h.price())
def test_price(ctx: Ctx, p: data.Price):
    pp = directives.Price.parse(p)
    ctx.compare_object(pp, p)
    ctx.compare_object(pp.export(), p, False)


@given(query())
def test_query(ctx: Ctx, q: data.Query):
    pq = directives.Query.parse(q)
    ctx.compare_object(pq, q)
    ctx.compare_object(pq.export(), q, False)


@given(h.transaction())
def test_transaction(ctx: Ctx, tr: data.Transaction):
    ptr = directives.Transaction.parse(tr)
    ctx.compare_object(ptr, tr)
    ctx.compare_object(ptr.export(), tr, False)


@given(h.txnposting())
def test_txnposting(ctx: Ctx, tr: data.TxnPosting):
    ptr = directives.TxnPosting.parse(tr)
    ctx.compare_object(ptr, tr)
    ctx.compare_object(ptr.export(), tr, False)
