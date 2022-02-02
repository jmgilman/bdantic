import random

from beancount.core.amount import Amount
from beancount.core.data import Directive, Posting, Transaction
from dataclasses import dataclass
from decimal import Decimal
from hypothesis import strategies as s
from random_words import RandomWords  # type: ignore
from typing import Dict, List, Optional, Type


def register() -> None:
    """Registers common type strategies used in tests."""
    s.register_type_strategy(Amount, amount())
    s.register_type_strategy(Decimal, decimal())


@dataclass
class AccountGenerator:
    """A class for generating semi-realistic account structures.

    This class provides a single method, generate(), which will create a list
    of nested accounts. The final result is intended to look semi-realistic in
    the sense that account names use real words and typically have one or more
    subaccounts (except for the leaves). The class attributes can be modified
    in order to control how the structure is generated.

    Attributes:
        min_leaves: The minimum number of leaves to generate for each node
        max_leaves: The maximum number of leaves to generate for each node
        min_nodes: The minimum number of nodes to generate for each leaf
        max_nodes: The max number of nodes to generate for each leaf
    """

    min_leaves = 1
    max_leaves = 3
    min_nodes = 3
    max_nodes = 5
    rw = RandomWords()

    def generate(self) -> List[str]:
        """Generates a list of semi-realistic account names.

        Example:
        [
            "Inquiry:Bars",
            "Inquiry:Entrance",
            "Inquiry:Introduction",
            "Successes:Armament",
            "Successes:Rail:Flares",
            "Successes:Rail:Spindle",
            "Successes:Rail:Ones",
            "Successes:Presses",
            "Successes:Waste:Hugs",
            "Successes:Waste:Catcher",
            "Successes:Waste:Signs",
            "Beams:Failure",
            "Beams:Cylinder",
            "Beams:Kiss",
            "Beams:Diseases"
        ]
        """
        accounts: List[str] = []
        for segments in _walk_dict(self._make_tree()):
            accounts.append(":".join(segments))

        return accounts

    def _make_tree(self, depth=0):
        """Generates a nested tree structure using random words as keys."""
        if depth >= self.max_leaves:
            return None

        names = self._rand_words()
        d = dict.fromkeys(names)
        for name in names:
            d[name] = self._make_tree(depth + self._rand_leave())

        return d

    def _rand_leave(self) -> int:
        """Generates a random number of leaves to generate."""
        return random.randrange(self.min_leaves, self.max_leaves)

    def _rand_node(self) -> int:
        """Generates a random number of nodes to generate."""
        return random.randrange(self.min_nodes, self.max_nodes)

    def _rand_words(self) -> List[str]:
        """Generates a random number of words as configured by the class."""
        return [
            w.capitalize()
            for w in self.rw.random_words(count=self._rand_node())
        ]


def amount(currency="USD") -> s.SearchStrategy[Amount]:
    """Generates a random Amount using the specified currency.

    Args:
        currency: The currency to use for the amount

    Returns:
        A new search strategy
    """
    return s.builds(
        Amount,
        currency=s.just(currency),
        number=decimal(),
    )


def decimal() -> s.SearchStrategy[Decimal]:
    """Generates a random decimal value.

    Returns:
        A new search strategy
    """
    return s.decimals(
        min_value=1, max_value=100, allow_infinity=False, allow_nan=False
    )


def directive(ty: Type[Directive]) -> s.SearchStrategy[Directive]:
    """Generates the given directive type.

    Args:
        ty: The type of directive to generate

    Returns:
        A new instance of the generated directive
    """
    return s.builds(ty, meta=meta())


def meta() -> s.SearchStrategy[Dict[str, str]]:
    """Generates metadata for directives.

    Returns:
        A new search strategy
    """
    return s.dictionaries(word(), words(), max_size=2)


@s.composite
def transaction(
    draw: s.DrawFn,
    accts: List[str],
    currency="USD",
    postings_min=2,
    postings_max=5,
) -> Transaction:
    """Generates a random transaction.

    The generated transaction will contain a random number of postings that may
    not have unique amounts but will always sum to zero. The accounts used in
    each posting will be unique and will be randomly pulled from the given list
    of account names.

    Args:
        accts: A list of account names to pull from for generating postings
        currency: The currency to use in postings
        postings_min: The minimum number of postings to generate
        postings_max: The maximum number of postings to generate

    Returns:
        A new search strategy
    """
    postings = []

    numbers = draw(
        s.lists(
            s.decimals(
                min_value=-50,
                max_value=50,
                allow_infinity=False,
                allow_nan=False,
            ).filter(lambda n: n > 1 or n < -1),
            min_size=postings_min,
            max_size=postings_max,
        )
    )

    numbers.append(Decimal(-sum(numbers)))
    assert sum(numbers) == 0

    amts = [Amount(number=n, currency=currency) for n in numbers]
    used_accounts = []
    for amt in amts:
        account = draw(
            s.sampled_from(accts).filter(lambda a: a not in used_accounts)
        )
        used_accounts.append(account)

        postings.append(
            Posting(
                account=account,
                units=amt,
                cost=None,
                price=None,
                flag=None,
                meta=None,
            )
        )

    txn = Transaction(
        meta=draw(meta()),
        date=draw(s.dates()),
        flag="*",
        payee=None,
        narration=draw(words()),
        tags=None,
        links=None,
        postings=postings,
    )

    return txn


@s.composite
def transactions(draw: s.DrawFn, min=3, max=5) -> List[Transaction]:
    """Generates a list of transactions.

    Args:
        min: The minimum number to generate
        max: The maximum number to generate

    Returns:
        A new search strategy
    """
    ag = AccountGenerator()
    accts = ag.generate()
    return draw(s.lists(transaction(accts=accts), min_size=min, max_size=max))


@s.composite
def word(_) -> str:
    """Generates a random word.

    Returns:
        A new strategy
    """
    rw = RandomWords()
    return rw.random_word()


@s.composite
def words(draw: s.DrawFn, min=3, max=5):
    """Generates a string of random words.

    Args:
        min: The minimum number of words to generate
        max: The maximum number of words to generate

    Returns:
        A new strategy
    """
    return " ".join(draw(s.lists(word(), min_size=min, max_size=max)))


def _walk_dict(d: Dict, pre: Optional[List] = None):
    """Walks the keys of the given dictionary, returning leaves as lists.

    This function will recursively walk a nested dictionary and generate a list
    of keys for all leaves contained within the nested structure. The given
    structure should only contain nested dictionaries and leaf values are
    discarded as this function is only concerned with dictionary keys.

    Args:
        d: The dictionary to walk
        pre: Used in recursion

    Yields:
        Lists for each leaf contained within the structure.

        For example:

            {
                "one":{
                    "two":{
                        "three": None
                    }
                },
                "four":{
                    "five":{
                        "six": None
                    }
                }
            }

        Would yield:

            ['one', 'two', 'three']
            ['four', 'five', 'six']
    """
    pre = pre[:] if pre else []
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                for d in _walk_dict(value, pre + [key]):
                    yield d
            else:
                yield pre + [key]
    else:
        yield pre + [d]
