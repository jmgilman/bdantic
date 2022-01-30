import collections

from beancount.core import (
    amount,
    data,
    display_context,
    distribution,
    inventory,
    position,
)
from bdantic import models
from datetime import date
from decimal import Decimal
from testing.util import is_equal
from typing import NamedTuple


def test_all():
    test_btypes = []
    test_models = []

    dd = collections.defaultdict(int)
    dd[2] = 2941
    dd[0] = 13
    dist = distribution.Distribution()
    dist.hist = dd

    cc = display_context._CurrencyContext()
    cc.has_sign = False
    cc.integer_max = 1
    cc.fractional_dist = dist

    dc = display_context.DisplayContext()
    dc.commas = False
    dc.ccontexts = collections.defaultdict(display_context._CurrencyContext)
    dc.ccontexts["USD"] = cc

    test_btypes.append(amount.Amount(number=Decimal(1.50), currency="USD"))
    test_btypes.append(
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
    test_btypes.append(
        data.Close(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
        )
    )
    test_btypes.append(
        data.Commodity(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            currency="USD",
        )
    )
    test_btypes.append(
        position.Cost(
            number=Decimal(1.50), currency="USD", date=date.today(), label=None
        )
    )
    test_btypes.append(
        position.CostSpec(
            number_per=None,
            number_total=None,
            currency=None,
            date=None,
            label=None,
            merge=None,
        )
    )
    test_btypes.append(cc)
    test_btypes.append(
        data.Custom(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            type="Test",
            values=[],
        )
    )
    test_btypes.append(dc)
    test_btypes.append(dist)
    test_btypes.append(
        data.Document(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
            filename="test.zip",
            tags=None,
            links=None,
        )
    )
    test_btypes.append(
        data.Event(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            type="test",
            description="test",
        )
    )
    test_btypes.append(
        inventory.Inventory(
            positions=[
                position.Position(
                    units=amount.Amount(number=Decimal(1.50), currency="USD"),
                    cost=None,
                )
            ]
        )
    )
    test_btypes.append(
        data.Note(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
            comment="test",
        )
    )
    test_btypes.append(
        data.Open(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
            currencies=[],
            booking=None,
        )
    )
    test_btypes.append(
        data.Pad(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            account="Test",
            source_account="Test",
        )
    )
    test_btypes.append(
        position.Position(
            units=amount.Amount(number=Decimal(1.50), currency="USD"),
            cost=None,
        )
    )
    test_btypes.append(
        data.Posting(
            account="Test",
            units=amount.Amount(number=Decimal(1.50), currency="USD"),
            cost=None,
            price=None,
            flag=None,
            meta=None,
        )
    )
    test_btypes.append(
        data.Price(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            currency="USD",
            amount=amount.Amount(number=Decimal(1.50), currency="USD"),
        )
    )
    test_btypes.append(
        data.Query(
            meta={
                "filename": "test.beancount",
                "lineno": 123,
            },
            date=date.today(),
            name="test",
            query_string="test",
        )
    )
    test_btypes.append(
        data.Transaction(
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
    )
    test_btypes.append(
        data.TxnPosting(
            txn=data.Transaction(
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
                        units=amount.Amount(
                            number=Decimal(1.50), currency="USD"
                        ),
                        cost=None,
                        price=None,
                        flag=None,
                        meta={},
                    )
                ],
            ),
            posting=data.Posting(
                account="Test",
                units=amount.Amount(number=Decimal(1.50), currency="USD"),
                cost=None,
                price=None,
                flag=None,
                meta=None,
            ),
        )
    )

    test_models.append(models.Amount(number=Decimal(1.50), currency="USD"))
    test_models.append(
        models.Balance(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            account="Test",
            amount=models.Amount(number=Decimal(1.50), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    test_models.append(
        models.Close(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            account="Test",
        )
    )
    test_models.append(
        models.Commodity(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            currency="USD",
        )
    )
    test_models.append(
        models.Cost(
            number=Decimal(1.50), currency="USD", date=date.today(), label=None
        )
    )
    test_models.append(
        models.CostSpec(
            number_per=None,
            number_total=None,
            currency=None,
            date=None,
            label=None,
            merge=None,
        )
    )
    test_models.append(
        models.CurrencyContext(
            has_sign=False,
            integer_max=1,
            fractional_dist=models.Distribution(hist=dd),
        )
    )
    test_models.append(
        models.Custom(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            type="Test",
            values=[],
        )
    )
    mcc = collections.defaultdict(models.CurrencyContext)
    mcc["USD"] = models.CurrencyContext(
        has_sign=False,
        integer_max=1,
        fractional_dist=models.Distribution(hist=dd),
    )
    test_models.append(models.DisplayContext(commas=False, ccontexts=mcc))
    test_models.append(models.Distribution(hist=dd))
    test_models.append(
        models.Document(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            account="Test",
            filename="test.zip",
            tags=None,
            links=None,
        )
    )
    test_models.append(
        models.Event(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            type="test",
            description="test",
        )
    )
    test_models.append(
        models.Inventory(
            __root__=[
                models.Position(
                    units=models.Amount(number=Decimal(1.50), currency="USD"),
                    cost=None,
                )
            ]
        )
    )
    test_models.append(
        models.Note(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            account="Test",
            comment="test",
        )
    )
    test_models.append(
        models.Open(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            account="Test",
            currencies=[],
            booking=None,
        )
    )
    test_models.append(
        models.Pad(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            account="Test",
            source_account="Test",
        )
    )
    test_models.append(
        models.Position(
            units=models.Amount(number=Decimal(1.50), currency="USD"),
            cost=None,
        )
    )
    test_models.append(
        models.Posting(
            account="Test",
            units=models.Amount(number=Decimal(1.50), currency="USD"),
            cost=None,
            price=None,
            flag=None,
            meta=None,
        )
    )
    test_models.append(
        models.Price(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            currency="USD",
            amount=models.Amount(number=Decimal(1.50), currency="USD"),
        )
    )
    test_models.append(
        models.Query(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
            date=date.today(),
            name="test",
            query_string="test",
        )
    )
    test_models.append(
        models.Transaction(
            meta=models.Meta(
                filename="test.beancount",
                lineno=123,
            ),
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
    )
    test_models.append(
        models.TxnPosting(
            txn=models.Transaction(
                meta=models.Meta(
                    filename="test.beancount",
                    lineno=123,
                ),
                date=date.today(),
                flag="*",
                payee="test",
                narration="test",
                tags=None,
                links=None,
                postings=[
                    models.Posting(
                        account="Test",
                        units=models.Amount(
                            number=Decimal(1.50), currency="USD"
                        ),
                        cost=None,
                        price=None,
                        flag=None,
                        meta={},
                    )
                ],
            ),
            posting=models.Posting(
                account="Test",
                units=models.Amount(number=Decimal(1.50), currency="USD"),
                cost=None,
                price=None,
                flag=None,
                meta=None,
            ),
        )
    )

    for btype, model in zip(test_btypes, test_models):
        result_model = type(model).parse(btype)
        assert is_equal(result_model, model)

        result_btype = model.export()
        assert is_equal(result_btype, btype)


def test_filter_dict():
    d = {"test": "test", 1: 2, type(str): "str"}
    expected = {"test": "test", 1: 2}

    result = models._filter_dict(d)
    assert result == expected


def test_is_named_tuple():
    class Test(NamedTuple):
        pass

    assert models._is_named_tuple(Test())

    tup = ("test", "tuple")
    assert not models._is_named_tuple(tup)


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

    result = models._recursive_parse(txn)
    assert result == expected


def test_recursive_export():
    txn = models.Transaction(
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

    result = models._recursive_export(txn)
    assert result == expected
