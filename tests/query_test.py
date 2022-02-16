import string
from copy import copy
from typing import Any, Dict, List, Tuple, Type

import beancount_hypothesis as h
from beancount.core import amount, data
from beancount.query import query as bquery
from conftest import Ctx
from hypothesis import given
from hypothesis import strategies as s

from bdantic.models import query


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
                        h.amount(),
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
def test_queryresult(
    ctx: Ctx, r: Tuple[List[Tuple[str, Type]], List[Dict[str, Any]]]
):
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

    pr = query.QueryResult.parse((r[0], rows))
    er = pr.export()

    columns = [(column.name, query._map[column.type]) for column in pr.columns]
    ctx.compare_list(er[0], columns)
    ctx.compare_list([r._asdict() for r in er[1]], pr.rows)
    ctx.compare_list(er[0], r[0], False)
    ctx.compare_list(
        [r._asdict() for r in er[1]],
        [r._asdict() for r in rows],
        False,
    )


def test_query(
    ctx: Ctx, beanfile: tuple[list[data.Directive], list, dict[str, Any]]
):
    entries, _, options = beanfile
    result = bquery.run_query(
        entries, options, "SELECT date, narration, account, position"
    )
    pr = query.QueryResult.parse(result)
    er = pr.export()

    ctx.compare_list(
        er[0],
        result[0],
        False,
    )
    ctx.compare_list(
        er[1],
        result[1],
        False,
    )
