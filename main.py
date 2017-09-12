import random


class Trader:

    def __init__(self, api):
        self.btc_balance = 0.002
        self.usd_balance = 0.0
        self.api = api

    def btc_buy(self, cost):
        if self.usd_balance > 0:
            self.usd_balance -= self.usd_balance*0.0025
            amount = self.usd_balance/cost
            self.usd_balance = 0.0
            self.btc_balance = amount
            print ("BTC Buy:%.8f" % amount)
            print ("BTC Balance:%.8f" % self.btc_balance)
            print ("USD Balance:%.8f" % self.usd_balance)
        else:
            print ("Not USD money!")

    def btc_sell(self, cost):
        if self.btc_balance > 0.001:
            self.btc_balance -= self.btc_balance * 0.0025
            amount = self.btc_balance
            self.usd_balance = float(self.btc_balance * cost)
            self.btc_balance = 0.0
            print ("BTC Sell:%.8f" % amount)
            print ("BTC Balance:%.8f" % self.btc_balance)
            print ("USD Balance:%.8f" % self.usd_balance)
        else:
            print ("Not BTC!")

if __name__ == "__main__":
    trader = Trader("api")
    cost = [x for x in range(4096, 4296)]
    for t in cost:
        flag = random.randint(0, 1)
        if flag == 0:
            trader.btc_buy(t)
        else:
            trader.btc_sell(t)



