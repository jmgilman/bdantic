# Filtering

## Overview

All models support mutation using [JMESPath](https://jmespath.org/) expressions.

## Select

The [select][bdantic.models.base.Base.select] method allows selecting subsets of
data from within a model:

```python
from beancount import loader
from bdantic import parse_loader

entries, errors, options = loader.load_file("ledger.beancount")
result = parse_loader(entries, errors, options)

print(result.entries[0].select("postings[].units"))
```

The result is dependent on the selection expression and will be in the form of
one or more nested dictionaries/lists. In other words, the original models will
be in `dict` form, however, they can be converted back like so:

```python
from bdantic.models import Amount

amounts = result.entries[0].select("postings[].units")
amounts = [Amount.parse_obj(a) for a in amounts]
```

## Filter

For models which wraps lists, the [filter][bdantic.models.base.BaseFiltered.filter]
method can be used for filtering the list down:

```python
from beancount import loader
from bdantic import parse_loader

entries, errors, options = loader.load_file("ledger.beancount")
result = parse_loader(entries, errors, options)

txns = result.entries.filter("[?ty == 'Transaction']")
```

Unlike the [select][bdantic.models.base.Base.select] method, filtering will
attempt to preserve the formats of models. This is important to note because if
the expression mutates the models in such a way that validation fails then an
exception will be raised.
