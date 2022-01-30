# beancount-stubs

<p align="center">
    <a href="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml">
        <img src="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml/badge.svg"/>
    </a>
    <a href="https://pypi.org/project/bdantic">
        <img src="https://img.shields.io/pypi/v/bdantic"/>
    </a>
</p>

> A package for extending [beancount][1] with [pydantic][2]

## Install

```shell
$> pip install bdantic
```

## Usage

The package includes compatible models for all of the core beancount data types.
Models are created by converting a beancount type into its respective model:

```python
from beancount.core import amount
from bdantic import parse
from decimal import Decimal

amt = amount.Amount(number=Decimal(1.50), currency="USD"))
model = parse(amt) # Produces a bdantic.models.Amount
```

All models can be exported back into their original beancount data type:

```python
amt_export = model.export()
assert amt == amt_export # The exported object is identical to the original
```

Since all models are Pydantic base models, it's possible to export the entire
result of parsing a beancount file into JSON:

```python
from beancount import loader
from bdantic import parse_loader

result = parse_loader(*loader.load_file("testing/static.beancount"))

print(result.json())
```

Note that models are not compatible with beancount functions as most functions
make heavy use of type checking and will fail when passed a model. It's expected
to do all processing using the beancount package and then convert the types to
models when needed. Additionally, while JSON can be generated, it's not
guaranteed to go both ways due to limitations with Pydantic.

## Contributing

Check out the [issues][3] for items needing attention or submit your own and
then:

1. [Fork the repo][4]
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

[1]: https://github.com/beancount/beancount
[2]: https://github.com/samuelcolvin/pydantic
[3]: https://github.com/jmgilman/bdantic/issues
[4]: https://github.com/jmgilman/bdantic/fork