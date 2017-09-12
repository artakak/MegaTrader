from poloniex import Poloniex
import time
import datetime
import requests
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

py.sign_in('artakak', 'hMpl7NDNfAm3WljsGzCg')
polo_stat = []
polo = Poloniex()
print(polo.returnTicker()['USDT_BTC'])

t1 = "7/9/2017 11:00:00"
t2 = "7/9/2017 12:00:00"
unix1 = time.mktime(datetime.datetime.strptime(t1, "%d/%m/%Y %H:%M:%S").timetuple())
unix2 = time.mktime(datetime.datetime.strptime(t2, "%d/%m/%Y %H:%M:%S").timetuple())
data = polo.returnChartData('USDT_BTC', 300, unix1, unix2)

print data
for t in data:
    print("%s %s") % (t['weightedAverage'], str(datetime.datetime.fromtimestamp(t['date'])))

dataframe = pd.DataFrame(data)
dataframe['date'] = [pd.to_datetime(t['date'], unit='s') for t in data]
dataframe.set_index('date', inplace=True)
print dataframe

trace1 = go.Scatter(x=[], y=[], stream=go.Stream(token="x8njptzh23"))
trace2 = go.Scatter(x=[], y=[], stream=go.Stream(token="hmyl27u0oq"))
data = go.Data([trace1, trace2])
fig = go.Figure(data=data)
py.plot(fig, filename='python-streaming')
s1 = py.Stream("x8njptzh23")
s2 = py.Stream("hmyl27u0oq")
s1.open()
s2.open()
url = "https://api.livecoin.net/exchange/ticker?currencyPair=DASH/BTC"
while True:
    x1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    y1 = float(polo.returnTicker()['BTC_DASH']["last"])
    req = requests.get(url)
    y2 = float(req.json()["last"])
    s1.write(dict(x=x1, y=y1))
    s2.write(dict(x=x1, y=y2))
    time.sleep(10)
print polo_stat
s1.close()
s2.close()
#btc_trace = go.Scatter(x=dataframe.index, y=dataframe['weightedAverage'])
#py.plot([btc_trace], filename='basic-line')
