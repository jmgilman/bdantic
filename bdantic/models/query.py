from __future__ import annotations

from .base import Base
from beancount.core import amount, inventory, position
import collections
from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from ..types import type_map
from typing import Any, Dict, List, Literal, Tuple, Type

QueryRow = Dict[str, Any]

_map: Dict[str, Type] = {
    "Amount": amount.Amount,
    "bool": bool,
    "date": date,
    "Decimal": Decimal,
    "int": int,
    "Inventory": inventory.Inventory,
    "Position": position.Position,
    "str": str,
}


class QueryColumn(BaseModel):
    name: str
    type: str


class QueryResult(Base):
    """A model representing the result from a beancount query."""

    ty: Literal["QueryResult"] = "QueryResult"
    columns: List[QueryColumn]
    rows: List[QueryRow]

    @classmethod
    def parse(
        cls, obj: Tuple[List[Tuple[str, Type]], List[Any]]
    ) -> QueryResult:
        """Parses a beancount query result into this model

        Args:
            obj: The Beancount query result

        Returns:
            A new instance of this model
        """
        columns: List[QueryColumn] = []
        for column in obj[0]:
            columns.append(
                QueryColumn(name=column[0], type=column[1].__name__)
            )

        rows: List[QueryRow] = []
        for row in obj[1]:
            d = row._asdict()
            for k, v in d.items():
                if type(v) in type_map.keys():
                    d[k] = type_map[type(v)].parse(v)

            rows.append(d)

        return QueryResult(columns=columns, rows=rows)

    def export(self) -> Tuple[List[Tuple[str, Type]], List[Any]]:
        """Exports this model into a beancount query result

        Returns:
            A new instance of a beancount query result
        """
        column_names = [v.name for v in self.columns]
        ResultRow = collections.namedtuple(  # type: ignore
            "ResultRow",
            column_names,
        )

        columns: List[Tuple[str, Type]] = []
        for column in self.columns:
            columns.append((column.name, _map[column.type]))

        rows: List[ResultRow] = []
        for row in self.rows:
            values = []
            for key in column_names:
                if type(row[key]) in type_map.values():
                    values.append(row[key].export())
                else:
                    values.append(row[key])
            rows.append(ResultRow._make(values))

        return (columns, rows)
