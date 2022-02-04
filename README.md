# bdantic

<p align="center">
    <a href="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml">
        <img src="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml/badge.svg"/>
    </a>
    <a href="https://pypi.org/project/bdantic">
        <img src="https://img.shields.io/pypi/v/bdantic"/>
    </a>
</p>

> A package for extending [beancount][1] with [pydantic][2]

See the [docs](https://jmgilman.github.io/bdantic/) for more details.

## Installation

```shell
pip install bdantic
```

## Usage

### Parsing

A handful of functions are provided for parsing Beancount types, but the primary
method supports parsing most core types:

```python
import bdantic

from beancount.core import amount
from decimal import Decimal

amt = amount.Amount(number=Decimal(1.50), currency="USD"))
model = bdantic.parse(amt) # Produces a bdantic.models.Amount
```

### Exporting

All models can be directly exported back to their native Beancount types by
using their bult-in `export` method:

```python
amt_export = model.export()
assert amt == amt_export
```

### Ingesting

Functions are available for parsing common responses from interacting with the
Beancount package. You can parse an entire Beancount file with the following:

```python
import bdantic

from beancount import loader

# A bdantic.models.BeancountFile instance
bfile = bdantic.parse_loader(*loader.load_file("ledger.beancount"))
print(len(bfile.entries))
```

You can also parse the response from executing a query:

```python
import bdantic

from beancount import loader
from beancount.query import query

entries, _, options = loader.load_file("ledger.beancount")

query = "SELECT date, narration, account, position"
result = query.run_query(entries, options, query)
parsed_result = bdantic.parse_query(result)
```

Or the result of running a realization:

```python
import bdantic

from beancount.core import realization

entries, _, options = loader.load_file("ledger.beancount")

real = realization.realize(entries)
parsed_real = bdantic.parse(real)
```

### Rendering

Perhaps the most powerful usage of `bdantic` is rendering beancount data into a
more universal format like JSON. Since all models inherit from `Pydantic` they
include full support for rendering their contents as JSON:

```python
import bdantic

from beancount import loader

bfile = bdantic.parse_loader(*loader.load_file("ledger.beancount"))
js = bfile.json()
print(js) # Look ma, my beancount data in JSON!
```

The rendered JSON can be parsed back into the Beancount model that generated it:

```python
from bdantic.models import BeancountFile

bfile = BeancountFile.parse_raw(js)
```

In additiona to JSON, the directive models can be rendered as valid Beancount
syntax using the built-in `syntax` method:

```python
from bdantic.models import Amount, Posting, Transaction
from datetime import date
from decimal import Decimal

txn = Transaction(
    date=date.today(),
    meta={},
    flag="*",
    payee="Home Depot",
    narration="Tools n stuff",
    tags=None,
    links=None,
    postings=[
        Posting(
            account="Assets:Bank:Cash",
            units=Amount(number=Decimal(-142.32), currency="USD"),
            cost=None,
            CostSpec=None,
            flag=None,
            meta={},
        ),
        Posting(
            account="Expenses:HomeDepot",
            units=Amount(number=Decimal(142.32), currency="USD"),
            cost=None,
            CostSpec=None,
            flag=None,
            meta={},
        ),
    ],
)

print(txn.syntax())
```

## Testing

```shell
pytest .
```

Most tests make heavy use of [hypothesis][3] for generating test data to be
used in the tests. Hypothesis automatically keeps a cache to speed up subsequent
testing, however, the first time you run `pytest` you may experience longer than
normal run times.

Additionally, many tests pull from the `static.beancount` file found in the
testing folder. This was generated using the `bean-example` CLI tool and is used
to verify models with a realistic ledger.

## Contributing

Check out the [issues][4] for items needing attention or submit your own and
then:

1. [Fork the repo][5]
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

[1]: https://github.com/beancount/beancount
[2]: https://github.com/samuelcolvin/pydantic
[3]: https://hypothesis.readthedocs.io/en/latest/
[4]: https://github.com/jmgilman/bdantic/issues
[5]: https://github.com/jmgilman/bdantic/fork
