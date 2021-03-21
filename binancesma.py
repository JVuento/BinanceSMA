
import requests
import json
import os
import time
#run in shell: 
# pip install git+https://github.com/bitfinexcom/bfx-hf-indicators-py 
#until i get this figured out
from bfxhfindicators import sma
#pip install python-binance
#more info about python-binance lib here: https://algotrading101.com/learn/binance-python-api-guide/
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)
#print(client.get_account()) #this prints the account balance

BASE_URL = 'https://api.binance.com'
TIMEFRAME = '15m'
SMA_PERIODS = [4, 12] #use only 2
SMA_POINTS = ['close', 'close'] 
LIMIT_NO = max(SMA_PERIODS)
symbol = ['XLMUSDT']

candles = {}
prices = {}
sma_values = {}
last_action = 'sell'
saldo = 100000

#file handling for testing
filu = open('kaupat.txt', 'a')
logfilu = open('botlog.txt','a')


print(symbol)
filu.write(' ' + '\n'+ str(symbol) + ' ' + str(TIMEFRAME) + ' ' + str(SMA_PERIODS) + ' ' + str(SMA_POINTS) + '\n')
payload = {
  'symbol': symbol,
  'interval': TIMEFRAME,
  'limit': LIMIT_NO
}

#args: symbol, side, type, quantity
def do_trade(sy, si, ty, qu):
  try:
      buy_order = client.create_order(
        symbol=sy,
        side=si,
        type=ty,
        quantity=qu)
      print("Trade done: " + sy + si + ty + str(qu))
  except BinanceAPIException as e:
      # error handling goes here
      print(e)
  except BinanceOrderException as e:
      # error handling goes here
      print(e)

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
  time.sleep(60)  
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
  print("SMA 1 (" + str(SMA_PERIODS[0]) + ")" + "  : " + str(sma1_value))
  print("SMA 2 (" + str(SMA_PERIODS[1]) + ")" + " : " + str(sma2_value))
  
  #triggers buy and changes last_action
  if last_action == 'sell' and sma1_value > sma2_value:
    treidaa(symbol, 'buy', parsed_klines[-1]['close'])
    do_trade(symbol, 'BUY', 'MARKET', 80)
    last_action = 'buy'
    saldo = saldo - parsed_klines[-1]['close']
  #triggers sell and changes last_action
  elif last_action == 'buy' and sma2_value > sma1_value:
    treidaa(symbol, 'sell', parsed_klines[-1]['close'])
    do_trade(symbol, 'SELL', 'MARKET', 80)
    last_action = 'sell'
    saldo = saldo + parsed_klines[-1]['close']

filu.close()
