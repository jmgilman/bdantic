from beancount.core import data
from .data import Amount, Cost, CostSpec
from decimal import Decimal
from .directives import Meta, Posting, Transaction
from .file import Entries, Options
from hypothesis import given, strategies as s
from testing import common as t
from ..types import OptionValues
from typing import Dict, List, Type

r = [Amount, Cost, CostSpec, Meta, Posting, Transaction]


def build_with_meta(t: Type):
    return s.builds(t, meta=s.dictionaries(s.text(), s.text()))


def reject(obj):
    if not isinstance(obj, list):
        return False
    elif obj:
        for v in obj:
            if isinstance(v, list):
                return False

    return True


def setup_module(_):
    s.register_type_strategy(
        Decimal, s.decimals(allow_nan=False, allow_infinity=False)
    )


@given(
    s.recursive(
        build_with_meta(data.Balance)
        | build_with_meta(data.Close)
        | build_with_meta(data.Commodity)
        | s.builds(
            data.Custom,
            meta=s.dictionaries(s.text(), s.text()),
            values=s.lists(s.text()),
        )
        | build_with_meta(data.Document)
        | build_with_meta(data.Event)
        | build_with_meta(data.Note)
        | build_with_meta(data.Open)
        | build_with_meta(data.Query)
        | build_with_meta(data.Pad)
        | build_with_meta(data.Price)
        | s.builds(
            data.Transaction,
            meta=s.dictionaries(s.text(), s.text()),
            tags=s.sets(s.text()),
            links=s.sets(s.text()),
            postings=s.lists(
                s.builds(data.Posting, meta=s.dictionaries(s.text(), s.text()))
            ),
        ),
        s.lists,
        max_leaves=5,
    ).filter(reject)
)
def test_entries(e: List[data.Directive]):
    pe = Entries.parse(e)

    for i, en in enumerate(pe):
        t.compare_object(en, e[i], ctx=t.Ctx(recurse=r))


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
