from requests import put, get, post
from renko import Renko
from time import time, sleep
from datetime import datetime
from math import floor

renko = Renko()
candlestick = None
execute_mode = None


def data_parse(data):
    global candlestick
    candle1 = data['latestCandles'][0]['candles'][0]
    candle2 = data['latestCandles'][0]['candles'][1]
    if candle1['complete'] and candle2['complete']:
        candle1epoch = datetime.strptime(candle1['time'], "%Y-%m-%dT%H:%M:%S.000000000Z")
        candle2epoch = datetime.strptime(candle2['time'], "%Y-%m-%dT%H:%M:%S.000000000Z")
        if candle1epoch > candle2epoch:
            candlestick = candle1
        elif candle1epoch < candle2epoch:
            candlestick = candle2
    elif candle1['complete'] and not candle2['complete']:
        candlestick = candle1
    elif not candle1['complete'] and candle2['complete']:
        candlestick = candle2


def buy():
    global execute_mode
    if execute_mode is True:
        close(False)

    if execute_mode is True or execute_mode is None:
        order(True)
        print("BUY EXECUTED")
        execute_mode = True


def sell():
    global execute_mode
    if execute_mode is True:
        close(True)

    if execute_mode is True or execute_mode is None:
        order(False)
        print("SELL EXECUTED")
        execute_mode = True


def close(signal):
    if signal:
        req_key = "longUnits"
    else:
        req_key = "shortUnits"

    put("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/positions/EUR_USD/close",
        headers={
            "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
        },
        data={
            req_key: "ALL"
        }
        )

    print("TRADE CLOSED")


def order(bull):
    summary = get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/summary",
                  headers={
                      "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
                  }).json()
    balance = float(summary['account']['balance'])
    margin_rate = float(summary['account']['marginRate'])
    units = floor((balance / 2) / margin_rate)
    if not bull:
        units *= -1

    post("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/orders",
         headers={
             "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
         },
         data={
             "order": {
                 "type": "MARKET",
                 "instrument": "EUR_USD",
                 "units": units,
                 "stopLossOnFill": {
                     "distance": 0.003
                 }
             }
         })


def do_something():
    test = get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/candles/latest",
               headers={
                   "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
               },
               params={
                   "count": 2,
                   "candleSpecifications": "EUR_USD:M15:BAM"}).json()
    data_parse(test)
    renko.feed(float(candlestick['mid']['c']))
    if renko.is_bull():
        buy()
    elif renko.is_bear():
        sell()


hist = get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/instruments/EUR_USD/candles",
           headers={
               "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
           },
           params={
               "price": "BAM",
               "count": 5000,
               "granularity": "M15"}).json()

for candle in hist['candles']:
    renko.feed(float(candle['mid']['c']))
    # if renko.is_bull():
    #     print(candle['time'])
    #     buy()
    # elif renko.is_bear():
    #     print(candle['time'])
    #     sell()

while True:
    start = time()
    do_something()
    end = time()
    wait_duration = 1 - (end - start)
    if wait_duration > 0:
        sleep(wait_duration)

# test2 = requests.get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/summary",
#                      headers={
#                          "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                      }).json()
# margin = (float(test2['account']['balance']) / float(test2['account']['marginRate'])) / 2
# while True:
#     test = requests.get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/candles/latest",
#                         headers={
#                             "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                         },
#                         params={
#                             "count": 2,
#                             "candleSpecifications": "EUR_USD:M5:BAM"}).json()
#     print(test)
