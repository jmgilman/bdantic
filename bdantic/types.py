from __future__ import annotations

from beancount.core import (
    amount,
    data,
    display_context,
    distribution,
    inventory,
    position,
)
from .models.data import (
    Amount,
    Cost,
    CostSpec,
    Inventory,
    Position,
)
from .models.directives import (
    Balance,
    Close,
    Commodity,
    Custom,
    Document,
    Event,
    Note,
    Open,
    Pad,
    Posting,
    Price,
    Query,
    Transaction,
    TxnPosting,
)
from .models.display import CurrencyContext, DisplayContext, Distribution
from decimal import Decimal
from typing import Dict, List, Type, Union


# A dictionary mapping Beancount types to their respective models
type_map: Dict[Type[BeancountType], Type[Model]] = {
    amount.Amount: Amount,
    data.Balance: Balance,
    data.Close: Close,
    data.Commodity: Commodity,
    position.Cost: Cost,
    position.CostSpec: CostSpec,
    display_context._CurrencyContext: CurrencyContext,
    data.Custom: Custom,
    display_context.DisplayContext: DisplayContext,
    distribution.Distribution: Distribution,
    data.Document: Document,
    data.Event: Event,
    data.Note: Note,
    data.Open: Open,
    data.Pad: Pad,
    position.Position: Position,
    data.Posting: Posting,
    data.Price: Price,
    data.Query: Query,
    data.Transaction: Transaction,
    data.TxnPosting: TxnPosting,
    inventory.Inventory: Inventory,
}

# A union for all models that are directives
ModelDirective = Union[
    Balance,
    Close,
    Commodity,
    Custom,
    Document,
    Event,
    Note,
    Open,
    Pad,
    Price,
    Query,
    Transaction,
]

# A union for all models which have Beancount types that are NamedTuple's
ModelTuple = Union[
    ModelDirective,
    Amount,
    Cost,
    CostSpec,
    Position,
    Posting,
    TxnPosting,
]

# A union for all models
Model = Union[
    ModelTuple, CurrencyContext, DisplayContext, Distribution, Inventory
]

# A union for all Beancount types which are NamedTuple's
BeancountTuple = Union[
    amount.Amount,
    data.Balance,
    data.Close,
    data.Open,
    position.Cost,
    position.CostSpec,
    data.Commodity,
    data.Custom,
    data.Document,
    data.Event,
    data.Note,
    data.Open,
    data.Pad,
    position.Position,
    data.Posting,
    data.Price,
    data.Query,
    data.Transaction,
    data.TxnPosting,
]

# A union for all Beancount types
BeancountType = Union[
    BeancountTuple,
    display_context._CurrencyContext,
    display_context.DisplayContext,
    distribution.Distribution,
    inventory.Inventory,
]

# Valid types for keys in the meta field
MetaKeys = Union[str, int, float, bool, None]

OptionValues = Union[
    bool,
    int,
    Decimal,
    data.Booking,
    str,
    Dict,
    List[str],
    set,
    None,
]

MetaValues = Union[bool, int, Decimal, str, Dict[str, Decimal]]