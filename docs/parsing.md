# Parsing

## Overview

Parsing is the main method by which Beancount types can be converted in their
respective Pydantic models. Every model provided by `bdantic` includes a
[parse][bdantic.models.base.Base.parse] method which is responsible for parsing
its associated Beancount type into a new instance of the model.

```python
import bdantic

from beancount.core import amount
from decimal import Decimal

amt = amount.Amount(number=Decimal(1.50), currency="USD"))
model = bdantic.parse(amt) # Produces a bdantic.models.Amount
```

In most cases, the model will match the native beancount type field-for-field.
In some cases the underlying Beancount data combines multiple types, like the
`realization.RealAccount` class which is both a dictionary of child accounts as
well as a container for individual account information. In cases like these the
model may differ slightly (i.e. the
[RealAccount][bdantic.models.realize.RealAccount] model uses a `children` field
for holding child accounts), however, models will always convert back to their
native Beancount types without issue.

When a Beancount type contains child elements which can be represented as a
model the [parse][bdantic.models.base.Base.parse] method will recursively
convert child elements to models as well. For example, parsing a
[Transaction][bdantic.models.directives.Transaction] will also parse all child
[postings][bdantic.models.directives.Posting] as well as all child
[amounts][bdantic.models.data.Amount] of those postings.

Not every Beancount type has an equivalent model. To see the currently suported
types, refer to the type signature of the [parse][bdantic.parse.parse] function.

## Parsing Beancount Types

### Parsing Files

The [parse_loader][bdantic.parse.parse_loader] function provides a convenient
interface for parsing the results of the `beancount.loader` functions. For
example, one can convert all entries loaded from a Beancount file to their
respective models like so:

```python
import bdantic

from beancount import loader

bfile = bdantic.parse_loader(*loader.load_file("ledger.beancount"))
```

The [BeancountFile][bdantic.models.file.BeancountFile] model provides access to
the parsed entries, errors, and options returned by the loader.

### Parsing Query Results

The [parse_query][bdantic.parse.parse_query] function provides an interface for
parsing the results of running a Beancount query:

```python
import bdantic

from beancount import loader
from beancount.query import query

entries, _, options = loader.load_file("ledger.beancount")

query = "SELECT date, narration, account, position"
result = query.run_query(entries, options, query)
parsed_result = bdantic.parse_query(result)
```

The [QueryResult][bdantic.models.query.QueryResult] returned contains the column
and row data with all Beancount types automatically parsed into models.

### Parsing Realizations

The `realization.realize` Beancount function takes a list of entries and uses
them to calculate data about the accounts included in those entries. It returns
a `realization.RealAccount` which is a `dict` like object that contains the
entire account hierarchy. This object can be parsed:

```python
import bdantic

from beancount.core import realization

entries, _, options = loader.load_file("ledger.beancount")

real = realization.realize(entries)
parsed_real = bdantic.parse(real)
```

An additional [Account][bdantic.models.realize.Account] model is provided and
can be obtained by parsing it directly from a `realization.RealAccount` or
calling the [to_account][bdantic.models.realize.RealAccount.to_account] method
on a [RealAccount][bdantic.models.realize.RealAccount]. This model offers a
simplified view of a single account and is thus easier to render.

## Internal

Internally, parsing is accomplished by abusing the fact that most objects have a
`__dict__` property and all `NamedTuple` objects have a `_asdict()` method.
Since Beancount makes heavy use of `NamedTuple` objects this fact is used by the
[recursive_parse][bdantic.models.base.recursive_parse] function to recursively
create a dictionary representation of any complex Beancount type. Pydantic
models have a
[parse_obj](https://pydantic-docs.helpmanual.io/usage/models/#helper-functions)
method which takes in a dictionary and performs validation, producing a model if
all validation checks pass. The nested dictionary produced is fed into this
method to create the models.
