from beancount.core import amount, data, inventory, position
from bdantic import models
from typing import Dict, List, Sequence, Type

# Maps Beancount types to their respective models
_type_map: Dict[Type[models.BeancountType], Type[models.Model]] = {
    amount.Amount: models.Amount,
    data.Balance: models.Balance,
    data.Close: models.Close,
    data.Commodity: models.Commodity,
    position.Cost: models.Cost,
    position.CostSpec: models.CostSpec,
    data.Custom: models.Custom,
    data.Document: models.Document,
    data.Event: models.Event,
    data.Note: models.Note,
    data.Open: models.Open,
    data.Pad: models.Pad,
    position.Position: models.Position,
    data.Posting: models.Posting,
    data.Price: models.Price,
    data.Query: models.Query,
    data.Transaction: models.Transaction,
    data.TxnPosting: models.TxnPosting,
    inventory.Inventory: models.Inventory,
}


def parse(obj: models.BeancountType) -> models.Model:
    """Parses a Beancount type into it's respective Pydantic models.

    Args:
        obj: A valid BeancountType

    Returns:
        The associated model for the given BeancountType
    """
    return _type_map[type(obj)].parse(obj)  # type: ignore


def parse_all(objs: Sequence[models.BeancountType]) -> List[models.Model]:
    """Parses a list of Beancount types into a list of their respective
    Pydantic models.

    Args:
        objs: A list of valid BeancountType's

    Returns:
        A list of associated models for each BeancountType
    """
    return [parse(obj) for obj in objs]
