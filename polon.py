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

t1 = "12/9/2017 03:00:00"
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

btc_trace = go.Scatter(x=[], y=[], stream=go.Stream(token="x8njptzh23"))
sma_trace = go.Scatter(x=[], y=[], stream=go.Stream(token="hmyl27u0oq"))
py.plot([btc_trace, sma_trace], filename='basic-line')

s1 = py.Stream("x8njptzh23")
s2 = py.Stream("hmyl27u0oq")
s1.open()
s2.open()
current = []
while True:
    x1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    y1 = float(polo.returnTicker()['USDT_BTC']["last"])
    current.append({"date": x1, "cost": y1})
    quotes['close'] = numpy.asarray([item['cost'] for item in current])
    sma = talib.SMA(quotes["close"], timeperiod=50)
    y2 = sma[-1]
    s1.write(dict(x=x1, y=y1))
    s2.write(dict(x=x1, y=y2))
    print sma
    time.sleep(10)
s1.close()
s2.close()

#ema_trace = go.Scatter(x=dataframe.index, y=ema, stream=go.Stream(token="mfy4jzuizz"))

