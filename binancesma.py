
import requests
import json
import os
import time
#run in shell: 
# pip install git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#until i get this figured out
from bfxhfindicators import sma
BASE_URL = 'https://api.binance.com'

TIMEFRAME = '15m'
SMA_PERIODS = [5, 10] #use only 2
SMA_POINTS = ['close', 'close'] 
LIMIT_NO = max(SMA_PERIODS)
symbol = ['BTCUSDT']
candles = {}
prices = {}
sma_values = {}
last_action = 'sell'
saldo = 100000

#file handling for testing
filu = open('kaupat.txt', 'a')

print(symbol)
filu.write(' ' + '\n'+ str(symbol) + ' ' + str(TIMEFRAME) + ' ' + str(SMA_PERIODS) + ' ' + str(SMA_POINTS) + '\n')
payload = {
  'symbol': symbol,
  'interval': TIMEFRAME,
  'limit': LIMIT_NO
}

#function for trade
def treidaa(symbooli, mitatehda, hinta):
# if mitatehda = 1 then buy if 0 then sell
  if mitatehda == 'sell':
    print('+' + str(hinta))
    filu.write('+' + str(hinta) + '\n')
  elif mitatehda == 'buy':
    print('-' + str(hinta))
    filu.write('-' + str(hinta) + '\n')
  return 1

#loop until end of the world
while saldo > 0 and saldo < 200000:
  #get candles  
  time.sleep(120)  
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
  #triggers buy and changes last_action
  if last_action == 'sell' and sma1_value > sma2_value:
    treidaa(symbol, 'buy', parsed_klines[-1]['close'])
    last_action = 'buy'
    saldo = saldo - parsed_klines[-1]['close']
  #triggers sell and changes last_action
  elif last_action == 'buy' and sma2_value > sma1_value:
    treidaa(symbol, 'sell', parsed_klines[-1]['close'])
    last_action = 'sell'
    saldo = saldo + parsed_klines[-1]['close']

filu.close()
