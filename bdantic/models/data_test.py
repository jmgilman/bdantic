from beancount.core import amount, inventory, position
from .data import Amount, Cost, CostSpec, Inventory, Position
from decimal import Decimal
from hypothesis import given, strategies as s
from testing import common as t
from typing import List


def setup_module(_):
    s.register_type_strategy(Decimal, s.decimals(allow_nan=False))


@given(s.builds(amount.Amount))
def test_amount(amt: amount.Amount):
    try:
        pamt = Amount.parse(amt)
    except AssertionError:
        return

    t.compare_object(pamt, amt, t.Ctx())
    t.compare_object(pamt.export(), amt, t.Ctx(partial=False))


@given(s.builds(position.Cost))
def test_cost(cost: position.Cost):
    try:
        pcost = Cost.parse(cost)
    except AssertionError:
        return

    t.compare_object(pcost, cost, t.Ctx())
    t.compare_object(pcost.export(), cost, t.Ctx(partial=False))


@given(s.builds(position.CostSpec))
def test_costspec(costspec: position.CostSpec):
    try:
        pcostspec = CostSpec.parse(costspec)
    except AssertionError:
        return

    t.compare_object(pcostspec, costspec, t.Ctx())
    t.compare_object(pcostspec.export(), costspec, t.Ctx(partial=False))


@given(s.lists(s.builds(position.Position)))
def test_inventory(pos: List[position.Position]):
    # None break beancount
    for p in pos:
        if not p.units.number:
            return

    inv = inventory.Inventory(pos)
    try:
        pinv = Inventory.parse(inv)
    except AssertionError:
        return

    t.compare_object(pinv, inv, t.Ctx())
    t.compare_object(pinv.export(), inv, t.Ctx(partial=False))


@given(s.builds(position.Position))
def test_position(pos: position.Position):
    try:
        ppos = Position.parse(pos)
    except AssertionError:
        return

    r = [Amount, Cost]
    t.compare_object(ppos, pos, t.Ctx(recurse=r))
    t.compare_object(ppos.export(), pos, t.Ctx(partial=False, recurse=r))
