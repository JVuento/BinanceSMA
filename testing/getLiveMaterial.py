import requests
import os
import time
import sys
from secrets import *
from settings import *
from binance.client import Client

def kirjoita(symboli, aika, juttu):
  filu = open('matskua-' + str(symboli) + '-' + str(aika) + '.txt.','a')
  filu.write(str(juttu) + '\n')
  filu.close()

#ajat = ['1h']
ajat = ['1h','15m','4h','30m']
#symbolit = ['BTCUSDT']
symbolit = []
for signal in SIGNALS:
  symbolit.append(signal[0])
client = Client(API_KEY, API_SECRET)



while True:
  for symboli in symbolit:
    print(str(symboli) + ' processing....')
    for aika in ajat:
      resp = client.get_klines(symbol=symboli, interval=aika, limit=20)
      parsed_klines = []
      for k in resp:
        k_candle = {
          'pair': symboli,
          'opentime': int(k[0]),
          'open': float(k[1]),
          'high': float(k[2]),
          'low': float(k[3]),
          'close': float(k[4]),
          'volume': float(k[5]),
          'closetime': int(k[6])
        }
        parsed_klines.append(k_candle)
      kirjoita(symboli, aika, parsed_klines)


      
    time.sleep(90)