from beancount import loader
from beancount.core import amount, data
from bdantic import parse, parse_all, parse_entries, parse_loader, models
from datetime import date
from decimal import Decimal
from testing.util import is_equal


def test_parse():
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

    expected = models.Transaction(
        meta=models.Meta(filename="test.beancount", lineno=123),
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
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
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
            meta=models.Meta(filename="test.beancount", lineno=123),
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
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
            amount=amount.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    btypes.append(
        data.Close(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
        )
    )
    btypes.append(
        data.Commodity(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            currency="USD",
        )
    )

    expected_models.append(
        models.Balance(
            meta=models.Meta(filename="test.beancount", lineno=123),
            date=date.today(),
            account="Test",
            amount=models.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    expected_models.append(
        models.Close(
            meta=models.Meta(filename="test.beancount", lineno=123),
            date=date.today(),
            account="Test",
        )
    )
    expected_models.append(
        models.Commodity(
            meta=models.Meta(filename="test.beancount", lineno=123),
            date=date.today(),
            currency="USD",
        )
    )
    expected_entries = models.Entries(__root__=expected_models)

    result = parse_entries(btypes)
    assert result == expected_entries


def test_parse_loader():
    entries, errors, options = loader.load_file("testing/static.beancount")
    parsed = parse_loader(entries, errors, options)

    def compare(object1, object2):
        for expected, result in zip(object1, object2):
            if type(expected) in models.type_map.keys():
                if not is_equal(expected, result):
                    print(expected)
                    print(result)
                assert is_equal(expected, result)
            else:
                if expected and result:
                    assert expected == result

    # Entries
    compare(entries, parsed.entries.export())

    # Options
    compare(options.values(), parsed.options.export().values())
    assert options.keys() == parsed.options.export().keys()

    # Errors
    assert errors == parsed.errors
