import json
import os
import time
from glob import glob
import re
from bfxhfindicators import sma
periodrounds = 12
filet = glob('looppi*')
tulosfilu = file.open('tulokset.txt', 'a')


for luettavafile in filet:
  saldo = 0
  SMA_PERIODS = [1, 2]
  LIMIT_NO = max(SMA_PERIODS)
  #open files with looppi in start, ex: looppiBTCUSDT250.txt
  filu = file.open(luettavafile, 'r')
  rivit = filu.readlines()
  #removes looppi and .txt from it
  luettavafile = luettavafile.replace('looppi','')
  luettavafile = luettavafile.replace('.txt','')
  symtim = luettavafile.split(filu, '.')
  #sould be now like BTCUSDT-250, now need to get symbol and timeframe from it
  symbol = symtim[0]
  TIMEFRAME = symtim[1]
  #for each first SMA_PERIODS
  for i in periodrounds:
    period1 = SMA_PERIODS[0] + i
    #for each second SMA_PERIODS
    for j in periodrounds:
        period1 = SMA_PERIODS[1] + j
