from beancount.core import (
    amount,
    data,
)
from bdantic.models import base, data as mdata, directives
from datetime import date
from decimal import Decimal


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

    result = base.recursive_parse(txn)
    assert result == expected


def test_recursive_export():
    txn = directives.Transaction(
        id="",
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

    result = base.recursive_export(txn, base._IGNORE_FIELDS)
    assert result == expected
