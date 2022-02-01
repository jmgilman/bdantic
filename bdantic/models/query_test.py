import string

from beancount import loader
from beancount.core import amount
from beancount.query import query  # type: ignore
from copy import copy
from .data import Amount, Inventory, Position
from decimal import Decimal
from hypothesis import given, strategies as s
from .query import QueryResult
from testing import common as t
from typing import Any, Dict, List, Tuple, Type


def setup_module(_):
    s.register_type_strategy(Decimal, s.decimals(allow_nan=False))


@s.composite
def query_response(draw):
    columns = draw(
        s.lists(
            s.tuples(
                s.uuids().map(lambda u: "a" + str(u).replace("-", "")),
                s.sampled_from([str, int, bool, amount.Amount]),
            ),
            min_size=5,
            max_size=5,
            unique=True,
        ),
    )

    column_names = [c[0] for c in columns]
    data = draw(
        s.lists(
            s.lists(
                s.one_of(
                    [
                        s.text(alphabet=string.ascii_letters, min_size=1),
                        s.integers(),
                        s.decimals(allow_infinity=False, allow_nan=False),
                        s.builds(amount.Amount),
                    ]
                ),
                min_size=5,
                max_size=5,
            ),
            min_size=1,
        )
    )

    # The row columns must match the header columns
    rows = []
    for d in data:
        row = {}
        for i in range(len(column_names)):
            row[column_names[i]] = d[i]
        rows.append(row)

    return (columns, rows)


@given(query_response())
def test_queryresult(r: Tuple[List[Tuple[str, Type]], List[Dict[str, Any]]]):
    class FakeTuple:
        d: Dict[str, Any]

        def __init__(self, d: Dict[str, Any]):
            self.d = d

        def _asdict(self):
            return copy(self.d)

    rows = []
    for row in r[1]:
        ft = FakeTuple(row)
        rows.append(ft)

    pr = QueryResult.parse((r[0], rows))
    er = pr.export()

    t.compare_list(er[0], pr.columns, t.Ctx(recurse=[Amount]))
    t.compare_list(
        [r._asdict() for r in er[1]], pr.rows, t.Ctx(recurse=[Amount])
    )
    t.compare_list(er[0], r[0], t.Ctx(partial=False, recurse=[Amount]))
    t.compare_list(
        [r._asdict() for r in er[1]],
        [r._asdict() for r in rows],
        t.Ctx(partial=False, recurse=[Amount]),
    )


def test_query():
    entries, errors, options = loader.load_file("testing/static.beancount")
    result = query.run_query(
        entries, options, "SELECT date, narration, account, position"
    )
    pr = QueryResult.parse(result)
    er = pr.export()

    t.compare_list(
        er[0],
        result[0],
        t.Ctx(partial=False, recurse=[Amount, Inventory, Position]),
    )
    t.compare_list(
        er[1],
        result[1],
        t.Ctx(partial=False, recurse=[Amount, Inventory, Position]),
    )