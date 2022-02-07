from math import floor
from time import sleep
from requests import get, post, put


def close(signal):
    if signal:
        req_key = "longUnits"
    else:
        req_key = "shortUnits"

    test = put("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/positions/EUR_USD/close",
        headers={
            "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
        },
        json={
            req_key: "ALL"
        }
        )

    print("TRADE CLOSED")



close(False)
