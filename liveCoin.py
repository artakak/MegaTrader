import requests


url = "https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD"
req = requests.get(url)
print req.json()