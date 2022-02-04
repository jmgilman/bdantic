# Introduction

The `bdantic` Python package provides an interface between [Beancount][1] and
[Pydantic][2]. It accomplishes this by providing models which can be parsed
directly from native Beancount types. In addition to this, all models can be
exported back into their native Beancount types for full compatibility.

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

Alternatively, you can call the `parse` method on the model directly:

```python
from bdantic.models import Amount
from beancount.core import amount
from decimal import Decimal

amt = amount.Amount(number=Decimal(1.50), currency="USD"))
model = Amount.parse(amt)
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

## Advanced

For more documentation, see the navigation sections to the left.

[1]: https://beancount.github.io/docs/index.html
[2]: https://pydantic-docs.helpmanual.io/
