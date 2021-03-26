#==============================================================================================================#
# BinaceSMA.py  
# small bot to trade in binance with help of SMA x 2
#
#
# Before run make sure you have bfx-hf-indicators-p and python-binance installed in you python : 
#  pip install git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#  pip install python-binance
#  more info about python-binance lib here: https://algotrading101.com/learn/binance-python-api-guide/
#
# Remember you are using this at your own risk, don't come crying to us if it fucks up your wallet. Thank you.
#==============================================================================================================#

import requests
import json
import os
import time
import sys
import math
from datetime import datetime
from bfxhfindicators import sma
from secrets import *
from binance.client import Client
from math import trunc



def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

#writes last log info to index.html, for easier cloud usage
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
  return 1
  

#Logging function
# logging(TYYPPI, PARI, LYHYT, PITKA, PRINT)
# example:(1, 'BTCUSDT',"Buy successful", "{'symbol': 'BTCUSDT', 'priceChange': '1769.10000000'...}")
#  TYYPPI:
#   0: Info, 1: Trade, 2: Error, 3: System
# 0 is not logged only printed
def logging(TYYPPI, PARI, LYHYT, PITKA, PRINT):
  tyypit = {0: '[INFO]', 1: '[TRADE]', 2: '[ERROR]', 3: '[SYSTEM]'}
  if PRINT == 1:
    printtiteksti = tyypit[TYYPPI] + ', ' + PARI + ': ' + LYHYT
    print(printtiteksti)
  logiteksti = tyypit[TYYPPI] + ', ' + str(datetime.now()) + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA
  if TYYPPI != 0:
    if TYYPPI == 1: logfilu = open('tradelog.txt','a')
    else: logfilu = open('botlog.txt','a')
    logfilu.write(logiteksti)
    logfilu.close()
  writeHtml(tyypit[TYYPPI] + ' ' + PARI + ' ' + LYHYT)
  return 1


#get last price 
def getLastPrice(symbooli):
    tikkeri = client.get_ticker(symbol=symbooli)['lastPrice']
    return tikkeri

#check if script was called with argument for traded pair, if so use them
def checkArgs(argumentit):
  if len(argumentit)<2: return DEFPAIR
  else: return argumentit[1]

#define if there has already been buy before, if so then sell next, if not then buy next
def checkLastAction(kolikko1):
  kk = float(client.get_asset_balance(asset=kolikko1)['free'])
  if kk >= maara and kk > (15/float(getLastPrice(symbol))): return 'BUY'
  else: return 'SELL'

#new client object
client = Client(API_KEY, API_SECRET)

#set variables and values
BASE_URL = 'https://api.binance.com'
SMA_POINTS = ['close', 'close'] 
tyyppi = 'MARKET'
balance=0
ostolause = ''
candles = {}
prices = {}
sma_values = {}
symbol=checkArgs(sys.argv)
TIMEFRAME = SIGNALS[symbol][0]
SMA_PERIODS = [SIGNALS[symbol][1], SIGNALS[symbol][2]] 
LIMIT_NO = max(SMA_PERIODS)
maara = SIGNALS[symbol][3]
kolikko1 = SIGNALS[symbol][4]
kolikko2 = SIGNALS[symbol][5]
last_action = getLastAction(kolikko1)

logging(0, symbol, 'Starting bot...', '', 1)

#set payload for fetching klines, will be fixed later to use client also
payload = {
  'symbol': symbol,
  'interval': TIMEFRAME,
  'limit': LIMIT_NO
}      

#loop until end of the world
while 1 > 0

  #get candles  
  try:
    resp = requests.get(BASE_URL + '/api/v3/klines', params=payload)
    klines = json.loads(resp.content)
    parsed_klines = []
    for k in klines:
      k_candle = {
        'open': float(k[1]),
        'high': float(k[2]),
        'low': float(k[3]),
        'close': float(k[4]),
        'vol': float(k[5]) 
      } 
      parsed_klines.append(k_candle)
  except Exception as e:
    logging(2, symbol, 'Getting candle failed', str(e), 1)
    continue


#get sma values
  sma1 = sma.SMA(SMA_PERIODS[0])
  sma2 = sma.SMA(SMA_PERIODS[1])
  for kline in parsed_klines:
  #add close values to sma objects  
    sma1.add(kline[SMA_POINTS[0]])
    sma2.add(kline[SMA_POINTS[1]])
  sma1_value = sma1.v() 
  sma2_value = sma2.v()
  logging(0, symbol, 'SMA1: ' + str(sma1_value) + ', SMA2: ' + str(sma2_value), '', 1)



#triggers buy and changes last_action
  if (last_action == 'SELL' and sma1_value > sma2_value) or (last_action == 'BUY' and sma2_value > sma1_value):
    logging(0, symbol, 'Trade trickered', '', 1)
#defines clause for trade function, testing purposes use create_test_order instead of create_order
    if  last_action == 'SELL':
      suunta =  'BUY'
      if maara == 0 :
        try:
          balance = client.get_asset_balance(asset=kolikko2)['free']
        except Exception as e:
          logging(2, symbol, 'getBalance failed', str(e), 1)
          continue
        balance = truncate(float(balance) * 0.98, 2)
        print(balance)
        ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quoteOrderQty=" + str(balance) +")"
      else: ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(maara)+")"
    elif  last_action == 'BUY':
      suunta =  'SELL'
      if maara == 0 :
        try:
          balance = truncate(float(client.get_asset_balance(asset=kolikko1)['free']),6)
        except Exception as e:
          logging(2, symbol, 'getBalance failed', str(e), 1)
          continue
        ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(balance)+")"
      else: ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(maara)+")"
    logging(3, symbol, 'Trading', ostolause, 1)
    
#handle trade
    try:
      buy_order = eval(ostolause)
    except Exception as e:
      logging(2, symbol, 'Trade failed', str(e), 1)
      continue      
    logging(1, symbol, 'Trade succesfull', str(buy_order), 1)

#after successfull trade change it to last made action and sleep a bit before new round    
    last_action = suunta
  time.sleep(SLEEPTIME)
filu.close()
