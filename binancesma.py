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
#==============================================================================================================#

import requests
import json
import os
import datetime
import time
from datetime import datetime
from bfxhfindicators import sma
from secrets import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

client = Client(API_KEY, API_SECRET)
symbol = 'REEFUSDT'
BASE_URL = 'https://api.binance.com'
TIMEFRAME = SIGNALS[symbol][0]
SMA_PERIODS = [SIGNALS[symbol][1], SIGNALS[symbol][2]] #use only 2
SMA_POINTS = ['close', 'close'] 
LIMIT_NO = max(SMA_PERIODS)

maara = 1500

candles = {}
prices = {}
sma_values = {}
last_action = 'SELL'
tyyppi = 'MARKET'
saldo = 100000


#logging function, writes argument in log file
def logging(teksti):
  logfilu = open('botlog.txt','a')
  logfilu.write(str(datetime.now()) + '; ' + teksti+ '\n' )
  print(str(datetime.now()) + '; ' + teksti)
  logfilu.close()

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
  time.sleep(60)  
  resp = requests.get(BASE_URL + '/api/v3/klines', params=payload)
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
    if  last_action == 'SELL': suunta =  'BUY'
    elif  last_action == 'BUY': suunta =  'SELL'
    logging('Trade:' + str(symbol) + ',' +  str(suunta) + ',' + str(tyyppi) + ',' + str(maara))
    #testing purposes use create_test_order instead of create_order
    try:
      buy_order = client.create_order(
        symbol=symbol,
        side=suunta,
        type=tyyppi,
        quantity=maara)
    except BinanceAPIException as e:
      # error handling goes here
      logging('Trade failed:' +  str(e))
      continue
    except BinanceOrderException as e:
      # error handling goes here
      logging('Trade failed:' +  str(e))  
      continue
    logging('Trade succesfull: ' + str(buy_order))
    last_action = suunta

filu.close()
