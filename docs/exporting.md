# Exporting

## Overview

All models (with the exception of the [Account][bdantic.models.realize.Account]
model) contain an [export][bdantic.models.base.Base.export] method which will
produce the equivalent Beancount type from the model. It's essentially reversing
what the [parse][bdantic.models.base.Base.parse] method does:

```python
import bdantic

from beancount.core import amount
from decimal import Decimal

amt = amount.Amount(number=Decimal(1.50), currency="USD"))

parsed_amt = bdantic.parse(amt)
exported_amt = parsed_amt.export()

assert amt == exported_amt
```

The model doesn't need to necessarily be derived from a beancount type in order
for it to be exported. This is a useful feature because it allows creating
Beancount types which are protected by the power of Pydantic validation models:

```python
from bdantic import models
from decimal import Decimal

# ValidationError: value is not a valid decimal (type=type_error.decimal)
amt = models.Amount(number=False, currency="USD").export()
```

## Helper Functions

In addition to the above method, an [export][bdantic.parse.export] function is
provided for exporting the given model. To export a list of models, use the
[export_all][bdantic.parse.export_all] function.
