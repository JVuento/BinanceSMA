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
from bfxhfindicators import sma
from secrets import *
from fuctions import *
from settings_2 import *
from binance.client import Client

logging(3, '', 'Starting bot version ' + versio, '', 1)
client = Client(API_KEY, API_SECRET)

for signal in SIGNALS:
  tiedot.append({'symbol' : signal[0] , 'TIMEFRAME' : signal[1], 'SMA_PERIODS': [signal[2], signal[3]], 'LIMIT_NO': max([signal[2], signal[3]]), 'maara': signal[4], 'kolikko1': signal[5], 'kolikko2': signal[6], 'last_action': checkLastAction(signal[5], signal[4], signal[0], client), 'SMA_POINTS':[signal[7],signal[8]], 'sma1multip':signal[9], 'sma2multip':signal[10], 'group':signal[11], 'buyprice':0, 'sellprice':0, 'highprice':0, 'lowprice':0 })
print(tiedot)
#loop until end of the world
while True:
  for tieto in tiedot:
    time.sleep(SLEEPTIME)
    kauppalause = ''
    #get candles  
    parsed_klines = getCandles(tieto['symbol'], tieto['TIMEFRAME'], tieto['LIMIT_NO'], client)
    lastclose = parsed_klines[-1]['close']
    #get sma values
    sma1 = sma.SMA(tieto['SMA_PERIODS'][0])
    sma2 = sma.SMA(tieto['SMA_PERIODS'][1])
    for kline in parsed_klines:
      sma1.add(kline[tieto['SMA_POINTS'][0]])
      sma2.add(kline[tieto['SMA_POINTS'][1]])
    sma1_value = sma1.v() 
    sma2_value = sma2.v()
    case = 0
    
    #check if trade is needed
    if (tieto['last_action'] == 'SELL') and (sma1_value > (sma2_value * tieto['sma2multip'])): case = 1
    elif (tieto['last_action'] == 'SELL') and (lastclose>(tieto['lowprice'] * SELLSTOP)) and (tieto['lowprice'] != 0): case = 2
    elif (tieto['last_action'] == 'SELL') and (lastclose<(tieto['buyprice'] * tieto['sma1multip'])) and (tieto['buyprice'] != 0): case = 3
    elif (tieto['last_action'] == 'BUY') and ((sma2_value > (sma1_value * tieto['sma1multip']))): case = 4
    elif (tieto['last_action'] == 'BUY') and (lastclose<(tieto['highprice'] * BUYSTOP)) and (tieto['highprice'] != 0): case = 5
    elif (tieto['last_action'] == 'BUY') and (lastclose>(tieto['sellprice'] * tieto['sma2multip'])) and (tieto['sellprice'] != 0): case = 6
    else: case = 0
    print('CASE: ' + str(case) + ', SMA1: ' + str(sma1_value) + ', SMA2: ' + str(sma2_value))
    #define what we are doing
    if case in [1,2,6]: suunta = 'BUY'
    elif case in [3,4,5]: suunta = 'SELL'
    elif case == 0: suunta = vaihdasuunta(tieto['last_action'])
    print('LAST CLOSE: ' + str(lastclose))
    print('SUUNTA: ' + str(suunta))
    print('LAST ACTION: ' + str(tieto['last_action']))
    #create trade clause
    if case > 0 and ((case in [1,2,4,5] and suunta != tieto['last_action']) or (case in [3,6] and suunta == tieto['last_action'])):
      print('EKA IF OHI')
      kauppalause = "client.create_test_order(symbol='" + str(tieto['symbol']) + "',side='" + str(suunta) + "',type='" + str(tyyppi)
      if suunta == 'BUY':
        print('TOKA IF BUY')
        tieto['buyprice'] = lastclose
        if tieto['maara'] == 0 :
          balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko2'])['free']) * 0.98, DECIMALS[tieto['kolikko2']])
          kauppalause = kauppalause + "',quoteOrderQty=" + str(balance) +")"
        else: kauppalause = kauppalause + "',quantity=" + str(tieto['maara'])+")"
      elif suunta == 'SELL':
        print('TOKA IF SELL')
        tieto['sellprice'] = lastclose 
        if tieto['maara'] == 0 :
          balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko1'])['free']),DECIMALS[tieto['kolikko1']])
          kauppalause = kauppalause + "',quantity=" + str(balance)+")"
        else: kauppalause = kauppalause + "',quantity=" + str(tieto['maara'])+")"
      #do trade
      handleTrade(kauppalause)
      print(str(suunta) + ': ' + str(lastclose))

    #set values depending of case if needed
    if case in [1,4]:
      print('EKA KEISSI')
      tieto['buyprice']=0
      tieto['sellprice']=0
      tieto['highprice']=0
      tieto['lowprice']=0
      tieto['last_action'] = vaihdasuunta(tieto['last_action'])
    elif case == 2:
      print('TOKA KEISSI')
      tieto['buyprice'] = lastclose
      tieto['highprice']=0
      tieto['lowprice']=0      
    elif case == 4:
      print('KOLMAS KEISSI')
      tieto['sellprice'] = lastclose
      tieto['highprice']=0
      tieto['lowprice']=0    
    if lastclose > tieto['highprice']: tieto['highprice'] = lastclose
    elif (lastclose < tieto['lowprice']) or (tieto['lowprice'] == 0): tieto['lowprice'] = lastclose
    print(tieto)
#The End
