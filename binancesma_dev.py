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
from settings_dev import *
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
    printtiteksti = str(datetime.now()) + ', ' + tyypit[TYYPPI] + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA
    print(printtiteksti)
  logiteksti = tyypit[TYYPPI] + ', ' + str(datetime.now()) + ', ' + PARI + ', ' + LYHYT + ', ' + PITKA + '\n'
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

#define if there has already been buy before, if so then sell next, if not then buy next
def checkLastAction(kolikko, maara, pari):
  kk = float(client.get_asset_balance(asset=kolikko)['free'])
  if kk >= maara and kk > (15/float(getLastPrice(pari))): return 'BUY'
  else: return 'SELL'

#new client object
versio='1.0003b'
client = Client(API_KEY, API_SECRET)
logging(3, '', 'Starting bot version ' + versio, '', 1)
#set variables and values
tyyppi = 'MARKET'
balance=0
groups = []
seq = [x[11] for x in SIGNALS]
for i in range(max(seq)+1):
  groups.append([])
sma_values = {}
# tiedot = [{'symbol' : , 'TIMEFRAME' : , 'SMA_PERIODS': , 'LIMIT_NO': , 'maara': , 'kolikko1': , 'kolikko2': , 'last_Action': , 'sma1_value': , 'sma2_value': }]
tiedot = []
for signal in SIGNALS:
  #tiedot.append({'symbol' : signal[0] , 'TIMEFRAME' : signal[1], 'SMA_PERIODS': [signal[2], signal[3]], 'LIMIT_NO': max([signal[2], signal[3]]), 'maara': signal[4], 'kolikko1': signal[5], 'kolikko2': signal[6], 'last_action': checkLastAction(signal[5], signal[4], signal[0]), 'SMA_POINTS':[signal[7],signal[8]], 'sma1multip':signal[9], 'sma2multip':signal[10], 'group':signal[11] })
  groups[signal[11]].append({'symbol' : signal[0] , 'TIMEFRAME' : signal[1], 'SMA_PERIODS': [signal[2], signal[3]], 'LIMIT_NO': max([signal[2], signal[3]]), 'maara': signal[4], 'kolikko1': signal[5], 'kolikko2': signal[6], 'last_action': checkLastAction(signal[5], signal[4], signal[0]), 'SMA_POINTS':[signal[7],signal[8]], 'sma1multip':signal[9], 'sma2multip':signal[10], 'group':signal[11] })
for j in tiedot:
  logging(0, '', str(j), '', 1)

#loop until end of the world
while True:
  for group in groups:
    if group == []: continue
    seq = []
    seq = [x['last_action'] for x in group]
    
    ryhma = []
    if group[0]['group'] == 0 or (group[0]['group'] != 0 and (not 'BUY' in seq)):
      ryhma = group.copy()
    elif 'BUY' in seq:
      ryhma.append(next(item for item in group if item['last_action'] == 'BUY'))
    logging(3, '', 'Next group ' + str(ryhma), '', 1)
    for tieto in ryhma:
      ostolause = ''
      #get candles  
      try:
        print(tieto['symbol'])
        resp = client.get_klines(symbol=tieto['symbol'], interval=tieto['TIMEFRAME'], limit=tieto['LIMIT_NO'])
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
      except Exception as e:
        logging(2, tieto['symbol'], 'Getting candle failed', str(e), 1)
        continue
    
    
    #get sma values
      sma1 = sma.SMA(tieto['SMA_PERIODS'][0])
      sma2 = sma.SMA(tieto['SMA_PERIODS'][1])
      for kline in parsed_klines:
      #add close values to sma objects  
        sma1.add(kline[tieto['SMA_POINTS'][0]])
        sma2.add(kline[tieto['SMA_POINTS'][1]])
      sma1_value = sma1.v() 
      sma2_value = sma2.v()
      logging(0, tieto['symbol'], 'SMA1: ' + str(sma1_value) + ', SMA2: ' + str(sma2_value), '', 1)
    
    
    
    #triggers buy and changes last_action
      if (tieto['last_action'] == 'SELL' and sma1_value > (sma2_value * tieto['sma2multip'])) or (tieto['last_action'] == 'BUY' and sma2_value > (sma1_value * tieto['sma1multip'])):
        logging(0, tieto['symbol'], 'Trade trickered ' + 'SMA1 :' + str(sma1_value) + ', SMA2: ' + str(sma2_value), '', 1)
        
    #defines clause for trade function, testing purposes use create_test_order instead of create_order
        if  tieto['last_action'] == 'SELL':
          suunta =  'BUY'
          ostolause = "client.create_test_order(symbol='" + str(tieto['symbol']) + "',side='" + str(suunta) + "',type='" + str(tyyppi)
          if tieto['maara'] == 0 :
            try:
              balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko2'])['free']) * 0.98, DECIMALS[tieto['kolikko2']])
              ostolause = ostolause + "',quoteOrderQty=" + str(balance) +")"
            except Exception as e:
              logging(2, tieto['symbol'], 'getBalance failed', str(e), 1)
              continue 
          else: ostolause = ostolause + "',quantity=" + str(tieto['maara'])+")"
        elif  tieto['last_action'] == 'BUY':
          suunta =  'SELL'
          ostolause = "client.create_test_order(symbol='" + str(tieto['symbol']) + "',side='" + str(suunta) + "',type='" + str(tyyppi)
          if tieto['maara'] == 0 :
            try:
              balance = truncate(float(client.get_asset_balance(asset=tieto['kolikko1'])['free']),DECIMALS[tieto['kolikko1']])
              ostolause = ostolause + "',quantity=" + str(balance)+")"
            except Exception as e:
              logging(2, tieto['symbol'], 'getBalance failed', str(e), 1)
              continue
          else: ostolause = ostolause + "',quantity=" + str(tieto['maara'])+")"
        
        logging(3, tieto['symbol'], 'Trading: ' + suunta, ostolause, 1)
        
    #handle trade
        try:
          buy_order = eval(ostolause)
        except Exception as e:
          logging(2, tieto['symbol'], 'Trade failed', str(e), 1)
          continue
        summat = []
        summat = [x['last_action'] for x in buy_order]
        if buy_order == {}:
          
          buy_order = {'symbol': 'TESTING', 'orderId': 1111, 'cummulativeQuoteQty': '123.45', 'side':'TEST'}
        if buy_order['side'] == 'BUY':
          logging(1, tieto['symbol'],'Trade succesfull', '-' + str(buy_order['cummulativeQuoteQty']), 1)
        else:
          logging(1, tieto['symbol'],'Trade succesfull', '+' + str(buy_order['cummulativeQuoteQty']), 1)
    #after successfull trade change it to last made action and sleep a bit before new round    
        tieto['last_action'] = suunta
      time.sleep(SLEEPTIME)

#The End
