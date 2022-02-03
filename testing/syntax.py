import os

from bdantic.models import (
    Balance,
    Close,
    Commodity,
    Document,
    Event,
    Note,
    Open,
    Pad,
    Price,
    Query,
    Transaction,
)

balance = "2022-01-01 balance Assets:US:BofA:Checking        2845.77 USD"

close = "2022-01-01 close Equity:Opening-Balances"

commodity = """2022-01-01 commodity USD
  export: "CASH"
  name: "US Dollar" """

document = f"""
2022-01-01 document Assets:US:Vanguard:Cash "{os.getcwd()}/test.doc" """

event = """2022-01-01 event "location" "Paris, France" """

note = """2022-01-01 note Liabilities:CreditCard "Called about fraudulence" """

open = """2022-01-01 open Liabilities:CreditCard:CapitalOne     USD"""

pad = "2022-01-01 pad Assets:BofA:Checking Equity:Opening-Balances"

price = "2022-01-01 price HOOL  579.18 USD"

query = """2022-01-01 query "france-balances" "
  SELECT account, sum(position) WHERE `trip-france-2014` in tags" """

transaction = """2022-01-01 * "Investing 40% of cash in VBMPX"
  Assets:US:Vanguard:VBMPX    1.122 VBMPX {213.90 USD, 2022-01-01}
  Assets:US:Vanguard:Cash   -240.00 USD"""

tests = [
    (balance, Balance),
    (close, Close),
    (commodity, Commodity),
    (document, Document),
    (event, Event),
    (note, Note),
    (open, Open),
    (pad, Pad),
    (price, Price),
    (query, Query),
    (transaction, Transaction),
]
