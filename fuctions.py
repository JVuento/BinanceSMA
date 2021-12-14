import os
import math
from math import trunc
from datetime import datetime


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
  if TYYPPI == 1: logfilu = open('tradelog2.txt','a')
  else: logfilu = open('botlog2.txt','a')
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

def handleTrade(kauppalause, client, tieto):
  #handle trade
  print(kauppalause)
  buy_order = eval(kauppalause)
  if buy_order == {}:
    buy_order = {'symbol': 'TESTING', 'orderId': 1111, 'cummulativeQuoteQty': '123.45', 'side':'TEST'}
  if buy_order['side'] == 'BUY':
    logging(1, tieto['symbol'],'Trade succesfull', '-' + str(buy_order['cummulativeQuoteQty']), 1)
  else:
    logging(1, tieto['symbol'],'Trade succesfull', '+' + str(buy_order['cummulativeQuoteQty']), 1)

def vaihdasuunta(vanha):
  uusi = ''
  if vanha.upper() == 'BUY': uusi = 'SELL'
  elif vanha.upper() == 'SELL': uusi = 'BUY'
  return uusi

def countRSI(lista, period):
  if len(lista) <= period: raise Exception('Too few values to count RSI')
  last = 0
  gains = 0
  losses = 0
  for i in range(len(lista)):
    luku = lista[i]
    if last == 0:
      last = luku
    else:
      if luku < last:
        losses = losses + (last - luku)/last
      elif luku > last:
        gains = gains + (luku - last)/last
    last = luku
  last_loss = 0
  last_gain = 0
  if lista[-1] < lista[-2]: last_loss = (lista[-2] - lista[-1]) / lista[-2]
  elif lista[-1] > lista[-2]: last_gain = (lista[-1] - lista[-2]) / lista[-2]
  per = period-1
  avggains = per*gains/period + last_gain/period
  avglosses = per*losses/period + last_loss/period
  if avglosses == 0: RSI = 100
  elif avggains == 0: RSI = 0
  else:
    RS = avggains / avglosses
    RSI = 100 - 100 / ( 1 + RS )
  return RSI

