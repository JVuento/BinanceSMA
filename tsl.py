#==============================================================================================================#
# tsl.py  
# small bot to trade in binance with Trailing Stop Losses
#
#
# Before run make sure you have bfx-hf-indicators-p and python-binance installed in you python : 
#  pip install git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#  pip install python-binance
#  more info about python-binance lib here: https://algotrading101.com/learn/binance-python-api-guide/
#
#  For python anywhere:
#  pip3.8 install --user git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#  pip3.8 install --user python-binance
#
# Remember you are using this at your own risk, don't come crying to us if it fucks up your wallet. Thank you.
#==============================================================================================================#

import requests
import os
import time
import sys
import math
import importlib
from datetime import datetime
from secrets import *
from tsl_functions import *
import tsl_settings
from binance.client import Client

logging(3, 'BOT', 'Initiating wallet destruction...', 'Peep peep boop', 1)
client = Client(API_KEY, API_SECRET)

while True:
  tauko=1
  importlib.reload(sys.modules['tsl_settings'])
  from tsl_settings import *
  TIEDOT = getTiedot(COINS, client)
  for tieto in TIEDOT:
    try:
      order = client.get_open_orders(symbol=tieto['symbol'])
      kerroin = tieto['stoploss']/100
      assetti = client.get_asset_balance(asset=tieto['kolikko1'])
      altmaara = float(assetti['free']) + float(assetti['locked'])
      last_action = checkLastAction(tieto['kolikko1'], tieto['symbol'], altmaara, client)
      kynttila = getCandles(tieto['symbol'], '5m', '1', client)
      # example kynttila: [{'open': 47503.39, 'high': 47508.54, 'low': 47000.00, 'close': 47457.98, 'vol': 1.0709}]         
      if order == []:
        kauppalause = ''
        if last_action == 'BUY':
          #make sell order
          stopprice = str(truncate((1-kerroin) * float(kynttila[0]['high']),tieto['tick']))
          price = str(truncate((1-kerroin*2) * float(kynttila[0]['high']),tieto['tick']))
          kauppalause = "client.create_order(symbol='" + str(tieto['symbol']) + "',side='SELL',type='STOP_LOSS_LIMIT',stopPrice=" + stopprice
          kauppalause = kauppalause + ",price=" + price + ",quantity=" + str(truncate(float(altmaara), tieto['trunc'])) + ",timeInForce='GTC')"
          handleTrade(kauppalause, tieto['symbol'], client)
          loglause = 'Stop:' + str(stopprice) + ', quantity:' + str(truncate(float(altmaara)))
          logging(1, str(tieto['symbol']),'Sell', str(loglause), 1)
        else:
          #make buy order
          stopprice = str(truncate((1+kerroin) * float(kynttila[0]['low']),tieto['tick']))
          price = str(truncate((1+kerroin*2) * float(kynttila[0]['low']),tieto['tick']))
          kauppalause = "client.create_order(symbol='" + str(tieto['symbol']) + "',side='BUY',type='STOP_LOSS_LIMIT',stopPrice=" + stopprice
          kauppalause = kauppalause + ",price=" + price + ",quantity=" + str(truncate(float(tieto['altamount']),tieto['trunc'])) +",timeInForce='GTC')"
          handleTrade(kauppalause, tieto['symbol'], client)
          loglause = 'Stop:' + str(stopprice) + ', quantity:' + str(truncate(float(tieto['altamount'])))
          logging(1, str(tieto['symbol']),'Buy', str(loglause), 1)
          
      #tarkistetaan pitääkö muuttaa orderia, jos niin poistetaan vanha order
      #else:
      else:
        order = order[0]     
        if last_action == 'BUY':
          if (1-kerroin) * float(kynttila[0]['high']) > float(order['stopPrice']):
            cancelOrder(order['orderId'], tieto['symbol'], client)
            tauko = 0
            loglause = 'Cancel:' + str(order['orderId'])
            logging(1, str(tieto['symbol']),'Cancel', str(loglause), 1)
          else: continue
          
        else:
          if (1+kerroin) * float(kynttila[0]['low']) < float(order['stopPrice']):
            cancelOrder(order['orderId'], tieto['symbol'], client)
            tauko = 0
            loglause = 'Cancel:' + str(order['orderId'])
            logging(1, str(tieto['symbol']),'Cancel', str(loglause), 1)
          else: continue
      
    except Exception as e:
      logging(2, tieto['symbol'], 'FAIL: ', str(e), 1)
      continue
  if tauko == 1:
    time.sleep(200)
  else:
    time.sleep(10)

  
