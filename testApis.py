from secrets import *
from settings import *
from binance.client import Client
import sys
from datetime import datetime
from bfxhfindicators import sma
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
#print(getBalance('DAI'))
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
#kk = getTrades()


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
  resp = client.get_klines(symbol='FTMUSDT', interval='4h', limit=5)
  return resp
a = getCandles()
'''
print(a)
sulku = 0.0 
avaus = 0.0
sma1 = sma.SMA(5)
sma2 = sma.SMA(5)
for each in a:
  avaus = avaus + float(each[1])
  sulku = sulku + float(each[4])
  sma1.add(float(each[1]))
  sma2.add(float(each[4]))
sma1_value = sma1.v() 
sma2_value = sma2.v()           
sulku = sulku / len(a)
avaus = avaus / len(a)
print('KA open: ' + str(avaus))
print('KA close: ' + str(sulku))
print('SMA open: ' + str(sma1_value))
print('SMA close: ' + str(sma2_value))
'''


#print(SIGNALS['BTCUSDT'])
#pp = SIGNALS['BTCUSDT']
#print(pp[1])
#argumentit = sys.argv
#if len(sys.argv)<2: symbol = 'REEFUSDT'
#else: symbol = argumentit[1]
#print(symbol)
#per = [1,2,3]
#se = per.copy()
#se.pop(0)
#print(per)
#print(se)
#pp = ['Buy','Buy']
#print(not 'Buy' in pp)
#kk = {'symbol': 'BTCDAI', 'orderId': 54189885, 'orderListId': -1, 'clientOrderId': '1bIkvtgFE9FEKLUexyP4Eu', 'transactTime': 1618300825964, 'price': '0.00000000', 'origQty': '0.01076300', 'executedQty': '0.01076300', 'cummulativeQuoteQty': '658.10890887', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '61145.49000000', 'qty': '0.01076300', 'commission': '0.00089526', 'commissionAsset': 'BNB', 'tradeId': 2475086}]}
#print(str(kk['cummulativeQuoteQty']))
