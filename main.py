# from requests import put, post
# from oanda_get import oanda_get
# from renko import Renko
# from time import time, sleep
# from datetime import datetime
# from math import floor
#
# renko = Renko()
# candlestick = None
# execute_mode = None
#
#
# def data_parse(data):
#     global candlestick
#     candle1 = data['latestCandles'][0]['candles'][0]
#     candle2 = data['latestCandles'][0]['candles'][1]
#     if candle1['complete'] and candle2['complete']:
#         candle1epoch = datetime.strptime(candle1['time'], "%Y-%m-%dT%H:%M:%S.000000000Z")
#         candle2epoch = datetime.strptime(candle2['time'], "%Y-%m-%dT%H:%M:%S.000000000Z")
#         if candle1epoch > candle2epoch:
#             candlestick = candle1
#         elif candle1epoch < candle2epoch:
#             candlestick = candle2
#     elif candle1['complete'] and not candle2['complete']:
#         candlestick = candle1
#     elif not candle1['complete'] and candle2['complete']:
#         candlestick = candle2
#
#
# def buy():
#     global execute_mode
#     if execute_mode is True:
#         close(False)
#
#     if execute_mode is True or execute_mode is None:
#         order(True)
#         print("BUY EXECUTED")
#         execute_mode = True
#
#
# def sell():
#     global execute_mode
#     if execute_mode is True:
#         close(True)
#
#     if execute_mode is True or execute_mode is None:
#         order(False)
#         print("SELL EXECUTED")
#         execute_mode = True
#
#
# def close(signal):
#     if signal:
#         req_key = "longUnits"
#     else:
#         req_key = "shortUnits"
#
#     put("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/positions/EUR_USD/close",
#         headers={
#             "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#         },
#         json={
#             req_key: "ALL"
#         }
#         )
#
#     print("TRADE CLOSED")
#
#
# def order(bull):
#     summary = oanda_get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/summary",
#                         headers={
#                             "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                         }).json()
#     while summary['account']['openPositionCount'] == 1:
#         print('Close Pending...')
#         summary = oanda_get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/summary",
#                             headers={
#                                 "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                             }).json()
#         sleep(0.5)
#     balance = float(summary['account']['marginAvailable'])
#     print(summary)
#
#     margin_rate = float(summary['account']['marginRate'])
#     units = floor((balance / 2) / margin_rate)
#     print('Units: {}'.format(units))
#     if not bull:
#         units *= -1
#
#     order_result = post("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/orders",
#                         headers={
#                             "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                         },
#                         json={
#                             "order": {
#                                 "type": "MARKET",
#                                 "instrument": "EUR_USD",
#                                 "units": units,
#                                 "stopLossOnFill": {
#                                     "distance": 0.003
#                                 }
#                             }
#                         }).json()
#     print(order_result)
#
#
# def do_something():
#     test = oanda_get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/candles/latest",
#                      headers={
#                          "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                      },
#                      params={
#                          "count": 2,
#                          "candleSpecifications": "EUR_USD:M15:BAM"}).json()
#     data_parse(test)
#     renko.feed(float(candlestick['mid']['c']))
#     if renko.is_bull():
#         buy()
#     elif renko.is_bear():
#         sell()
#
#
# hist = oanda_get("https://api-fxpractice.oanda.com/v3/accounts/101-004-5674482-009/instruments/EUR_USD/candles",
#                  headers={
#                      "Authorization": "Bearer 5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5"
#                  },
#                  params={
#                      "price": "BAM",
#                      "count": 5000,
#                      "granularity": "M15"}).json()
#
# for candle in hist['candles']:
#     renko.feed(float(candle['mid']['c']))
#     # if renko.is_bull():
#     #     print(candle['time'])
#     #     buy()
#     # elif renko.is_bear():
#     #     print(candle['time'])
#     #     sell()
#
# while True:
#     start = time()
#     do_something()
#     end = time()
#     wait_duration = 1 - (end - start)
#     if wait_duration > 0:
#         sleep(wait_duration)

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
from v20 import Context
from v20.transaction import StopLossDetails
from v20.instrument import Candlestick, CandlestickData
from v20.order import EntitySpec as OrderEntitySpec, MarketOrderRequest
from v20.account import EntitySpec as AccountEntitySpec
from v20.position import EntitySpec as PositionEntitySpec
from redis import Redis
from RenkoBricks import BlankBrick, BullBrick, BearBrick
from json import loads
from CandlestickDataAdvanced import CandlestickAdvanced
from datetime import datetime


