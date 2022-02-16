from typing import List

import beancount_hypothesis as h
from beancount.core import amount, inventory, position
from conftest import Ctx
from hypothesis import given

from bdantic.models import data


@given(h.amount())
def test_amount(ctx: Ctx, amt: amount.Amount):
    try:
        pamt = data.Amount.parse(amt)
    except AssertionError:
        return

    ctx.compare_object(pamt, amt)
    ctx.compare_object(pamt.export(), amt, False)


@given(h.cost())
def test_cost(ctx: Ctx, cost: position.Cost):
    try:
        pcost = data.Cost.parse(cost)
    except AssertionError:
        return

    ctx.compare_object(pcost, cost)
    ctx.compare_object(pcost.export(), cost, False)


@given(h.costspec())
def test_costspec(ctx: Ctx, costspec: position.CostSpec):
    try:
        pcostspec = data.CostSpec.parse(costspec)
    except AssertionError:
        return

    ctx.compare_object(pcostspec, costspec)
    ctx.compare_object(pcostspec.export(), False)


@given(h.inventory())
def test_inventory(ctx: Ctx, pos: List[position.Position]):
    # None break beancount
    for p in pos:
        if not p.units.number:
            return

    inv = inventory.Inventory(pos)
    try:
        pinv = data.Inventory.parse(inv)
    except AssertionError:
        return

    ctx.compare_object(pinv, inv)
    ctx.compare_object(pinv.export(), inv, False)


@given(h.position())
def test_position(ctx: Ctx, pos: position.Position):
    try:
        ppos = data.Position.parse(pos)
    except AssertionError:
        return

    ctx.compare_object(ppos, pos)
    ctx.compare_object(ppos.export(), pos, False)
