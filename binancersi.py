#==============================================================================================================#
# BinaceRSI.py  
# small bot to trade in binance with help of RSI
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
import sys
import time
from secrets import *
from fuctions import *
from settingsrsi import *
from binance.client import Client

logging(3, 'RSIBOT', 'Starting bot version ' + versio, 'Peep peep boop', 1)
client = Client(API_KEY, API_SECRET)
# [0: symbol, 1: TIMEFRAME, 2: buy rsi low, 3: buy rsi high, 4: sell rsi low, 5: sell rsi high, 6: amount, 7: rsi length, 8: coin1, 9: coin2]
for signal in SIGNALS:
  tiedot.append({'symbol' : signal[0] , 'TIMEFRAME' : signal[1], 'BuyRsiLow': signal[2], 'BuyRsiHigh': signal[3], 'maara': signal[4], 'LIMIT_NO':signal[7], 'kolikko1': signal[8], 'kolikko2': signal[9], 'last_action': checkLastAction(signal[8], signal[6], signal[0], client), 'last_alue': 0})

while True:
  for tieto in tiedot:
    try:
      kauppalause = ''
      toiminta = ''
      parsed_klines = getCandles(tieto['symbol'], tieto['TIMEFRAME'], tieto['LIMIT_NO'] + 1, client)
      #get RSI
      lista = []
      for kline in parsed_klines:
        lista.append(kline['close'])
      rsi1_value = countRSI(lista, tieto['LIMIT_NO'])

      #get RSI area where we at
      aluenyt = 0
      if rsi1_value < tieto['RSIA']: aluenyt = 1
      if rsi1_value >= tieto['RSIA'] and rsi1_value <= tieto['RSIB']: aluenyt = 2
      if rsi1_value > tieto['RSIB']: aluenyt = 3
      if tieto['last_alue'] == 0: tieto['last_alue'] = aluenyt

      #figure out should we buy or sell if anything
      if (tieto['last_action'] == 'BUY') and (aluenyt < tieto['last_alue']): toiminta = 'SELL'
      elif (tieto['last_action'] == 'SELL') and (aluenyt > tieto['last_alue']): toiminta = 'BUY'
      print(tieto['symbol'])
      print('last action: ' + str(tieto['last_action']))
      print('toiminta: ' + str(toiminta))      
      print('aluenyt: ' + str(aluenyt))      
      print('rsi1_value: ' + str(rsi1_value))      
      if toiminta != '':
        print(tieto)
        print(toiminta)
        print(rsi1_value)
        kauppalause = "client.create_test_order(symbol='" + str(tieto['symbol']) + "',side='" + str(toiminta) + "',type='" + str(tyyppi)
        if tieto['maara'] == 0 :
          balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko2'])['free']) * 0.98, DECIMALS[tieto['kolikko2']])
          print('balance: ' + str(balance))
          if toiminta == 'BUY': kauppalause = kauppalause + "',quoteOrderQty=" + str(balance) +")"
          elif toiminta == 'SELL': kauppalause = kauppalause + "',quantity=" + str(balance)+")"
        else: kauppalause = kauppalause + "',quantity=" + str(tieto['maara'])+")"
        
        #do trade
        handleTrade(kauppalause, client, tieto)
        tieto['last_action'] = toiminta
      
      tieto['last_alue'] = aluenyt
      time.sleep(SLEEPTIME)
      
    #if error, log it
    except Exception as e:
      logging(2, tieto['symbol'], 'FAIL: ', str(e), 1)
      continue 