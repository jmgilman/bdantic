from beancount.core import amount, data
from bdantic import parse, parse_all, parse_entries, models
from datetime import date
from decimal import Decimal


def test_parse():
    txn = data.Transaction(
        meta={},
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

    expected = models.Transaction(
        meta={},
        date=date.today(),
        flag="*",
        payee="test",
        narration="test",
        tags=None,
        links=None,
        postings=[
            models.Posting(
                account="Test",
                units=models.Amount(number=Decimal(1.50), currency="USD"),
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
            meta={},
            date=date.today(),
            account="Test",
            amount=amount.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )

    expected_models.append(models.Amount(number=Decimal(1.50), currency="USD"))
    expected_models.append(
        models.Balance(
            meta={},
            date=date.today(),
            account="Test",
            amount=models.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )

    result = parse_all(btypes)
    assert result == expected_models


def test_parse_entries():
    btypes = []
    expected_models = []

    btypes.append(
        data.Balance(
            meta={},
            date=date.today(),
            account="Test",
            amount=amount.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    btypes.append(data.Close(meta={}, date=date.today(), account="Test"))
    btypes.append(data.Commodity(meta={}, date=date.today(), currency="USD"))

    expected_models.append(
        models.Balance(
            meta={},
            date=date.today(),
            account="Test",
            amount=models.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    expected_models.append(
        models.Close(meta={}, date=date.today(), account="Test")
    )
    expected_models.append(
        models.Commodity(meta={}, date=date.today(), currency="USD")
    )
    expected_directives = models.Directives(__root__=expected_models)

    result = parse_entries(btypes)
    assert result == expected_directives
