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
from datetime import datetime
from secrets import *
from tsl_functions import *
from tsl_settings import *
from binance.client import Client

logging(3, 'BOT', 'Starting bot version ' + VERSIO, 'Peep peep boop', 1)
client = Client(API_KEY, API_SECRET)

for coin in COINS:
  info = client.get_symbol_info(coin[0]+coin[1])
  #get symbols minimum ticksize
  trunc = 0.01000000
  for filter in info['filters']:
    if filter['filterType'] == 'PRICE_FILTER': trunc = filter['tickSize']
  trunc = 9 - len(str(int(float(trunc) * 100000000)))
  #save information about symbols
  TIEDOT.append({'symbol':coin[0]+coin[1], 'kolikko1':coin[0], 'kolikko2': coin[1], 'stoploss':coin[2], 'altamount':0, 'trunc':trunc})

while True:
  tauko=1
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
          tieto['altamount'] = altmaara
          #make sell order
          stopprice = str(truncate((1-kerroin) * float(kynttila[0]['high']),tieto['trunc']))
          price = str(truncate((1-kerroin*2) * float(kynttila[0]['high']),tieto['trunc']))
          kauppalause = "client.create_order(symbol='" + str(tieto['symbol']) + "',side='SELL',type='STOP_LOSS_LIMIT',stopPrice=" + stopprice
          kauppalause = kauppalause + ",price=" + price + ",quantity=" + str(truncate(float(altmaara), tieto['trunc'])) + ",timeInForce='GTC')"
          handleTrade(kauppalause, tieto['symbol'], client)
          loglause = 'Stop:' + str(stopprice) + ', quantity:' + str(truncate(float(altmaara)))
          logging(1, str(tieto['symbol']),'Sell', str(loglause), 1)
        else:
          #make buy order
          stopprice = str(truncate((1+kerroin) * float(kynttila[0]['low']),tieto['trunc']))
          price = str(truncate((1+kerroin*2) * float(kynttila[0]['low']),tieto['trunc']))
          kauppalause = "client.create_order(symbol='" + str(tieto['symbol']) + "',side='BUY',type='STOP_LOSS_LIMIT',stopPrice=" + stopprice
          kauppalause = kauppalause + ",price=" + price + ",quantity=" + str(truncate(float(tieto['altamount']),tieto['trunc'])) +",timeInForce='GTC')"
          handleTrade(kauppalause, tieto['symbol'], client)
          loglause = 'Stop:' + str(stopprice) + ', quantity:' + str(truncate(float(tieto['altamount'])))
          logging(1, str(tieto['symbol']),'Buy', str(loglause), 1)
          
      #tarkistetaan pitääkö muuttaa orderia, jos niin poistetaan vanha order
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

  
