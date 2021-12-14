import os
import math
from math import trunc
from datetime import datetime

#Logging function
def logging(TYYPPI, PARI, LYHYT, PITKA, PRINT):
  tyypit = {0: '[INFO]', 1: '[TRADE]', 2: '[ERROR]', 3: '[SYSTEM]'}
  printtiteksti = str(datetime.now()) + ', ' + tyypit[TYYPPI] + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA
  print(printtiteksti)
  logiteksti = tyypit[TYYPPI] + ', ' + str(datetime.now()) + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA + '\n'
  if TYYPPI == 1: logfilu = open('orderlog.txt','a')
  else: logfilu = open('botlog.txt','a')
  logfilu.write(logiteksti)
  logfilu.close()
  
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

#define if there has already been buy before, if so then sell next, if not then buy next
def checkLastAction(kolikko, pari, altmaara, client):
  if float(altmaara) > (15/float(client.get_ticker(symbol=pari)['lastPrice'])): return 'BUY'
  else: return 'SELL'

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

def handleTrade(kauppalause, symbooli, client):
  #handle trade
  #print(kauppalause)
  buy_order = eval(kauppalause)
  if buy_order == {}:
    buy_order = {'symbol': 'TESTING', 'orderId': 1111, 'cummulativeQuoteQty': '123.45', 'side':'TEST'}
  logging(3, symbooli,'Trade order inserted', '-' + str(buy_order), 1)

def cancelOrder(orderiid, symbooli, client):
  result = client.cancel_order(symbol=symbooli,orderId=orderiid)
  logging(3, symbooli,'Trade order canceled', '-' + str(result), 1)
  return result