from math import trunc
from datetime import datetime
import os

#Returns a value truncated to a specific number of decimal places.
def truncate(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)
    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

#Logging function
def logging(TYYPPI, PARI, LYHYT, PITKA, PRINT):
  tyypit = {0: '[INFO]', 1: '[TRADE]', 2: '[ERROR]', 3: '[SYSTEM]'}
  printtiteksti = str(datetime.now()) + ', ' + tyypit[TYYPPI] + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA
  print(printtiteksti)
  logiteksti = tyypit[TYYPPI] + ', ' + str(datetime.now()) + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA + '\n'
  if TYYPPI == 1: logfilu = open('tradelog.txt','a')
  else: logfilu = open('botlog.txt','a')
  logfilu.write(logiteksti)
  logfilu.close()
  
#define if there has already been buy before, if so then sell next, if not then buy next
def checkLastAction(kolikko, maara, pari, client):
  kk = float(client.get_asset_balance(asset=kolikko)['free'])
  if kk >= maara and kk > (15/float(client.get_ticker(symbol=pari)['lastPrice'])): return 'BUY'
  else: return 'SELL'
  
#get candles
def getCandles(symbooli, intervalli, limitti, client):
  resp = client.get_klines(symbol=symbooli, interval=intervalli, limit=limitti)
  parsed_klines = []
  for k in resp:
    k_candle = {
      'open': float(k[1]),
      'high': float(k[2]),
      'low': float(k[3]),
      'close': float(k[4]),
      'vol': float(k[5]) 
    } 
    parsed_klines.append(k_candle)
  return parsed_klines

def handleTrade(kauppalause):
  #handle trade
  '''buy_order = eval(kauppalause)
  if buy_order == {}:
    buy_order = {'symbol': 'TESTING', 'orderId': 1111, 'cummulativeQuoteQty': '123.45', 'side':'TEST'}
  if buy_order['side'] == 'BUY':
    logging(1, tieto['symbol'],'Trade succesfull', '-' + str(buy_order['cummulativeQuoteQty']), 1)
  else:
    logging(1, tieto['symbol'],'Trade succesfull', '+' + str(buy_order['cummulativeQuoteQty']), 1)'''
  print(kauppalause)

def vaihdasuunta(vanha):
  uusi = ''
  if vanha.upper() == 'BUY': uusi = 'SELL'
  elif vanha.upper() == 'SELL': uusi = 'BUY'
  return uusi