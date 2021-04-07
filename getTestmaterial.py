import requests
import json
import os
import time
BASE_URL = 'https://api.binance.com'
TIMEFRAME = ['4h']
SMA_PERIOD1 = 1
SMA_PERIOD2 = 2
symbol1 = 'BTC'
symbol2 = 'USDT'
symbols = 'BTCUSDT'
LIMIT_NO = 250
candles = {}
prices = {}
sma_values = {}
filu = open('looppi-' + str(symbols) + '-' + str(TIMEFRAME[0].replace("'","")) + '.txt', 'a')
payload = {
    'symbol': symbols,
    'interval': TIMEFRAME[0],
    'limit': LIMIT_NO
  }

resp = requests.get(BASE_URL + '/api/v1/klines', params=payload)
klines = json.loads(resp.content)
parsed_klines = []
filu.write('{'+ "'symbols':'" + symbols + "','symbol1':'" + symbol1 + "','symbol2':'" + symbol2 + "','timeframe':'" + str(TIMEFRAME[0]) + "'}" + "\n") 
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
print('Haettu')