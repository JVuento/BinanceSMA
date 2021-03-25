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
import time
import sys
from datetime import datetime
from bfxhfindicators import sma
from secrets import *
from binance.client import Client

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

#set payload for fetching klines, will be fixed later to use client also
payload = {
  'symbol': symbol,
  'interval': TIMEFRAME,
  'limit': LIMIT_NO
}      
print(payload)


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
    logging('Getting candle failed:' +  str(e))
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
  print(symbol + ', SMA1: ' + str(sma1_value) + ', SMA2: ' + str(sma2_value))



#triggers buy and changes last_action
  if (last_action == 'SELL' and sma1_value > sma2_value) or (last_action == 'BUY' and sma2_value > sma1_value):

#defines clause for trade function, testing purposes use create_test_order instead of create_order
    if  last_action == 'SELL':
      suunta =  'BUY'
      if maara == 0 :
        try:
          balance = client.get_asset_balance(asset=kolikko2)['free']
        except Exception as e:
          logging('getBalance failed:' +  str(e))
          continue
        balance = round(float(balance) * 0.98, 2)
        print(balance)
        ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quoteOrderQty=" + str(balance) +")"
      else: ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(maara)+")"
    elif  last_action == 'BUY':
      suunta =  'SELL'
      if maara == 0 :
        try:
          balance = round(float(client.get_asset_balance(asset=kolikko1)['free']),6)
        except Exception as e:
          logging('getBalance failed:' +  str(e))
          continue
        ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(balance)+")"
      else: ostolause = "client.create_order(symbol='" + str(symbol) + "',side='" + str(suunta) + "',type='" + str(tyyppi) + "',quantity=" + str(maara)+")"
    logging('Trade:' + str(ostolause))
    
#handle trade
    try:
      buy_order = eval(ostolause)
    except Exception as e:
      logging('Trade failed:' +  str(e))  
      continue      
    logging('Trade succesfull: ' + str(buy_order))

#after successfull trade change it to last made action and sleep a bit before new round    
    last_action = suunta
  time.sleep(SLEEPTIME)
filu.close()
