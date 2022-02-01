from beancount.core import (
    amount,
    data,
)
from bdantic.models import common, data as mdata, directives
from datetime import date
from decimal import Decimal
from typing import NamedTuple


def test_filter_dict():
    d = {"test": "test", 1: 2, type(str): "str"}
    expected = {"test": "test", 1: 2}

    result = common.filter_dict(d)
    assert result == expected


def test_is_named_tuple():
    class Test(NamedTuple):
        pass

    assert common.is_named_tuple(Test())

    tup = ("test", "tuple")
    assert not common.is_named_tuple(tup)


def test_recursive_parse():
    txn = data.Transaction(
        meta={
            "filename": "test.beancount",
            "lineno": 123,
        },
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

    expected = {
        "meta": {
            "filename": "test.beancount",
            "lineno": 123,
        },
        "date": date.today(),
        "flag": "*",
        "payee": "test",
        "narration": "test",
        "tags": None,
        "links": None,
        "postings": [
            {
                "account": "Test",
                "units": {
                    "number": Decimal(1.50),
                    "currency": "USD",
                },
                "cost": None,
                "price": None,
                "flag": None,
                "meta": {},
            }
        ],
    }

    result = common.recursive_parse(txn)
    assert result == expected


def test_recursive_export():
    txn = directives.Transaction(
        meta={
            "filename": "test.beancount",
            "lineno": 123,
        },
        date=date.today(),
        flag="*",
        payee="test",
        narration="test",
        tags=None,
        links=None,
        postings=[
            directives.Posting(
                account="Test",
                units=mdata.Amount(number=Decimal(1.50), currency="USD"),
                cost=None,
                price=None,
                flag=None,
                meta={},
            )
        ],
    )

    expected = {
        "meta": {
            "filename": "test.beancount",
            "lineno": 123,
        },
        "date": date.today(),
        "flag": "*",
        "payee": "test",
        "narration": "test",
        "tags": None,
        "links": None,
        "postings": [
            data.Posting(
                account="Test",
                units=amount.Amount(number=Decimal(1.50), currency="USD"),
                cost=None,
                price=None,
                flag=None,
                meta={},
            )
        ],
    }

    result = common.recursive_export(txn)
    assert result == expected
