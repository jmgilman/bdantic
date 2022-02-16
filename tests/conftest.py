import hashlib
import pickle
import pytest
import datetime
import random
import io
import os
from beancount.scripts import example  # type: ignore

from beancount.core import data, distribution
from beancount import loader
from bdantic import models, types
from bdantic.models import base
from pydantic import BaseModel
from typing import Any, List, Type


class Ctx(BaseModel):
    """Holds contextual information when comparing values.

    Attributes:
        partial: The type of comparison to perform
        recurse: The types of objects to recursively compare
    """

    recurse: List[Type] = [
        models.Amount,
        models.Close,
        models.Cost,
        models.CostSpec,
        models.CurrencyContext,
        models.DisplayContext,
        distribution.Distribution,
        models.Distribution,
        base.Meta,
        models.Open,
        models.Posting,
        models.Position,
        models.Transaction,
        models.TxnPosting,
    ]

    def is_recurse(self, obj1: Any, obj2: Any) -> bool:
        """Returns whether or not the two objects should be recursed.

        Args:
            obj1: An object to check
            obj2: An object to check

        Returns:
            True if the objects should be recursed, False otherwise
        """
        return type(obj1) in self.recurse or type(obj2) in self.recurse

    def compare(self, obj1: Any, obj2: Any, partial: bool = True) -> None:
        """Compares two objects by asserting equality.

        The type of comparison performed is dependent on the types of the
        passed objects and information contained within the context. Objects
        that are recursible will have their attributes compared, dictionaries
        and lists will be iterated over to find recursible objects and
        keys/values will be asserted to be equal, all other types will be
        asserted to be equal to each other.

        Args:
            obj1: The first object to compare
            obj2: The second object to compare
            partial: If True, allows objects to have different attributes.

        Raises:
            AssertionError when an equality check fails
        """
        if hasattr(obj1, "__root__"):
            obj1 = obj1.__root__
        elif hasattr(obj2, "__root__"):
            obj2 = obj2.__root__

        if self.is_recurse(obj1, obj2):
            self.compare_object(obj1, obj2, partial)
        elif isinstance(obj1, dict) and isinstance(obj2, dict):
            self.compare_dict(obj1, obj2)
        elif isinstance(obj1, list) and isinstance(obj2, list):
            self.compare_list(obj1, obj2)
        elif isinstance(obj1, tuple) and isinstance(obj2, tuple):
            self.compare_list(obj1, obj2)
        else:
            assert obj1 == obj2

    def compare_dict(self, dict1, dict2, partial: bool = True) -> None:
        """Compares two dictionaries, asserting they are equal.

        Args:
            dict1: The first dictionary to compare
            dict2: The second dictionary to compare
            partial: If True, allows objects to have different attributes.

        Raises:
            AssertionError when an equality check fails
        """
        assert not set(dict1.keys()).difference(set(dict2.keys()))
        for key in dict1:
            self.compare(dict1[key], dict2[key], partial)

    def compare_list(self, list1, list2, partial: bool = True) -> None:
        """Compares two lists, asserting they are equal.

        Args:
            list1: The first list to compare
            list2: The second list to compare
            partial: If True, allows objects to have different attributes.

        Raises:
            AssertionError when an equality check fails
        """
        assert len(list1) == len(list2)
        for i in range(len(list1)):
            self.compare(list1[i], list2[i], partial)

    def compare_object(
        self, obj1: Any, obj2: Any, partial: bool = True
    ) -> None:
        """Compares two objects, asserting they are equal.

        Objects are compared by iterating over their attributes and asserting
        equality. If the context is set to partial, only attributes which the
        two objects share will be asserted equal. Attributes which are lists or
        dictionaries will be recursively checked. Nested objects are only
        recursed if their types are found in the recurse attribute of the given
        context.

        Args:
            obj1: The first object to compare
            obj2: The second object to compare
            partial: If True, allows objects to have different attributes.

        Raises:
            AssertionError when an equality check fails
        """

        def is_valid_attr(k: str, obj: Any) -> bool:
            if k.startswith("__"):
                return False
            elif callable(getattr(obj, k)):
                return False
            return True

        attr1 = set([attr for attr in dir(obj1) if is_valid_attr(attr, obj1)])
        attr2 = set([attr for attr in dir(obj2) if is_valid_attr(attr, obj2)])

        if not partial:
            assert not attr1.difference(
                attr2
            ), "Objects have dissimilar attributes"
            attrs = attr1
        else:
            attrs = attr1.intersection(attr2)

        for attr in attrs:
            val1 = getattr(obj1, attr)
            val2 = getattr(obj2, attr)

            self.compare(val1, val2, partial)


@pytest.fixture(scope="session")
def ctx() -> Ctx:
    return Ctx()


@pytest.fixture(scope="session")
def beanfile() -> tuple[list[data.Directive], list, dict[str, Any]]:
    end = datetime.date.today()

    start_offset = random.randrange(2, 10)
    start_month = random.randrange(1, 12)
    start_day = random.randrange(1, 28)
    start = datetime.date(end.year - start_offset, start_month, start_day)

    birth_offset = random.randrange(20, 40)
    birth_month = random.randrange(1, 12)
    birth_day = random.randrange(1, 28)
    birth = datetime.date(end.year - birth_offset, birth_month, birth_day)

    with io.StringIO() as s:
        example.write_example_file(birth, start, end, True, s)
        s.seek(0)
        return loader.load_string(s.read())


@pytest.fixture(scope="session")
def syntax() -> list[tuple[str, type[types.ModelDirective]]]:
    balance = "2022-01-01 balance Assets:US:BofA:Checking        2845.77 USD"
    close = "2022-01-01 close Equity:Opening-Balances"
    commodity = """2022-01-01 commodity USD
    export: "CASH"
    name: "US Dollar" """
    document = f"""
    2022-01-01 document Assets:US:Vanguard:Cash "{os.getcwd()}/test.doc" """
    event = """2022-01-01 event "location" "Paris, France" """
    note = """2022-01-01 note Liabilities:Credit "Called about fraudulence" """
    open = """2022-01-01 open Liabilities:Credit:CapitalOne     USD"""
    pad = "2022-01-01 pad Assets:BofA:Checking Equity:Opening-Balances"
    price = "2022-01-01 price HOOL  579.18 USD"
    query = """2022-01-01 query "france-balances" "
    SELECT account, sum(position) WHERE `trip-france-2014` in tags" """
    transaction = """2022-01-01 * "Investing 40% of cash in VBMPX"
    Assets:US:Vanguard:VBMPX    1.122 VBMPX {213.90 USD, 2022-01-01}
    Assets:US:Vanguard:Cash   -240.00 USD"""

    return [
        (balance, models.Balance),
        (close, models.Close),
        (commodity, models.Commodity),
        (document, models.Document),
        (event, models.Event),
        (note, models.Note),
        (open, models.Open),
        (pad, models.Pad),
        (price, models.Price),
        (query, models.Query),
        (transaction, models.Transaction),
    ]


def hash(obj) -> str:
    """Hashes the given object.

    Args:
        obj: The object to hash.

    Returns:
        An MD5 hash of the object.
    """
    return hashlib.md5(pickle.dumps(obj)).hexdigest()
