from secrets import *
from binance.client import Client

client = Client(API_KEY, API_SECRET)

#get market depth
def getDepth(symbooli):
    depth = client.get_order_book(symbol=symbooli)
    return depth
#print(getDepth('ADABTC'))

#place test market buy order
def makeTestBuy(symbooli):
    print(client.create_test_order(symbol = symbooli, side = 'SELL', type = 'MARKET', quantity = 10))
    return 1
#print(makeTestBuy('ADAUSDT'))

# get balance
def getBalance(symbooli):
    balance = client.get_asset_balance(asset=symbooli)
    return balance
#print(getBalance('BTC'))

#get latest price
def getLatestPrice(symbooli):
    price = client.get_symbol_ticker(symbol=symbooli)
    return price
#print(getLatestPrice('ADABTC'))


print(SIGNALS['BTCUSDT'])
pp = SIGNALS['BTCUSDT']
print(pp[1])