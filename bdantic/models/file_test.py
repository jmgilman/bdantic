from beancount.core import data
from .file import Directives, Options
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
