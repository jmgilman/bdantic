# Rendering

## Overview

Since all models inherit from Pydantic they gain access to
[useful methods](https://pydantic-docs.helpmanual.io/usage/exporting_models/)
for rendering the contained data in different formats. Namely, the ability
to generate JSON:

```python
import bdantic

from beancount import loader

bfile = bdantic.parse_loader(*loader.load_file("ledger.beancount"))
js = bfile.json()
print(js) # Look ma, my beancount data in JSON!
```

This allows, for example, processing some Beancount data and then exporting it
to another language or tool which can ingest JSON. The resulting JSON can be
parsed back into a model:

```python
from bdantic.models import BeancountFile

bfile = BeancountFile.parse_raw(js)
```

This behavior allows one to write or generate Beancount constructs in JSON and
then parse them back into their native types in Python.

## Syntax

In addition to the support provided by Pydantic, directive models also provide
a useful method for generating raw Beancount syntax:

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

Combined with the above, it's possible to go all the way from JSON to valid
Beancount syntax with the use of `bdantic`.
