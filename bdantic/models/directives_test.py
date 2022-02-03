from beancount.core import data
from beancount.parser import parser  # type: ignore
from .directives import (
    Balance,
    Close,
    Commodity,
    Custom,
    Document,
    Event,
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
from testing import common as t, generate as g, syntax as sy


def setup_module(_):
    g.register()


def build_meta():
    return s.dictionaries(s.text(), s.text())


def test_syntax():
    def strip(s: str) -> str:
        return s.strip().replace(" ", "").replace("\n", "")

    for test in sy.tests:
        d = parser.parse_string(test[0])[0][0]
        pd = test[1].parse(d)
        syn = pd.syntax()

        assert strip(test[0]) == strip(syn)


@given(g.directive(data.Balance))
def test_balance(b: data.Balance):
    pb = Balance.parse(b)
    t.compare_object(pb, b, t.Ctx(recurse=g.recurse))
    t.compare_object(pb.export(), b, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Close))
def test_close(c: data.Close):
    pc = Close.parse(c)
    t.compare_object(pc, c, t.Ctx(recurse=g.recurse))
    t.compare_object(pc.export(), c, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Commodity))
def test_commodity(c: data.Commodity):
    pc = Commodity.parse(c)
    t.compare_object(pc, c, t.Ctx(recurse=g.recurse))
    t.compare_object(pc.export(), c, t.Ctx(partial=False, recurse=g.recurse))


@given(g.custom())
def test_custom(c: data.Custom):
    pc = Custom.parse(c)
    t.compare_object(pc, c, t.Ctx(recurse=g.recurse))
    t.compare_object(pc.export(), c, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Document))
def test_document(d: data.Document):
    pd = Document.parse(d)
    t.compare_object(pd, d, t.Ctx(recurse=g.recurse))
    t.compare_object(pd.export(), d, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Event))
def test_event(e: data.Event):
    pe = Event.parse(e)
    t.compare_object(pe, e, t.Ctx(recurse=g.recurse))
    t.compare_object(pe.export(), e, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Note))
def test_note(n: data.Note):
    pn = Note.parse(n)
    t.compare_object(pn, n, t.Ctx(recurse=g.recurse))
    t.compare_object(pn.export(), n, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Open))
def test_open(o: data.Open):
    po = Open.parse(o)
    t.compare_object(po, o, t.Ctx(recurse=g.recurse))
    t.compare_object(po.export(), o, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Pad))
def test_pad(p: data.Pad):
    pp = Pad.parse(p)
    t.compare_object(pp, p, t.Ctx(recurse=g.recurse))
    t.compare_object(pp.export(), p, t.Ctx(partial=False, recurse=g.recurse))


@given(g.posting())
def test_posting(p: data.Posting):
    pp = Posting.parse(p)
    t.compare_object(pp, p, t.Ctx(recurse=g.recurse))
    t.compare_object(pp.export(), p, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Price))
def test_price(p: data.Price):
    pp = Price.parse(p)
    t.compare_object(pp, p, t.Ctx(recurse=g.recurse))
    t.compare_object(pp.export(), p, t.Ctx(partial=False, recurse=g.recurse))


@given(g.directive(data.Query))
def test_query(q: data.Query):
    pq = Query.parse(q)
    t.compare_object(pq, q, t.Ctx(recurse=g.recurse))
    t.compare_object(pq.export(), q, t.Ctx(partial=False, recurse=g.recurse))


@given(g.transaction())
def test_transaction(tr: data.Transaction):
    ptr = Transaction.parse(tr)
    t.compare_object(ptr, tr, t.Ctx(recurse=g.recurse))
    t.compare_object(ptr.export(), tr, t.Ctx(partial=False, recurse=g.recurse))


@given(g.txnposting())
def test_txnposting(tr: data.TxnPosting):
    ptr = TxnPosting.parse(tr)
    t.compare_object(ptr, tr, t.Ctx(recurse=g.recurse))
    t.compare_object(ptr.export(), tr, t.Ctx(partial=False, recurse=g.recurse))
