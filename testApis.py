from secrets import *
from settings import *
from binance.client import Client
import sys
from datetime import datetime
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
#example return: {'asset': 'BTC', 'free': '0.00849630', 'locked': '0.00000000'}


#get latest price
def getLatestPrice(symbooli):
    price = client.get_symbol_ticker(symbol=symbooli)
    return price
#print(getLatestPrice('ADABTC'))

#get ticker
def getTicker(symbooli):
    tikkeri = client.get_ticker(symbol=symbooli)
    return tikkeri
#print(getTicker('BTCUSDT'))

#Get trades per pair and print in kaupat.txt
def getTrades():
    filu = open('kaupat.txt','a')
    for each in SIGNALS:
        print(each)
        trades = client.get_my_trades(symbol=each[0],limit=10)
        for i in trades:
          i['time'] = datetime.fromtimestamp(i['time']/1000).strftime('%Y %B %d %H:%M:%S')
          filu.write(str(i) + '\n')
    return 1
kk = getTrades()


def writeHtml(lause):
  filu = open('index.html','w')
  htmlalku = """
  <!DOCTYPE html>
  <html>
  <head>
  <meta http-equiv="refresh" content="1">
  </head>
  <body>
  <h2>BinanceSMA """ + str(datetime.now()) + """</h2> 
  <p>
  """
  htmlloppu = """
  </p>
  </body>
  </html>
  """
  filu.write(htmlalku + lause + htmlloppu)
  filu.close
#writeHtml('BTCUSDT: stopped')

#get candles
def getCandles():
  resp = client.get_klines(symbol='BTCUSDT', interval='1h', limit=4)
  return resp
#print(getCandles())

#print(SIGNALS['BTCUSDT'])
#pp = SIGNALS['BTCUSDT']
#print(pp[1])
#argumentit = sys.argv
#if len(sys.argv)<2: symbol = 'REEFUSDT'
#else: symbol = argumentit[1]
#print(symbol)
