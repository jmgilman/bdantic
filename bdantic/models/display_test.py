from beancount.core import display_context, distribution
from .display import CurrencyContext, DisplayContext, Distribution
from hypothesis import given, strategies as s
from testing import common as t, generate as g


def setup_module(_):
    g.register()


def build_distribution():
    return s.builds(
        Distribution,
        hist=s.dictionaries(s.integers(), s.integers()),
    )


def build_currencycontext():
    return s.builds(
        CurrencyContext,
        fractional_dist=build_distribution(),
    )


@given(build_currencycontext())
def test_currencycontext(c: CurrencyContext):
    bd = distribution.Distribution()
    bd.hist = c.fractional_dist.hist

    bcc = display_context._CurrencyContext()
    bcc.has_sign = c.has_sign
    bcc.integer_max = c.integer_max
    bcc.fractional_dist = bd

    pc = CurrencyContext.parse(bcc)
    t.compare_object(pc, bcc, t.Ctx(recurse=g.recurse))
    t.compare_object(pc.export(), bcc, t.Ctx(partial=False, recurse=g.recurse))


@given(
    s.builds(
        DisplayContext,
        ccontexts=s.dictionaries(s.text(), build_currencycontext()),
    )
)
def test_displaycontext(c: DisplayContext):
    ccs = {}
    for key, cc in c.ccontexts.items():
        bd = distribution.Distribution()
        bd.hist = cc.fractional_dist.hist

        bcc = display_context._CurrencyContext()
        bcc.has_sign = cc.has_sign
        bcc.integer_max = cc.integer_max
        bcc.fractional_dist = bd
        ccs[key] = cc

    bdc = display_context.DisplayContext()
    bdc.ccontexts = ccs
    bdc.commas = c.commas

    pdc = DisplayContext.parse(bdc)
    t.compare_object(pdc, bdc, t.Ctx(recurse=g.recurse))
    t.compare_object(
        pdc.export(), bdc, t.Ctx(partial=False, recurse=g.recurse)
    )


@given(build_distribution())
def test_distribution(d: Distribution):
    bd = distribution.Distribution()
    bd.hist = d.hist

    pd = Distribution.parse(bd)
    t.compare_object(pd, bd, t.Ctx(recurse=g.recurse))
    t.compare_object(pd.export(), bd, t.Ctx(partial=False, recurse=g.recurse))
