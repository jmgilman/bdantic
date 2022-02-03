import string

from beancount import loader
from beancount.core import amount
from beancount.query import query
from copy import copy
from hypothesis import given, strategies as s
from .query import _map, QueryResult
from testing import common as t, generate as g
from typing import Any, Dict, List, Tuple, Type


def setup_module(_):
    g.register()


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

    columns = [(column.name, _map[column.type]) for column in pr.columns]
    t.compare_list(er[0], columns, t.Ctx(recurse=g.recurse))
    t.compare_list(
        [r._asdict() for r in er[1]], pr.rows, t.Ctx(recurse=g.recurse)
    )
    t.compare_list(er[0], r[0], t.Ctx(partial=False, recurse=g.recurse))
    t.compare_list(
        [r._asdict() for r in er[1]],
        [r._asdict() for r in rows],
        t.Ctx(partial=False, recurse=g.recurse),
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
        t.Ctx(partial=False, recurse=g.recurse),
    )
    t.compare_list(
        er[1],
        result[1],
        t.Ctx(partial=False, recurse=g.recurse),
    )
