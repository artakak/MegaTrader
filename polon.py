from poloniex import Poloniex
import time
import datetime
import requests
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import talib
import numpy
from main import Trader

py.sign_in('artakak', 'hMpl7NDNfAm3WljsGzCg')
polo_stat = []
polo = Poloniex()
print(polo.returnTicker()['USDT_BTC'])

t1 = "19/10/2017 03:00:00"
t2 = "8/9/2017 03:00:00"
unix1 = time.mktime(datetime.datetime.strptime(t1, "%d/%m/%Y %H:%M:%S").timetuple())
unix2 = time.mktime(datetime.datetime.strptime(t2, "%d/%m/%Y %H:%M:%S").timetuple())
data = polo.returnChartData('USDT_BTC', 300, unix1)

print data
for t in data:
    print("%s %s") % (t['weightedAverage'], str(datetime.datetime.fromtimestamp(t['date'])))

dataframe = pd.DataFrame(data)
dataframe['date'] = [pd.to_datetime(t['date'], unit='s') for t in data]
dataframe.set_index('date', inplace=True)
print dataframe
quotes = {}
quotes['close'] = numpy.asarray([float(item['close']) for item in data])

btc_trace = go.Candlestick(x=[], open=[], high=[], low=[], close=[], stream=go.Stream(token="x8njptzh23"))
#btc_trace = go.Scatter(x=[], y=[], stream=go.Stream(token="x8njptzh23"))
sma_trace = go.Scatter(x=[], y=[], stream=go.Stream(token="hmyl27u0oq"))
ema_trace = go.Scatter(x=[], y=[], stream=go.Stream(token="mfy4jzuizz"))
py.plot([btc_trace, sma_trace, ema_trace], filename='basic-line')

s1 = py.Stream("x8njptzh23")
s2 = py.Stream("hmyl27u0oq")
s3 = py.Stream("mfy4jzuizz")
s1.open()
s2.open()
s3.open()
current = []


def candle_data(count, period):
    candle = {}
    prices = [float(polo.returnTicker()['USDT_BTC']["last"])]
    for _ in range(count):
        time.sleep(period)
        prices.append(float(polo.returnTicker()['USDT_BTC']["last"]))
    candle["open"] = prices[0]
    candle["close"] = prices[-1]
    candle["high"] = max(prices)
    candle["low"] = min(prices)
    return candle


while True:
    #time.sleep(60)
    try:
        candle = candle_data(5, 10)
        y1 = float(polo.returnTicker()['USDT_BTC']["last"])
    except:
        continue
    x1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current.append({"date": x1, "cost": y1})
    if len(current) > 50:
        current.__delitem__(0)
    quotes['close'] = numpy.asarray([item['cost'] for item in current])
    sma = talib.SMA(quotes["close"], timeperiod=50)
    ema = talib.EMA(quotes["close"], timeperiod=30)
    y2 = sma[-1]
    y3 = ema[-1]
    try:
        s1.write(dict(x=x1, open=candle["open"], high=candle["high"], low=candle["low"], close=candle["close"]), validate=False)
        s2.write(dict(x=x1, y=y2))
        s3.write(dict(x=x1, y=y3))
    except:
        pass
    print sma
    print "\n***\n"
    print ema

s1.close()
s2.close()
s3.close()