def margin_available(ctx):
    return AccountEntitySpec(ctx).summary("101-004-5674482-009").body['account'].marginAvailable


def buy(ctx):
    buy_order = OrderEntitySpec(oanda_context).create("101-004-5674482-009", order=MarketOrderRequest(
        instrument="EUR_USD", units=margin_available(ctx) / 2, stopLossOnFill=StopLossDetails(distance=0.003)
    ))
    if buy_order.status != 200 or buy_order.status != 201:
        raise ValueError("Buy Order returned code {}".format(buy_order.status))


def sell(ctx):
    sell_order = OrderEntitySpec(oanda_context).create("101-004-5674482-009", order=MarketOrderRequest(
        instrument="EUR_USD", units=(margin_available(ctx) / 2) * -1, stopLossOnFill=StopLossDetails(distance=0.003)
    ))
    if sell_order.status != 200 or sell_order.status != 201:
        raise ValueError("Sell Order returned code {}".format(sell_order.status))


def close(ctx, signal):
    if signal:
        close_order = PositionEntitySpec(ctx).close("101-004-5674482-009", "EUR_USD", longUnits="ALL")
    else:
        close_order = PositionEntitySpec(ctx).close("101-004-5674482-009", "EUR_USD", shortUnits="ALL")

    if close_order.status != 200:
        raise ValueError("Close Order returned code {}".format(close_order.status))


if __name__ == '__main__':
    redis = Redis(host='192.168.10.166', port=6379, db=0)
    psubscribe = redis.pubsub()

    oanda_context = Context("api-fxpractice.oanda.com",
                            token="5952c019ff679e3bd52cacc82a1599ab-6469870a2ec126764f162fafc5e36be5")
    hist = oanda_context.pricing.candles("101-004-5674482-009", "EUR_USD", price="M", granularity="M15", count=5000).body["candles"]
    brick = None
    for i in range(len(hist)):
        candle = hist[i]
        if i == 0:
            brick = BlankBrick(candle.mid.c)
        else:
            brick = brick.feed(candle.mid.c)

    candle_advanced = CandlestickAdvanced("M15")
    candle_advanced.feed(hist[-1])
    psubscribe.psubscribe("ticks.EUR_USD")
    for message in psubscribe.listen():
        if message is not None and isinstance(message, dict):
            if message.get('data') != 1:
                data = loads(message.get('data').decode('utf-8'))
                redis_candle = Candlestick()
                redis_candle.time = data['time']
                redis_candle.mid = CandlestickData(c=data['mid'])
                candle_advanced.feed(redis_candle)
                if candle_advanced.complete:
                    old_brick = brick
                    brick = brick.feed(candle_advanced.mid.c)
                    if not type(old_brick) == type(brick):
                        if isinstance(brick, BullBrick):
                            close(oanda_context, False)
                            buy(oanda_context)
                            print("BUY SIGNAL AT {}".format(datetime.now()))
                        elif isinstance(brick, BearBrick):
                            close(oanda_context, True)
                            sell(oanda_context)
                            print("SELL SIGNAL AT {}".format(datetime.now()))
                    old_candle_advanced = candle_advanced
                    candle_advanced = CandlestickAdvanced("M15")
                    candle_advanced.feed(old_candle_advanced)
                print(data['time'])