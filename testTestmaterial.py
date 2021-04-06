import json
import os
import time
from glob import glob
import re
from bfxhfindicators import sma
filet = glob('looppi*')
tulosfilu = open('tulokset.txt', 'a')


for luettavafile in filet:
  saldo = 0
  kauppoja = 0
  SMA_PERIODS = [5, 10]
  SMA_POINTS = ['close', 'close']
  candles = []
  last_action = 'SELL'
  multipsma1 = 1.000
  multipsma2 = 1.001
  #open files with looppi in start, ex: looppi-BTCUSDT-1h.txt
  filu = open(luettavafile, 'r')
  rivit = filu.readlines()

  for line in rivit:
      line = line.replace('\n','')
      line = line.replace('"','')
      candles.append(eval(line))
  tiedot= candles[0]
  candles.pop(0)
  sma1 = sma.SMA(SMA_PERIODS[0])
  sma2 = sma.SMA(SMA_PERIODS[1])
  for i in range(SMA_PERIODS[0]):
    sma1.add(candles[i][SMA_POINTS[0]])
  for j in range(SMA_PERIODS[1]):
    sma2.add(candles[j][SMA_POINTS[1]])
  for k in range(SMA_PERIODS[1]):
    candles.pop(0)
  for candle in candles:
    sma1.add(candle[SMA_POINTS[0]])
    sma2.add(candle[SMA_POINTS[1]])
    sma1_value = sma1.v()
    sma2_value = sma2.v()
    if last_action == 'SELL' and sma1_value > sma2_value * multipsma2:
      #print('-' + str(candle['close']))
      saldo = saldo - candle['close']
      last_action = 'BUY'
      kauppoja = kauppoja + 1
    elif last_action == 'BUY' and sma2_value > sma1_value * multipsma1:
      #print('+' + str(candle['close']))
      saldo = saldo + candle['close']
      last_action = 'SELL'
      kauppoja = kauppoja + 1
  if last_action == 'BUY':
    saldo = saldo + candles[-1]['close']
  holdi = 0 - candles[0]['close'] + candles[-1]['close']
  print(tiedot)
  print('Saldo: ' + str(saldo))
  print('Holdi: ' + str(holdi))
  print('Kauppoja: ' + str(kauppoja))
  
