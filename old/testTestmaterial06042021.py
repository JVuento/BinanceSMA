import json
import os
import time
from glob import glob
import re
from bfxhfindicators import sma
filet = glob('looppi*')
tulosfilu = open('tulokset.txt', 'a')


for luettavafile in filet:
  
  
  SMA_PERIODS = [1,1]
  MAX_PERIODS = [10,15]
  SMA_POINTS = ['close', 'close']
  candles = []
  
  multipsma1 = 1.000
  multipsma2 = 1.003
  #open files with looppi in start, ex: looppi-BTCUSDT-1h.txt
  filu = open(luettavafile, 'r')
  rivit = filu.readlines()

  for line in rivit:
      line = line.replace('\n','')
      line = line.replace('"','')
      candles.append(eval(line))
  tiedot= candles[0]
  print(tiedot)
  candles.pop(0)
  paras = 0
  parassma = []
  parashold = 0
  for x in range(SMA_PERIODS[0], MAX_PERIODS[0]+1):
    for y in range(max(SMA_PERIODS[1], x), MAX_PERIODS[1]):
      #print('SMA1: ' + str(x) + ' SMA2: ' + str(y))
      last_action = 'SELL'
      saldo = 0
      kauppoja = 0
      kynttilat = []
      kynttilat = candles.copy()
      sma1 = sma.SMA(x)
      sma2 = sma.SMA(y)
      for i in range(x):
        sma1.add(kynttilat[i][SMA_POINTS[0]])
      for j in range(y):
        sma2.add(kynttilat[j][SMA_POINTS[1]])
      for k in range(y):
        kynttilat.pop(0)
      for kynttila in kynttilat:
        #print('added: ' + str(kynttila[SMA_POINTS[0]]))
        sma1.add(kynttila[SMA_POINTS[0]])
        sma2.add(kynttila[SMA_POINTS[1]])
        sma1_value = sma1.v()
        sma2_value = sma2.v()
        if last_action == 'SELL' and sma1_value > sma2_value * multipsma2:
          saldo = saldo - kynttila['close']
          last_action = 'BUY'
          kauppoja = kauppoja + 1
        elif last_action == 'BUY' and sma2_value > sma1_value * multipsma1:
          saldo = saldo + kynttila['close']
          last_action = 'SELL'
          kauppoja = kauppoja + 1
      if last_action == 'BUY':
        saldo = saldo + kynttilat[-1]['close']
      holdi = 0 - kynttilat[0]['close'] + kynttilat[-1]['close']
      if saldo > paras:
        paras = saldo
        parassma = [x,y]
        parashold = holdi
      #print('Saldo: ' + str(saldo) + ' Holdi: ' + str(holdi) + ' Kauppoja: ' + str(kauppoja))
  print('Paras: ' + str(paras) + ', ' + str(parassma) + ', Hold: ' + str(parashold))  
