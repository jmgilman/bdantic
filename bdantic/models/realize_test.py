from beancount import loader
from beancount.core import realization
from hypothesis import given
from .realize import RealAccount
from testing import generate as g


def setup_module(_):
    g.register()


@given(g.transactions())
def test_realaccount(txns):
    ra = realization.realize(txns)
    pra = RealAccount.parse(ra)
    era = pra.export()

    assert era == ra


def test_realize():
    entries, _, options = loader.load_file("testing/static.beancount")
    ra = realization.realize(entries)
    pra = RealAccount.parse(ra)
    era = pra.export()

    assert era == ra
