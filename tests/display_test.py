from beancount.core import display_context, distribution
from bdantic.models import display
from hypothesis import given, strategies as s
from conftest import Ctx


def build_distribution():
    return s.builds(
        display.Distribution,
        hist=s.dictionaries(s.integers(), s.integers()),
    )


def build_currencycontext():
    return s.builds(
        display.CurrencyContext,
        fractional_dist=build_distribution(),
    )


@given(build_currencycontext())
def test_currencycontext(ctx: Ctx, c: display.CurrencyContext):
    bd = distribution.Distribution()
    bd.hist = c.fractional_dist.hist

    bcc = display_context._CurrencyContext()
    bcc.has_sign = c.has_sign
    bcc.integer_max = c.integer_max
    bcc.fractional_dist = bd

    pc = display.CurrencyContext.parse(bcc)
    ctx.compare_object(pc, bcc)
    ctx.compare_object(pc.export(), bcc, False)


@given(
    s.builds(
        display.DisplayContext,
        ccontexts=s.dictionaries(s.text(), build_currencycontext()),
    )
)
def test_displaycontext(ctx: Ctx, c: display.DisplayContext):
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

    pdc = display.DisplayContext.parse(bdc)
    ctx.compare_object(pdc, bdc)
    ctx.compare_object(pdc.export(), bdc, False)


@given(build_distribution())
def test_distribution(ctx: Ctx, d: display.Distribution):
    bd = distribution.Distribution()
    bd.hist = d.hist

    pd = display.Distribution.parse(bd)
    ctx.compare_object(pd, bd)
    ctx.compare_object(pd.export(), bd, False)
