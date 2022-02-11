from beancount import loader
from beancount.core import amount, data
from bdantic import (
    parse,
    parse_all,
    parse_directives,
    parse_loader,
    parse_query,
    types,
)
from bdantic import models
from datetime import date
from decimal import Decimal
from testing import common as t
from unittest.mock import patch, Mock


def test_parse():
    txn = data.Transaction(
        meta=None,
        date=date.today(),
        flag="*",
        payee="test",
        narration="test",
        tags=None,
        links=None,
        postings=[
            data.Posting(
                account="Test",
                units=amount.Amount(number=Decimal(1.50), currency="USD"),
                cost=None,
                price=None,
                flag=None,
                meta={},
            )
        ],
    )

    expected = models.directives.Transaction(
        date=date.today(),
        flag="*",
        payee="test",
        narration="test",
        tags=None,
        links=None,
        postings=[
            models.directives.Posting(
                account="Test",
                units=models.data.Amount(number=Decimal(1.50), currency="USD"),
                cost=None,
                price=None,
                flag=None,
                meta={},
            )
        ],
    )

    result = parse(txn)
    assert result == expected


def test_parse_all():
    btypes = []
    expected_models = []

    btypes.append(amount.Amount(number=Decimal(1.50), currency="USD"))
    btypes.append(
        data.Balance(
            meta=None,
            date=date.today(),
            account="Test",
            amount=amount.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )

    expected_models.append(
        models.data.Amount(number=Decimal(1.50), currency="USD")
    )
    expected_models.append(
        models.directives.Balance(
            meta=None,
            date=date.today(),
            account="Test",
            amount=models.data.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )

    result = parse_all(btypes)
    assert result == expected_models


def test_parse_directives():
    btypes = []
    expected_models = []

    btypes.append(
        data.Balance(
            meta=None,
            date=date.today(),
            account="Test",
            amount=amount.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    btypes.append(
        data.Open(
            meta=None,
            date=date.today(),
            account="Test",
            currencies=["USD"],
            booking=None,
        )
    )
    btypes.append(
        data.Commodity(
            meta=None,
            date=date.today(),
            currency="USD",
        )
    )

    expected_models.append(
        models.directives.Balance(
            date=date.today(),
            account="Test",
            amount=models.data.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    expected_models.append(
        models.directives.Open(
            date=date.today(),
            account="Test",
            currencies=["USD"],
        )
    )
    expected_models.append(
        models.directives.Commodity(
            date=date.today(),
            currency="USD",
        )
    )
    expected_directives = models.file.Directives(__root__=expected_models)

    result = parse_directives(btypes)
    assert result == expected_directives


def test_parse_loader():
    entries, errors, options = loader.load_file("testing/static.beancount")
    # import pprint

    # pprint.pprint(options)
    parsed = parse_loader(entries, errors, options)
    # print(parsed.options.export())

    def compare(object1, object2):
        for expected, result in zip(object1, object2):
            if type(expected) in types.type_map.keys():
                t.compare_object(expected, result, t.Ctx())
            else:
                if expected and result:
                    assert expected == result

    # Entries
    compare(entries, parsed.entries.export())

    # Options
    expected = options
    del expected["dcontext"]

    result = parsed.options.export()
    del result["dcontext"]

    t.compare_dict(expected, result, t.Ctx())

    # Errors
    assert errors == parsed.errors

    # Verify ID's are unique
    ids = [e.id for e in parsed.entries]
    assert len(ids) == len(set(ids))


@patch("bdantic.models.QueryResult.parse")
def test_parse_query(p):
    m = Mock()
    parse_query(m)
    p.assert_called_once_with(m)
