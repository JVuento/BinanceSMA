#==============================================================================================================
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
import datetime
import time
import sys
import math
from datetime import datetime
from bfxhfindicators import sma
from templatesecrets import *
from secrets import *
from settings import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

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

#logging function, writes argument in log file
def logging(teksti):
  logfilu = open('botlog.txt','a')
  logfilu.write(str(datetime.now()) + '; ' + teksti+ '\n' )
  print(str(datetime.now()) + '; ' + teksti)
  logfilu.close()

#get last price 
def getLastPrice(symbooli):
    tikkeri = client.get_ticker(symbol=symbooli)['lastPrice']
    return tikkeri

#if using heroku, set env vars in Heroku CLI
#heroku config:set API_KEY=<your api key>
#heroku config:set API_SECRET=<your api secret>
#then bring'em here. Commented out so far
#API_KEY = os.getenv('API_KEY')
#API_SECRET = os.environ.get('API_SECRET')

argumentit = sys.argv
client = Client(API_KEY, API_SECRET)
if len(sys.argv)<2: symbol = 'XVSBUSD'
else: symbol = argumentit[1]
BASE_URL = 'https://api.binance.com'
TIMEFRAME = SIGNALS[symbol][0]
SMA_PERIODS = [SIGNALS[symbol][1], SIGNALS[symbol][2]] #use only 2
SMA_POINTS = ['close', 'close'] 
LIMIT_NO = max(SMA_PERIODS)

maara = SIGNALS[symbol][3]
kolikko1 = SIGNALS[symbol][4]
kolikko2 = SIGNALS[symbol][5]

candles = {}
prices = {}
sma_values = {}
kk = client.get_asset_balance(asset=kolikko1)['free']
print(kk)
kk = float(kk)
if kk >= maara and kk > (15/float(getLastPrice(symbol))): last_action = 'BUY'
else: last_action = 'SELL'
print('Last action: ' + str(last_action))
tyyppi = 'MARKET'
saldo = 100000
balance=0
ostolause = ''



#set payload for fetching klines, will be fixed later to use client also
payload = {
  'symbol': symbol,
  'interval': TIMEFRAME,
  'limit': LIMIT_NO
}      
print(payload)


#loop until end of the world
while saldo > 0 and saldo < 200000:
  #get candles  
  time.sleep(120)
  try:
    resp = requests.get(BASE_URL + '/api/v3/klines', params=payload)
  except Exception as e:
    logging('Loop failed:' +  str(e))
    continue
  klines = json.loads(resp.content)

  #parse to get only needed values
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

  sma1 = sma.SMA(SMA_PERIODS[0])
  sma2 = sma.SMA(SMA_PERIODS[1])
  for kline in parsed_klines:
  #add close values to sma objects  
    sma1.add(kline[SMA_POINTS[0]])
    sma2.add(kline[SMA_POINTS[1]])
  sma1_value = sma1.v() 
  sma2_value = sma2.v()
  print(symbol + ', SMA1: ' + str(sma1_value) + ', SMA2: ' + str(sma2_value))
  #triggers buy and changes last_action
  if (last_action == 'SELL' and sma1_value > sma2_value) or (last_action == 'BUY' and sma2_value > sma1_value):
  
    try:
      balance = client.get_asset_balance(asset=kolikko2)['free']
    except Exception as e:
      logging('getBalance failed:' +  str(e))
      continue

    if  last_action == 'SELL':
      suunta =  'BUY'
      if maara == 0 :
        try:
          balance = client.get_asset_balance(asset=kolikko2)['free']
        except Exception as e:
          logging('getBalance failed:' +  str(e))
          continue
        print('YOOOYOYOYOOO')
        print(balance)
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
          logging('getBalance failed:' +  str(e))
          continue
        ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(balance)+")"
      else: ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(maara)+")"
    
    
    
    logging('Trade:' + str(ostolause))
    #testing purposes use create_test_order instead of create_order
    try:
      buy_order = eval(ostolause)
    except BinanceAPIException as e:
      # error handling goes here
      logging('Trade failed:' +  str(e))
      continue
    except BinanceOrderException as e:
      # error handling goes here
      logging('Trade failed:' +  str(e))  
      continue
    except Exception as e:
      logging('Trade failed:' +  str(e))  
      continue      
    logging('Trade succesfull: ' + str(buy_order))
    last_action = suunta

filu.close()
