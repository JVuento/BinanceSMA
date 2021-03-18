import requests
import json
import os
import time
BASE_URL = 'https://api.binance.com'
TIMEFRAME = ['1h']
SMA_PERIOD1 = 1
SMA_PERIOD2 = 2
symbol = 'BTCUSDT'
LIMIT_NO = 250
candles = {}
prices = {}
sma_values = {}
filu = file.open('looppi' + str(symbol) + str(TIMEFRAME) + '.txt', 'a')
payload = {
    'symbol': symbol,
    'interval': aika,
    'limit': LIMIT_NO
  }

resp = requests.get(BASE_URL + '/api/v1/klines', params=payload)
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
  filu.write(str(k_candle) + '\n') 
filu.close()