"""Provides models for constructing a DisplayContext."""

from __future__ import annotations

import collections

from .base import Base
from beancount.core import distribution, display_context
from typing import Literal


class CurrencyContext(Base):
    """A model representing a `beancount.core.display_context._CurrencyContext`.

    Attributes:
        ty: A string literal identifying this model.
        has_sign: True if at least one of the numbers has a negative or
            explicit positive sign.
        integer_max: The maximum number of digits for the integer part.
        fractional_dist: A frequency distribution of fractionals seen in the
            input file.
    """

    _sibling = display_context._CurrencyContext
    ty: Literal["CurrencyContext"] = "CurrencyContext"
    has_sign: bool
    integer_max: int
    fractional_dist: Distribution

    @classmethod
    def parse(cls, obj: display_context._CurrencyContext) -> CurrencyContext:
        """Parses a beancount CurrencyContext into this model

        Args:
            obj: The Beancount CurrencyContext to parse

        Returns:
            A new instance of this model
        """

        return CurrencyContext(
            has_sign=obj.has_sign,
            integer_max=obj.integer_max,
            fractional_dist=Distribution.parse(obj.fractional_dist),
        )

    def export(self) -> display_context._CurrencyContext:
        """Exports this model into a beancount CurrencyContext

        Returns:
            A new instance of a beancount CurrencyContext
        """
        ctx = display_context._CurrencyContext()
        ctx.has_sign = self.has_sign
        ctx.integer_max = self.integer_max
        ctx.fractional_dist = self.fractional_dist.export()
        return ctx


class DisplayContext(Base):
    """A model representing a `beancount.core.display_context.DisplayContext`.

    Attributes:
        ty: A string literal identifying this model.
        ccontexts: A dict of currency string to CurrencyContext instances.
        commas: True if we should render commas.
    """

    _sibling = display_context.DisplayContext
    ty: Literal["DisplayContext"] = "DisplayContext"
    ccontexts: collections.defaultdict
    commas: bool

    @classmethod
    def parse(cls, obj: display_context.DisplayContext) -> DisplayContext:
        """Parses a beancount DisplayContext into this model

        Args:
            obj: The Beancount DisplayContext to parse

        Returns:
            A new instance of this model
        """
        ccontexts = collections.defaultdict(
            CurrencyContext,
            {k: CurrencyContext.parse(v) for (k, v) in obj.ccontexts.items()},
        )
        return DisplayContext(ccontexts=ccontexts, commas=obj.commas)

    def export(self) -> display_context.DisplayContext:
        """Exports this model into a beancount DisplayContext

        Returns:
            A new instance of a beancount DisplayContext
        """
        ccontexts = collections.defaultdict(
            display_context._CurrencyContext,
            {k: v.export() for (k, v) in self.ccontexts.items()},
        )
        ctx = display_context.DisplayContext()
        ctx.ccontexts = ccontexts
        ctx.commas = self.commas
        return ctx


class Distribution(Base):
    """A model representing a `beancount.core.distribution.Distribution`.

    Attributes:
        ty: A string literal identifying this model.
        hist: A histogram of integer values.
    """

    _sibling = distribution.Distribution
    ty: Literal["Distribution"] = "Distribution"
    hist: collections.defaultdict

    @classmethod
    def parse(cls, obj: distribution.Distribution) -> Distribution:
        """Parses a beancount Distribution into this model

        Args:
            obj: The Beancount Distribution to parse

        Returns:
            A new instance of this model
        """

        return Distribution(hist=obj.hist)

    def export(self) -> distribution.Distribution:
        """Exports this model into a beancount Distribution

        Returns:
            A new instance of a beancount Distribution
        """
        dist = distribution.Distribution()
        dist.hist = self.hist
        return dist


CurrencyContext.update_forward_refs()
